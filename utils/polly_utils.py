import boto3
from apikey import aws_access_key, aws_secret_key, aws_region
from pydub import AudioSegment
from pathlib import Path
from io import BytesIO

temp_dir = Path(__file__).parent / "temp"
temp_dir.mkdir(parents=True, exist_ok=True)

polly_client = boto3.client(
    "polly",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)


def synthesize_speech(text):
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="pcm", VoiceId="Joanna"
    )

    # Save the synthesized speech to a BytesIO object
    audio_data = BytesIO(response["AudioStream"].read())

    # Load the audio data with PyDub
    audio = AudioSegment.from_file(
        audio_data, format="raw", frame_rate=16000, channels=1, sample_width=2
    )

    # Convert the audio to WAV format and return it
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)

    return buffer
