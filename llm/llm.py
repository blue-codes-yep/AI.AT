from langchain.llms import OpenAI
from apikey import (
    apikey,
    google_search,
    google_cse,
    serp,
    aws_access_key,
    aws_secret_key,
    aws_region,
)
import os
from typing import Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper

os.environ["OPENAI_API_KEY"] = apikey
os.environ["GOOGLE_API_KEY"] = google_search
os.environ["GOOGLE_CSE_ID"] = google_cse
os.environ["SERPAPI_API_KEY"] = serp
os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
os.environ["AWS_DEFAULT_REGION"] = aws_region

# LLMs
llm = OpenAI(temperature=0.8, max_tokens=2048)

# Memory
conv_memory = ConversationBufferMemory()


# Prompt template for LLM
script_template = PromptTemplate(
    input_variables=["topic", "google_search"],
    template="Write me a YouTube voiceover script about {topic}, and also do research about the topic on Google. {google_search}",
)

adjust_template = PromptTemplate(
    input_variables=["script"],
    template="Edit, and adjust the script in a fun, relaxed way: {script}\n\n-=-=-=- Adjusted Script -=-=-=-",
)

# Add a new prompt template for further adjustments
refine_template = PromptTemplate(
    input_variables=[
        "script",
        "adjusted_script",
    ],
    template="Refine the adjusted script staying on topic to make it more charismatic:\n{script}\n\n-=-=-=- Adjusted Script -=-=-=-\n{adjusted_script}\n\n-=-=-=- Refined Script -=-=-=-",
)

# LLM Chains
script_chain = LLMChain(
    llm=llm, prompt=script_template, verbose=True, output_key="script"
)
adjust_chain = LLMChain(
    llm=llm, prompt=adjust_template, verbose=True, output_key="adjusted_script"
)
refine_chain = LLMChain(
    llm=llm, prompt=refine_template, verbose=True, output_key="refined_script"
)

search = GoogleSearchAPIWrapper()


def run_all_chains(prompt: str, google_search_result: str) -> Dict[str, str]:
    script = script_chain({"topic": prompt, "google_search": google_search_result})
    conv_memory.save_context(
        {"topic": prompt}, {"script": script[script_chain.output_key]}
    )
    print("Script chain output:", script)

    adjust = adjust_chain({"script": script[script_chain.output_key]})
    conv_memory.save_context(
        {"script": script[script_chain.output_key]},
        {"adjusted_script": adjust[adjust_chain.output_key]},
    )
    print("Adjust chain output:", adjust)
    adjust_output = adjust[adjust_chain.output_key]
    adjusted_script = adjust_output.split("-=-=-=- Adjusted Script -=-=-=-")[-1].strip()

    refine = refine_chain(
        {
            "script": script[script_chain.output_key],
            "adjusted_script": adjust[adjust_chain.output_key],
        }
    )
    conv_memory.save_context(
        {"adjusted_script": adjust[adjust_chain.output_key]},
        {"refined_script": refine[refine_chain.output_key]},
    )
    print("Refine chain output:", refine)

    refine_output = refine[refine_chain.output_key]
    refined_script = refine_output.split("-=-=-=- Refined Script -=-=-=-")[-1].strip()

    return {
        "script": script[script_chain.output_key],
        "adjusted_script": adjusted_script,
        "refined_script": refined_script,
    }
