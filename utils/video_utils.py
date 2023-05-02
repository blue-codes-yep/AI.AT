import os
import moviepy.editor as mp
from moviepy.editor import TextClip, CompositeVideoClip
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

def create_video(image_urls, audio_base64, script, output_file):
    clips = []
    sentences = split_sentences(script)
    subtitle_timings = generate_subtitle_timings(sentences, synthesize_speech)
    
    background = Image.new('RGB', (1280, 720), color='black')
    
    for url in image_urls:
        print(f"Processing image: {url['thumbnail']}")
        image_data = url['thumbnail']
        response = requests.get(image_data)
        image = Image.open(BytesIO(response.content))
        image = resize_image(image, width=1280, height=720)
        img_bg = background.copy()
        img_bg.paste(image, (int((background.width - image.width) / 2), int((background.height - image.height) / 2)))
        img_bg_clip = mp.ImageClip(np.array(img_bg)).set_duration(5)
        clips.append(img_bg_clip)

    concatenated_clip = mp.concatenate_videoclips(clips)


    subtitle_clips = []
    for start, end, sentence in subtitle_timings:
        if not sentence.strip():  # skip empty sentences
            continue

        print(f"Creating subtitle clip: start={start}, end={end}, sentence={sentence}")
        subtitle_clip = TextClip(
            sentence,
            fontsize=24,
            color='white',
            size=(concatenated_clip.w, 100),
            bg_color='black',
            print_cmd=True
        ).set_position(('center', 'bottom')).set_start(start).set_end(end)
        subtitle_clips.append(subtitle_clip)

    subtitles = CompositeVideoClip(subtitle_clips)
    composite_clip = CompositeVideoClip([concatenated_clip, subtitles])

    temp_dir = Path(__file__).resolve().parent / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)

    audio_data = base64.b64decode(audio_base64)
    audio_temp_file = temp_dir / 'temp_audio.wav'
    with open(audio_temp_file, 'wb') as f:
        f.write(audio_data)

    audioclip = mp.AudioFileClip(str(audio_temp_file))

    final_clip = composite_clip.set_audio(audioclip)

    output_path = temp_dir / 'video.mp4'

    temp_audio_path = temp_dir / 'temp_audio.m4a'
    final_clip.write_videofile(str(output_path), codec='libx264', temp_audiofile=str(temp_audio_path), remove_temp=False, audio_codec='aac', fps=24)

    with open(output_file, 'rb') as f:
        video_data = f.read()

    if audio_temp_file.exists():
        audio_temp_file.unlink()

    if temp_audio_path.exists():
        temp_audio_path.unlink()

    return video_data
