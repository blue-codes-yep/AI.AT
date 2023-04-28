from flask import Blueprint, render_template, request
import os
from apikey import apikey
from langchain.llms import OpenAI

main_bp = Blueprint('main', __name__)

os.environ["OPENAI_API_KEY"] = apikey

llm = OpenAI(temperature=0.9)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        generated_text = llm(prompt)
        return render_template('index.html', generated_text=generated_text)
    else:
        return render_template('index.html')
