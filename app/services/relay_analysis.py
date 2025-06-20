from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_for_relay(message: str, thread: list) -> dict:
    context_snippet = "\n".join(
        [
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in thread[-5:]
        ])
    
    prompt = f"""
            You are Bizzy, a friendly AI assistant that helps manage conversations for a hairstylist named Melissa.
            Given the most recent client message and recent conversation context, determine:

            1. The **intent** of the message (e.g., booking_request, style_advice, policy_question, feedback, greeting).
            2. A **sensitivity score** from 0 to 10. The higher the score, the more likely Melissa (the owner) must intervene before replying.
            3. A short explanation of **why** you rated it this way.
            4. If the sensitivity is 8 or above, write a warm, natural-sounding response Bizzy should send while waiting for Melissa.

            Output format:
            ```json
            {{
            "intent": "...",
            "sensitivity": ..., 
            "reason": "...",
            "bizzy_response": "..."  // Optional. Only if sensitivity >= 8
            }}
            ```

            Recent thread:
            {context_snippet}

            Latest message:
            Client: {message}
            """
    
    response = client.responses.create(
        model="gpt-4o",
        instructions = prompt + "\n\nRespond ONLY with valid JSON. Do not include any explanation, markdown, or backticks.",
        input = message,
        temperature=0.6
    )
    
    try:
        raw_text = response.output_text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        result = json.loads(raw_text)
        return result
    

    except Exception as e:
        print("Error parsing GPT response:", e)
        print("Raw response was:", raw_text)
        return {
            "intent": "unknown",
            "sensitivity": 5,
           "reason": "Unable to parse GPT output.",
           "bizzy_response": "Let me check with Melissa and get back to you just to be safe! "
        }

