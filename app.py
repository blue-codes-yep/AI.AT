import os
import redis
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from routes.main import main_bp
from apikey import apikey
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = apikey

app = Flask(__name__, static_folder="frontend/build", static_url_path="")
app.register_blueprint(main_bp)
CORS(app)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join("frontend/build", path)):
        return send_from_directory("frontend/build", path)
    else:
        return send_from_directory("frontend/build", "index.html")


if __name__ == '__main__':
    app.run()