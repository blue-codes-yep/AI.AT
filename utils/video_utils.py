import moviepy.editor as mp
import concurrent.futures
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter
from moviepy.video.fx.resize import resize
import requests
from io import BytesIO
from PIL import Image
import base64
import numpy as np
from pathlib import Path
from utils.subtitle_utils import split_sentences, generate_subtitle_timings
from utils.polly_utils import synthesize_speech


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
    image_data = url["thumbnail"]
    response = requests.get(image_data)
    image = Image.open(BytesIO(response.content))
    image = resize_image(image, width=1280, height=720)
    return image


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
        stroke_width=0.3,  # Increase the stroke_width for better edge contrast
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


def create_video(image_urls, audio_base64, script, output_file):
    clips = []
    sentences = split_sentences(script)
    subtitle_timings = generate_subtitle_timings(sentences, synthesize_speech)
    background = Image.new("RGB", (1280, 720), color="black")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        images = list(executor.map(download_and_resize_image, image_urls))

    for image in images:
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

    subtitle_clips = [
        create_subtitle_clip(text, start, end, concatenated_clip.size)
        for start, end, text in subtitle_timings
    ]

    final_clip = add_subtitles_to_video(
        concatenated_clip, subtitle_timings, subtitle_clips
    )

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
        codec="libx264",
        temp_audiofile=str(temp_audio_path),
        remove_temp=False,
        audio_codec="aac",
        fps=24,
        threads=8,
        ffmpeg_params=[
            "-preset",
            "fast",
            "-profile:v",
            "main",  # Add the profile
            "-level:v",
            "4.0",  # Add the level
        ],
    )
    with open(output_path, "rb") as f:
        video_data = f.read()

    if audio_temp_file.exists():
        audio_temp_file.unlink()

    if temp_audio_path.exists():
        temp_audio_path.unlink()

    return video_data
