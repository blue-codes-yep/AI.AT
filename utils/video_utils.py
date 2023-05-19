import moviepy.editor as mp
import concurrent.futures
from utils.progress_utils import celery
import requests
import base64
import numpy as np
import os
import tempfile
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from io import BytesIO
from PIL import Image
from pathlib import Path
from utils.subtitle_utils import split_sentences, generate_subtitle_timings, get_audio_duration
from utils.polly_utils import synthesize_speech
from utils.s3_utils import upload_to_s3
from celery import group

def resize_image(image, width=1280, height=720):
    aspect_ratio = image.width / image.height
    new_width = width
    new_height = int(new_width / aspect_ratio)

    if new_height > height:
        new_height = height
        new_width = int(new_height * aspect_ratio)

    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    return image


def download_and_resize_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    resized_image = image.resize((1280, 720))  # Adjust the size as per your requirement
    return resized_image


def create_subtitle_clip(text, start_time, end_time, video_size, fps=24):
    fontsize = 34  # Increase the fontsize for better text quality
    padding = 10
    background_opacity = 128  # Change this value (0-255) to adjust the opacity of the subtitle background
    move_up_pixels = (
        50.9  # The number of pixels to move the subtitle up from the bottom
    )

    # Create the text clip
    subtitle_text = TextClip(
        txt=text,
        fontsize=fontsize,
        color="white",
        font="C:\\USERS\\BLUE\\APPDATA\\LOCAL\\MICROSOFT\\WINDOWS\\FONTS\\ROBOTOSLAB-VARIABLEFONT_WGHT.TTF",
        stroke_color="black",
        stroke_width=0.9,  # Increase the stroke_width for better edge contrast
    )

    # Create a semi-transparent background for the subtitle
    text_size = subtitle_text.size
    background_size = (text_size[0] + 2 * padding, text_size[1] + 2 * padding)
    subtitle_background = ColorClip(
        size=background_size, color=(0, 0, 0, background_opacity)
    )

    # Combine the text and background clips
    subtitle = (
        CompositeVideoClip(
            [
                subtitle_background.set_position(
                    ("center", video_size[1] - background_size[1] - move_up_pixels)
                ),
                subtitle_text.set_position(
                    ("center", video_size[1] - text_size[1] - move_up_pixels)
                ),
            ],
            size=video_size,
        )
        .set_start(start_time)
        .set_end(end_time)
    )

    subtitle.fps = fps  # Set the FPS attribute for the subtitle clip

    return subtitle


def add_subtitles_to_video(video, subtitle_timings, subtitle_clips):
    video_size = video.size

    final_video = CompositeVideoClip([video] + subtitle_clips)
    return final_video

@celery.task(bind=True)
def process_results(self, data):
    # Initialize the subtitle_timings list and the current_time
    subtitle_timings = []
    current_time = 0
    chunks = data.get('chunks')
    print("HERE IS DATA", data, "HERE IS CHUNKS", chunks)

    # Create a group of tasks
    tasks = [synthesize_speech.s({'refined_script': chunk}) for chunk in chunks]

    # Apply the group and get the results
    results = group(*tasks).apply_async().get()

    # Return the results
    return results


@celery.task(bind=True)
def process_synthesized_speech(self, results):
    subtitle_timings = []
    current_time = 0
    chunks = []
    print(f"Results: {results}, type: {type(results)}")
    # Iterate over the results
    for result in results:
        # Extract the audioBase64 and chunk from the result
        audio_base64 = result.get('audioBase64')
        chunk = result.get('refined_script')

        chunks.append(chunk)
        # Decode the base64 string back into bytes
        if audio_base64 is not None:
            audio_bytes = base64.b64decode(audio_base64)
            audio_data = BytesIO(audio_bytes)
        else:
            # Handle the case when audio_base64 is None
            # For example, you can raise an error or return from the function
            raise ValueError("audioBase64 is None")

        # Get the duration of the audio
        duration = get_audio_duration(audio_data)

        # Calculate the end_time
        end_time = current_time + duration

        # Append the current_time, end_time, and chunk to the subtitle_timings list
        subtitle_timings.append([current_time, end_time, chunk])

        # Update the current_time
        current_time = end_time

    # Return the subtitle_timings
    print("Chunks, In Synth", chunks)
    return {
        'subtitle_timings': subtitle_timings,
        'chunks': chunks,
        'audioBase64': audio_base64
    }

@celery.task(bind=True)
def create_video(self, result_of_previous_task):
    video_size = (1280, 720)
    data = result_of_previous_task.get('data')
    image_urls = result_of_previous_task.get('image_urls')
    audio_base64 = data.get('audioBase64')
    generated_text = data.get('refined_script')
    show_subtitles = data.get('showSubtitles')
    output_file = data.get('output_file')

    clips = []
    print("HERE IS GENERATED TEXT:", generated_text)
    sentences = split_sentences(generated_text)

    from utils.subtitle_utils import generate_subtitle_timings
    subtitle_timings = generate_subtitle_timings.delay(sentences).get()

    background = Image.new("RGB", (1280, 720), color="black")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        images = list(executor.map(download_and_resize_image, image_urls))

    total_images = len(images)
    for i, image in enumerate(images):
        # Update the task's progress
        self.update_state(state="PROGRESS", meta={"current": i, "total": total_images})

        img_bg = background.copy()
        img_bg.paste(
            image,
            (
                int((background.width - image.width) / 2),
                int((background.height - image.height) / 2),
            ),
        )
        img_bg_clip = mp.ImageClip(np.array(img_bg)).set_duration(5)
        clips.append(img_bg_clip)

    concatenated_clip = mp.concatenate_videoclips(clips)

    print(f"show_subtitles: {show_subtitles}") 

    if show_subtitles:
        print(
            "Creating subtitle clips"
        )  # Debug message to indicate subtitles are being created
        subtitle_clips = [
            create_subtitle_clip(text, start, end, video_size, show_subtitles)
            for start, end, text in subtitle_timings
        ]
        final_clip = add_subtitles_to_video(
            concatenated_clip, subtitle_timings, subtitle_clips
        )
    else:
        print(
            "Skipping subtitle clips"
        )  # Debug message to indicate subtitles are being skipped
        final_clip = concatenated_clip

    temp_dir = Path(__file__).resolve().parent / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    audio_data = base64.b64decode(audio_base64)
    audio_temp_file = temp_dir / "temp_audio.wav"
    with open(audio_temp_file, "wb") as f:
        f.write(audio_data)
        
    audioclip = mp.AudioFileClip(str(audio_temp_file))

    final_clip = final_clip.set_audio(audioclip)

    output_path = temp_dir / "video.mp4"

    temp_audio_path = temp_dir / "temp_audio.m4a"
    final_clip.write_videofile(
        str(output_path),
        temp_audiofile=str(temp_audio_path),
        remove_temp=False,
        audio_codec="aac",
        fps=24,
        threads=12,
        ffmpeg_params=[
            "-preset",
            "fast",
            "-b:v",
            "10M",
        ],
    )

    with open(output_path, "rb") as f:
        video_data = f.read()

    if audio_temp_file.exists():
        audio_temp_file.unlink()

    if temp_audio_path.exists():
        temp_audio_path.unlink()

    # Save the video to AWS S3
    object_name ="video.mp4"
    s3_video_url = upload_to_s3(output_file, object_name)

    # Remove the temporary output file
    os.remove(Path(output_file))

    # Return the video URL
    return s3_video_url