import spacy
from pydub import AudioSegment
from utils.polly_utils import synthesize_speech
from io import BytesIO


nlp = spacy.load("en_core_web_sm")

def split_text_into_chunks(result_of_previous_task, max_length):
    text = result_of_previous_task.get('refined_script')
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    chunks.append(' '.join(current_chunk))
    return chunks

def split_sentences(result_of_previous_task):
    text = result_of_previous_task.get('refined_script')
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def get_audio_duration(audio_data: BytesIO):
    audio_data.seek(0)
    audio = AudioSegment.from_file(audio_data, format="wav")
    return len(audio) / 1000

def generate_subtitle_timings(sentences, synthesize_speech, max_chunk_length=45):
    timings = []
    current_time = 0

    for sentence in sentences:
        chunks = split_text_into_chunks(sentence, max_chunk_length)
        for chunk in chunks:
            audio_data = synthesize_speech(chunk)
            duration = get_audio_duration(audio_data)
            end_time = current_time + duration
            timings.append([current_time, end_time, chunk])
            current_time = end_time

    return timings
