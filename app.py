import os
from apikey import apikey
from langchain.llms import OpenAI
from flask import Flask
from routes.main import main_bp

os.environ["OPENAI_API_KEY"] = apikey

app = Flask(__name__)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run()

