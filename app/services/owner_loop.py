import os
import json
from datetime import datetime


def get_owner_thread(ticket_id):
    path = os.path.join("owner_memory", f"{ticket_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_owner_thread(ticket_id, thread):
    os.makedirs("owner_memory", exist_ok=True)
    path = os.path.join("owner_memory", f"{ticket_id}.json")
    with open(path, "w") as f:
        json.dump(thread, f, indent=2)

def handle_owner_relay_response(ticket_id, phone_number, relay_result):
    intent = relay_result.get("intent")
    reason = relay_result.get("reason")
    sensitivity = relay_result.get("sensitivity")

    print("\n📥 [Bizzy ➡️ Melissa]")
    print("Client needs your input:")
    print(f"-Intent: {intent}")
    print(f"- Reason: {reason}")
    print(f"-Sensitivity: {sensitivity}")

    thread = get_owner_thread(ticket_id)
    thread.append({
        "role": "assistant",
        "content": f"Hi Melissa, the client needs your input:\nIntent: {intent}\nReason: {reason}"
    })

    save_owner_thread(ticket_id, thread)

    should_reply = input("Reply to this ticket? (yes/no): ").strip().lower()

    if should_reply != "yes":
        print("❌ No reply given. Ticket remains open and I will not mark it closed until you reply 'close ticket' if you will take care of it'.")
        return 
    
    reply = input("✍️ Your message to the client: ").strip()

    thread.append({
        "role": "owner",
        "content": reply
    })

    save_owner_thread(ticket_id, thread) # we continuously update and save as the convo flows.

    print("✅ Melissa's reply has been saved and added to the thread.")

    