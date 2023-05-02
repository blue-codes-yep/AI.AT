import os
import base64
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, send_from_directory, make_response
from apikey import apikey, google_search, google_cse, serp, aws_access_key, aws_secret_key, aws_region
from collections import deque
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper
from utils import get_image_results, synthesize_speech, create_video, upload_to_s3
from pydub.playback import play
from io import BytesIO

main_bp = Blueprint('main', __name__)

import os

# Define the temporary directory path
temp_dir = os.path.join(os.path.dirname(__file__), 'utils', 'temp')


os.environ["OPENAI_API_KEY"] = apikey
os.environ["GOOGLE_API_KEY"] = google_search
os.environ["GOOGLE_CSE_ID"] = google_cse
os.environ["SERPAPI_API_KEY"] = serp
os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
os.environ["AWS_DEFAULT_REGION"] = aws_region



# Prompt template for LLM
script_template = PromptTemplate(
    input_variables=['topic', 'google_search'],
    template='Write me a YouTube voiceover script about {topic}, and also do research about the topic on Google. {google_search}'
)

adjust_template = PromptTemplate(
    input_variables=['script'],
    template='Edit, and ajdust the script in a fun, relaxed way: {script}'
)

# Memory
script_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
adjust_memory = ConversationBufferMemory(input_key='script', memory_key='chat_history')

# LLMs
llm = OpenAI(temperature=0.1)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)
adjust_chain = LLMChain(llm=llm, prompt=adjust_template, verbose=True, output_key='adjust', memory=adjust_memory)


# Message history
message_history = deque(maxlen=10)


# Google Search
search = GoogleSearchAPIWrapper()


@main_bp.route('/api', methods=['POST'])
def index():
    data = request.get_json()
    prompt = data.get('prompt')

    # Run the chain with the prompt
    google_search_result = search.run(prompt)
    script = script_chain({'topic': prompt, 'google_search': google_search_result})
    adjust = adjust_chain({'script': script['script']})

    # Get image results
    image_results = get_image_results(prompt)

    # Save the response to the message history
    message_history.append({'script': script_memory.buffer, 'adjust': adjust_memory.buffer})

    response = {
        'generated_text': {
            'script': adjust['script'],
            'adjust': adjust['adjust'],
        },
        'message_history': list(message_history),
        'image_results': image_results,
    }

    return jsonify(response)

@main_bp.route('/api/tts', methods=['POST'])
def tts():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
        audio_base64 = generate_audio_base64(text)
        return jsonify({'audio_base64': audio_base64})

def generate_audio_base64(text):
    audio = synthesize_speech(text)
    raw_data = audio.read()
    audio_base64 = base64.b64encode(raw_data).decode('utf-8')
    return audio_base64

@main_bp.route('/api/video', methods=['POST'])
def create_video_endpoint():
    data = request.get_json()
    image_urls = data['imageResults']
    audio_base64 = data['audioBase64']
    text = data['generatedText']

    # Call the create_video function
    output_path = Path("G:/AI Application/utils/temp")
    output_file = output_path / 'video.mp4'

    create_video(image_urls, audio_base64, text, output_file)

    # Save the video to AWS S3
    object_name = f"{output_file}"  # Adjust this to your preferred naming convention
    s3_video_url = upload_to_s3(output_file, object_name)

    # Upload the video to S3
    s3_video_url = upload_to_s3(str(output_file), f"videos/{output_file.name}")
    os.remove(output_file)  
    print("Output file:", output_file)
    print("S3 Video URL:", s3_video_url)
    # Return the video URL in the response
    return jsonify({'video_url': s3_video_url})