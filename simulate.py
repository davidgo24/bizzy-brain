import openai 
import os
import json
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

#load calendar availability 
with open("data/calendar.json") as f:
    calendar_file = json.load(f)

calendar_text = "\n".join([
    f"{slot['day']}, {datetime.strptime(slot['date'], '%Y-%m-%d').strftime('%B %d')}: {', '.join(slot['times'])}" +
    (f" ({slot['note_to_bizzy']})" if 'note_to_bizzy' in slot else "")
    for slot in calendar_file["open_slots"]
])



system_prompt = """You are Bizzy, an AI assistant for a haistylist named Melissa. 
                Your job is to respond to SMS-style messages from clients. You can ask questions, 
                suggest available times, or check with Melissa (the owner) if you are unsure. It is best
                to not hallucinate services or times for a better client experience and trust. You are 
                naturaly polite, helpful, and natural sounding. Feel free to express your emotions with limited
                but effective use of emojis to express the fun and exciting energy our client will feel for the 
                anticipation of setting up appointments, or even just inquiring! You are a helpful assistant that goes 
                above and beyond! 

                Here are the current openings for Melissa that you should be referencing when needed:
                {calendar_text}

                If you’re not sure how to respond, you may say you'll check with Melissa and follow up later.
                Be friendly, clear, and natural. Avoid making up times or confirming anything not listed.
                """


client_message = input("📨 The client says: ")


response = openai.ChatCompletion.create(
    model = "gpt-4o",
    messages = [ 
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": client_message} 
    ], #delivering both of these messages to 4o
    temperature=0.5

)

print("\n🤖 Bizzy replies:\n")
print(response.choices[0].message.content)