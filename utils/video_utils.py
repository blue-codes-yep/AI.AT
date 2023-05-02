import moviepy.editor as mp
import requests
import base64
import imageio
import tempfile
import os
from moviepy.video.fx.all import resize
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from io import BytesIO
from pathlib import Path
from .s3_utils import upload_to_s3

def create_video(image_urls, audio_base64, text, output_file):
    """Creates a video from a list of image URLs, an audio file, and some text.

    Args:
        image_urls: A list of image URLs.
        audio_base64: The audio file as a base64-encoded string.
        text: The text to be displayed on the video.
        output_file: The name of the output file.

    Returns:
        The video as a array buffer.
    """

    clips = []

    # Download and process images
    for url in image_urls:
        image_data = url['thumbnail']
        response = requests.get(image_data)
        image = mp.ImageClip(imageio.imread(response.content))
        image = resize(image, width=1280)
        clips.append(image.set_duration(5))

    # Concatenate images
    concatenated_clip = mp.concatenate_videoclips(clips)

    # Create subtitles
    subtitles = TextClip(
        text,
        fontsize=24,
        color='white',
        size=(concatenated_clip.w, 100),
        bg_color='black',
        print_cmd=True
    ).set_position(('center', 'bottom')).set_duration(concatenated_clip.duration)

    # Create composite clip
    composite_clip = CompositeVideoClip([concatenated_clip, subtitles])

    temp_dir = Path(__file__).resolve().parent / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Save audio_base64 content to a temporary file
    audio_data = base64.b64decode(audio_base64)
    audio_temp_file = temp_dir / 'temp_audio.wav'
    with open(audio_temp_file, 'wb') as f:
        f.write(audio_data)

    # Use the temporary file path for mp.AudioFileClip
    audioclip = mp.AudioFileClip(str(audio_temp_file))

    # Set the audio for the composite clip
    final_clip = composite_clip.set_audio(audioclip)

    # Get the absolute path to the output file
    output_path = temp_dir / 'video.mp4'

    # Write the video to the specified output file
    temp_audio_path = temp_dir / 'temp_audio.m4a'
    final_clip.write_videofile(str(output_path), codec='libx265', temp_audiofile=str(temp_audio_path), remove_temp=False, audio_codec='aac', fps=24)


    # Read the video file as an ArrayBuffer
    with open(output_file, 'rb') as f:
        video_data = f.read()

    # Remove the temporary audio file
    if audio_temp_file.exists():
        audio_temp_file.unlink()

    if temp_audio_path.exists():
        temp_audio_path.unlink()



    return video_data