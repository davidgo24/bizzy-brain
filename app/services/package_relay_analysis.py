import os
import json
from datetime import datetime
from app.services.owner_loop import handle_owner_relay_response
from app.services.ticket_id_generator import generate_ticket_id


def log_relay_event(phone_number, relay_result, thread):
    # Ensure relay_logs folder exists
    os.makedirs("relay_logs", exist_ok=True)
    ticket_id = generate_ticket_id(phone_number)

    file_path = os.path.join("relay_logs", f"{ticket_id}.json")

    # Create a timestamped filename
    timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '-')
    file_name = f"{phone_number}__{timestamp}.json"
    path = os.path.join("relay_logs", file_name)


    # Extract relay metadata
    intent = relay_result.get("intent", "unknown")
    sensitivity = relay_result.get("sensitivity", 0)
    reason = relay_result.get("reason", "No reason provided.")

    # Package payload
    payload = {
        "ticket_id": ticket_id,
        "phone_number": phone_number,
        "timestamp": timestamp,
        "sensitivity": sensitivity,
        "intent": intent,
        "reason": reason,
        "thread": thread
    }

    # Save payload to file
    with open(path, 'w') as f:
        json.dump(payload, f, indent=2)

    # Generate summary alert
    summary = (
        f"\n📤 [Bizzy ➡️ Melissa — New Ticket: {ticket_id}]\n"
        f"\nTime: {timestamp}\n"
        f"Client needs your input:\n"
        f"- Intent: {intent}\n"
        f"- Reason: {reason}\n"
        f"- Sensitivity: {sensitivity}"
    )
    # Mock owner notification
    print(summary)

    # Trigger owner response loop (via console for now)
    if sensitivity >= 8:
        handle_owner_relay_response(ticket_id, phone_number, relay_result)




def notify_owner(summary: str):
    print(f"\n📤 Notifying Melissa:\n{summary}\n")
    