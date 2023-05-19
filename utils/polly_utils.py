import boto3
import base64
from apikey import aws_access_key, aws_secret_key, aws_region
from pydub import AudioSegment
from pathlib import Path
from io import BytesIO
from .progress_utils import celery

temp_dir = Path(__file__).parent / "temp"
temp_dir.mkdir(parents=True, exist_ok=True)

polly_client = boto3.client(
    "polly",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)

@celery.task(bind=True)
def synthesize_speech(self, result_of_previous_task):
    text = result_of_previous_task['refined_script']
    print(f"synthesize_speech input: {result_of_previous_task}")
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="pcm", VoiceId="Joanna"
    )

    # Save the synthesized speech to a BytesIO object
    audio_data = BytesIO(response["AudioStream"].read())

    # Load the audio data with PyDub
    audio = AudioSegment.from_file(
        audio_data, format="raw", frame_rate=16000, channels=1, sample_width=2
    )

    # Convert the audio to WAV format and save it to a BytesIO object
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)

    # Convert the BytesIO object to a base64-encoded string
    audio_base64 = base64.b64encode(buffer.getvalue()).decode()

    self.update_state(state="PROGRESS", meta={"current": 50, "total": 100})

    
    print(f"synthesize_speech output: {audio_base64}")
    # Return the base64-encoded string
    return {'audioBase64': audio_base64, 'refined_script': text}

