from flask import Blueprint, render_template, request
import os
from apikey import apikey, google_search, google_cse
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper
from collections import deque

main_bp = Blueprint('main', __name__)

os.environ["OPENAI_API_KEY"] = apikey
os.environ["GOOGLE_API_KEY"] = google_search
os.environ["GOOGLE_CSE_ID"] = google_cse

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

search = GoogleSearchAPIWrapper()

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')

        # Run the chain with the prompt
# Run the chain with the prompt
        google_search_result = search.run(prompt)
        script = script_chain({'topic': prompt, 'google_search': google_search_result})
        adjust = adjust_chain({'script': script['script']})

        print(script) 
        print(adjust) 
        
        # Save the response to the message history
        message_history.append({'script': script_memory.buffer, 'adjust': adjust_memory.buffer})
        
        return render_template('index.html', generated_text=adjust, message_history=message_history)
    else:
        return render_template('index.html', message_history=message_history)