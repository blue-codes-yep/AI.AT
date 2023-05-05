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
from typing import Dict, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper


os.environ["OPENAI_API_KEY"] = apikey
os.environ["GOOGLE_API_KEY"] = google_search
os.environ["GOOGLE_CSE_ID"] = google_cse
os.environ["SERPAPI_API_KEY"] = serp
os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
os.environ["AWS_DEFAULT_REGION"] = aws_region

from typing import Dict, Optional
from langchain.memory import ConversationBufferMemory


from typing import Dict, Optional
from langchain.memory import ConversationBufferMemory


class CustomConversationBufferMemory(ConversationBufferMemory):
    input_key_mapping: Optional[Dict[str, str]] = None

    def _get_input_output(self, inputs, outputs):
        prompt_input_key = (
            self.input_key_mapping.get(self.input_key, self.input_key)
            if self.input_key_mapping
            else self.input_key
        )
        output_key = self.output_key or self.input_key

        input_str = inputs.get(prompt_input_key, None)
        output_str = outputs.get(output_key, None)

        if input_str is None or output_str is None:
            return None, None

        return input_str, output_str

    def save_context(self, inputs, outputs, message_type="ai"):
        input_str, output_str = self._get_input_output(inputs, outputs)
        if input_str is None or output_str is None:
            print(
                f"KeyError occurred when trying to save context with inputs: {inputs}, outputs: {outputs}"
            )
        else:
            if message_type == "ai":
                self.chat_memory.add_ai_message(output_str)
            elif message_type == "user":
                self.chat_memory.add_user_message(input_str)


# Memory
script_memory = ConversationBufferMemory(input_key="topic", memory_key="chat_history")

adjust_memory = ConversationBufferMemory(input_key="script", memory_key="chat_history")

combined_memory = CustomConversationBufferMemory(
    input_key="adjusted_script",
    memory_key="chat_history",
    input_key_mapping={"adjusted_script": "script"},
)

refine_memory = CustomConversationBufferMemory(
    input_key="refined_script",
    memory_key="chat_history",
    input_key_mapping={"refined_script": "adjusted_script"},
)

print(combined_memory.buffer)

# LLMs
llm = OpenAI(temperature=0.4, max_tokens=2048)

# Prompt template for LLM
script_template = PromptTemplate(
    input_variables=["topic", "google_search"],
    template="Write me a YouTube voiceover script about {topic}, and also do research about the topic on Google. {google_search}",
)

adjust_template = PromptTemplate(
    input_variables=["script"],
    template="Edit, and adjust the script in a fun, relaxed way: {script}",
)

# Add a new prompt template for further adjustments
refine_template = PromptTemplate(
    input_variables=[
        "adjusted_script",
    ],
    template="Refine the adjusted script staying on topic to make it more charismatic: {adjusted_script}",
)

script_chain = LLMChain(
    llm=llm,
    prompt=script_template,
    verbose=True,
    output_key="script",
    memory=script_memory,
)

adjust_chain = LLMChain(
    llm=llm,
    prompt=adjust_template,
    verbose=True,
    output_key="adjusted_script",
    memory=adjust_memory,
)

refine_chain = LLMChain(
    llm=llm,
    prompt=refine_template,
    verbose=True,
    output_key="refined_script",
    memory=refine_memory,
)

search = GoogleSearchAPIWrapper()
