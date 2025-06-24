# main.py

from app.chat_engine import ask_bizzy
from app.memory.client_memory import add_message, get_thread, reset_thread, archive_client_thread_if_needed
from app.services.relay_analysis import analyze_for_relay
from app.services.package_relay_analysis import log_relay_event
from fastapi import FastAPI
from app.background.scheduler import register_background_tasks
import time

app = FastAPI()
register_background_tasks(app)

def simulate_convo(phone_number):
    archived = archive_client_thread_if_needed(phone_number)
    if archived:
        print(f"[📦] Old thread for {phone_number} was archived before starting a new one.\n")
    
    print("---- New SMS Thread ----")

    while True:
        user_input = input("Client: ")
        #if user_input.lower() in ("quit", "exit"):
           # reset_thread(phone_number)
          #  break

        # Add client message
        add_message(phone_number, "user", user_input)

        # Get full message thread
        messages = get_thread(phone_number)

        relay_result = analyze_for_relay(user_input, messages)
        print("🔎 Relay Analysis:", relay_result)

        if relay_result["sensitivity"] >= 8:
            log_relay_event(phone_number, relay_result, messages)
            print(f"Bizzy: {relay_result['bizzy_response']}\n")
            add_message(phone_number, "assistant", relay_result["bizzy_response"])
            continue

        if not messages:
            print("⚠️ No messages in thread - skipping response.")
            continue

        thread_prompt = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages]
        )

        if not thread_prompt.strip():
            print("⚠️ Thread empty. Skipping GPT call.")
            continue

        system_prompt = "You are bizzy, a friendly AI assistant for a hairstylist. You are provided the authority to help clients select an appointment slot!"
        response = ask_bizzy(system_prompt, thread_prompt)

        # Add Bizzy response to thread
        add_message(phone_number, "assistant", response)
        
        print(f"Bizzy: {response}\n")
        time.sleep(0.2)

if __name__ == "__main__":
    simulate_convo("3234594057")
    
