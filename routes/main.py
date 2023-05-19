import os
import base64
import json
from pathlib import Path
from collections import deque
from celery import chain

from llm import (
    run_all_chains,
    search,
)

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from utils import (
    synthesize_speech,
    create_video,
    upload_to_s3,
    get_unsplash_image_urls,
    celery,
    process_results,
    generate_subtitle_timings,
    process_synthesized_speech,
)

main_bp = Blueprint("main", __name__)

# Define the temporary directory path
temp_dir = os.path.join(os.path.dirname(__file__), "utils", "temp")


# Message history
message_history = deque(maxlen=15)


@main_bp.route("/api/start", methods=["POST"])
def start():
    data = request.json
    prompt = data.get("prompt")

    # Define the output path
    output_path = Path("/home/blue/AiProj/AI.AT/utils/temp")
    output_file = str(output_path / "video.mp4") 

    # Get the required data for the tasks
    image_urls = data.get("image_results")
    audio_base64 = data.get("audioBase64")
    show_subtitles = data.get("showSubtitles")

    # Create a Celery chain that runs the tasks in sequence
    task_chain = chain(
        run_all_chains.s(prompt),
        synthesize_speech.s(),
        generate_subtitle_timings.s(max_chunk_length=45),
        process_results.s(),
        process_synthesized_speech.s(),
        create_video.s(output_file=output_file, show_subtitles=show_subtitles),
        upload_to_s3.s(),
    )

    # Start the chain
    task = task_chain.apply_async()

    # Return the task ID in the response
    return jsonify({'task_id': task.id}), 202


@main_bp.route("/api/status/<task_id>", methods=["GET"])
def status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING' or task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0) if task.info else 0,
            'total': task.info.get('total', 1) if task.info else 1,
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': str(task.result),  # convert result to string
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'error': str(task.result),  # convert Exception to string
        }
    else:
        response = {'state': task.state}
    return jsonify(response)
