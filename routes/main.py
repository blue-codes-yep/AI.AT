import os
import base64
import json
from pathlib import Path
from collections import deque
from llm import (
    run_all_chains,
    search,
)

from flask import (
    Blueprint,
    request,
    jsonify,
)

from utils import (
    synthesize_speech,
    create_video,
    upload_to_s3,
    get_unsplash_image_urls,
    long_task,
)

main_bp = Blueprint("main", __name__)

# Define the temporary directory path
temp_dir = os.path.join(os.path.dirname(__file__), "utils", "temp")


# Message history
message_history = deque(maxlen=15)


@main_bp.route("/api", methods=["POST"])
def index():
    data = request.json
    prompt = data.get("prompt")

    # Run the chain with the prompt
    google_search_result = search.run(prompt)

    # Call the run_all_chains function
    chain_outputs = run_all_chains(prompt, google_search_result)

    # Get image results
    image_results = get_unsplash_image_urls(prompt)

    # Save the response to the message history
    message_history.append(chain_outputs)

    message_history_list = list(message_history)

    response = {
        "generated_text": {
            "script": chain_outputs["script"],
            "adjusted": chain_outputs["adjusted_script"],
            "refine": chain_outputs["refined_script"],
        },
        "image_results": image_results,
        "message_history": message_history_list,
    }

    return json.dumps(response)


@main_bp.route("/api/tts", methods=["POST"])
def tts():
    if request.method == "POST":
        print("Inside /api/tts route")
        data = request.json
        text = data["text"]
        print("Refined Text:", text)
        if text is None:
            return jsonify({"error": "No text provided"}), 400

        audio_base64 = generate_audio_base64(text)
        return jsonify({"audio_base64": audio_base64})


def generate_audio_base64(text):
    audio = synthesize_speech(text)
    raw_data = audio.read()
    audio_base64 = base64.b64encode(raw_data).decode("utf-8")
    return audio_base64


@main_bp.route("/api/video", methods=["POST"])
def create_video_endpoint():
    data = request.get_json()
    image_urls = data["image_results"]
    audio_base64 = data["audioBase64"]
    text = data["generatedText"]["refine"]
    show_subtitles = data.get("showSubtitles")
    print(show_subtitles)
    # Call the create_video function
    output_path = Path("/home/blue/AiProj/AI.AT/utils/temp")
    output_file = output_path / "video.mp4"

    create_video(image_urls, audio_base64, text, show_subtitles, output_file)

    # Save the video to AWS S3
    object_name = "video.mp4"
    s3_video_url = upload_to_s3(output_file, object_name)

    # Remove the temporary output file
    os.remove(output_file)

    # Return the video URL in the response
    return jsonify({"video_url": s3_video_url})

@main_bp.route('/task-status/<task_id>')
def task_status(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
        }
    else:
        response = {'state': task.state, 'result': task.result}
    return jsonify(response)

@main_bp.route('/start-task', methods=['GET'])
def start_task():
    task = long_task.apply_async()
    return jsonify({'task_id': task.id}), 202