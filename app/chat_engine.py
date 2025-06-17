# app/chat_engine.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def ask_bizzy(system_prompt: str, user_message: str, model="gpt-4o") -> str:
    response = client.responses.create(
        model=model,
        instructions = system_prompt, #providing prompt we set up
        input = user_message, #passing the message to bizzy from the client
        temperature=0.7
    )
    return response.output_text

