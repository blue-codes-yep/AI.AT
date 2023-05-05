import os
import base64
import json
from pathlib import Path
from collections import deque
from llm import (
    script_chain,
    adjust_chain,
    refine_chain,
    search,
    refine_chain,
    script_memory,
    adjust_memory,
    refine_memory,
    combined_memory,
)

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    send_from_directory,
    make_response,
)

from utils import (
    get_image_results,
    synthesize_speech,
    create_video,
    upload_to_s3,
    split_sentences,
    generate_subtitle_timings,
    get_unsplash_image_urls,
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
    # Run the chain with the prompt
    google_search_result = search.run(prompt)
    script = script_chain({"topic": prompt, "google_search": google_search_result})
    combined_memory.save_context(
        script, {script_chain.output_key: script[script_chain.output_key]}
    )
    adjust = adjust_chain({"script": script[script_chain.output_key]})
    print("Adjust Output:", adjust)

    combined_memory.save_context(
        adjust, {adjust_chain.output_key: adjust[adjust_chain.output_key]}
    )
    print("Combined Memory:", combined_memory.buffer)

    # Possibly change the input key for combined memory?
    refine = refine_chain({"adjusted_script": adjust[adjust_chain.output_key]})
    print("Refine Output:", refine)

    combined_memory.save_context(
        refine, {refine_chain.output_key: refine[refine_chain.output_key]}
    )
    print("Combined Memory after Refine:", combined_memory.buffer)

    refine_output = (
        refine[refine_chain.output_key]
        if refine[refine_chain.output_key]
        else refine_memory.buffer
    )

    print("Adjust:", adjust)
    print("Refine:", refine)
    print("Script Memory:", script_memory.buffer)
    print("Adjust Memory:", adjust_memory.buffer)
    print("Refine Memory:", refine_memory.buffer)
    # Get image results
    image_results = get_unsplash_image_urls(prompt)

    # Save the response to the message history
    message_history.append(
        {
            "script": script_memory.buffer,
            "adjust": adjust_memory.buffer,
            "refine": refine_memory.buffer,
        }
    )

    message_history_list = list(message_history)
    print("Message History:", message_history_list)

    response = {
        "generated_text": {
            "refine": refine_output,
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
    text = data["generatedText"][
        "refine"
    ]  # Extract the script text from the generatedText dictionary

    # Call the create_video function
    output_path = Path("G:/AI Application/utils/temp")
    output_file = output_path / "video.mp4"

    create_video(image_urls, audio_base64, text, output_file)

    # Save the video to AWS S3
    object_name = "video.mp4"  # Update with the correct S3 object key
    s3_video_url = upload_to_s3(output_file, object_name)

    # Remove the temporary output file
    os.remove(output_file)

    # Return the video URL in the response
    return jsonify({"video_url": s3_video_url})
