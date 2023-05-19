import spacy
from pydub import AudioSegment
from utils.polly_utils import synthesize_speech
from io import BytesIO
from celery import group
from celery import chord
from celery import current_app as celery

nlp = spacy.load("en_core_web_sm")

def split_text_into_chunks(text, max_chunk_length):
    words = text.split()
    chunks = []
    current_chunk = ''

    for word in words:
        if len(current_chunk) + len(word) <= max_chunk_length:
            current_chunk += ' ' + word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    chunks.append(current_chunk)

    return chunks


def split_sentences(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences


def get_audio_duration(audio_data: BytesIO):
    audio_data.seek(0)
    audio = AudioSegment.from_file(audio_data, format="wav")
    return len(audio) / 1000

@celery.task
def generate_subtitle_timings(result_of_previous_task, max_chunk_length=45):
    # Import synthesize_speech here
    from utils import synthesize_speech

    # Extract the audio_base64 value from the input
    audio_base64 = result_of_previous_task['audioBase64']

    # Create a list of chunks and a group of tasks to synthesize speech for all chunks
    sentences = result_of_previous_task['refined_script'].split('.')
    chunks = [chunk for sentence in sentences for chunk in split_text_into_chunks(sentence, max_chunk_length)]
    tasks = [synthesize_speech.s({'refined_script': chunk}) for chunk in chunks]

    # Return the chunks, tasks, and audio_base64
    return {'chunks': chunks, 'tasks': tasks, 'audioBase64': audio_base64}
