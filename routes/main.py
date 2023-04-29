from flask import Blueprint, render_template, request
import os
from apikey import apikey
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

main_bp = Blueprint('main', __name__)

os.environ["OPENAI_API_KEY"] = apikey

# Prompt template for LLM
script_template = PromptTemplate(
    input_variables=['topic'],
    template='Write me a YouTube voiceover script about {topic}.',
)

adjust_template = PromptTemplate(
    input_variables=['script'],
    template='Adjust the script in a fun, relaxed way: {script}',
)

# LLMs
llm = OpenAI(temperature=0.1)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script')
adjust_chain = LLMChain(llm=llm, prompt=adjust_template, verbose=True, output_key='adjust')
sequential_chain = SequentialChain(chains=[script_chain, adjust_chain], input_variables=['topic'], output_variables=['script', 'adjust'], verbose=True)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')

        # Run the chain with the prompt
        response = sequential_chain({'topic': prompt})  # Use 'topic' as the key
        print(response['script'])  # Log the response to the console
        print(response['adjust']) 
        return render_template('index.html', generated_text=response)
    else:
        return render_template('index.html')