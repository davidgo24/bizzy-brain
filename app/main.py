from fastapi import FastAPI
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.chat_engine import ask_bizzy
from app.memory.client_memory import (
    add_message,
    get_thread,
    reset_thread,
    archive_client_thread_if_needed,
    load_client_thread,
)
from app.services.relay_analysis import analyze_for_relay
from app.memory.owner_conversations.owner_relay import (
    create_relay_ticket,
    try_owner_response,
)
from app.background.scheduler import register_background_tasks
from app.memory.services.relay_followup import should_follow_up_with_owner
from app.memory.owner_conversations.relay_tracker import (
    has_open_ticket,
    owner_has_replied,
    get_active_ticket_path,
)

app = FastAPI()
register_background_tasks(app)

OWNER_PHONE = "melissa"


def simulate_convo(phone_number):
    print("\U0001f9cd MEMORY_DIR resolved to: /Users/david/workspace/github.com/davidgo24/bizzy-brain/app/active_convos/client_msgs")
    now = datetime.now(ZoneInfo("America/Los_Angeles"))
    print(f"🕰️ Local time: {now.strftime('%Y-%m-%d %I:%M %p')}")

    archived = archive_client_thread_if_needed(phone_number)
    if archived:
        print(f"[\ud83d\udcc6] Old thread for {phone_number} was archived before starting a new one.\n")

    thread = load_client_thread(phone_number)
    if not thread or not thread.get("messages"):
        print(f"❌ No memory file or empty message history for {phone_number}")
    else:
        last_ts = thread["messages"][-1].get("timestamp")
        if last_ts:
            last_dt = datetime.fromisoformat(last_ts).astimezone(ZoneInfo("America/Los_Angeles"))
            expire_dt = last_dt + timedelta(days=14)
            print(f"\ud83d\udd50 {phone_number} | Last: {last_dt} | Expires after: {expire_dt}")

    print("---- New SMS Thread ----")

    while True:
        user_input = input("Client: ")
        add_message(phone_number, "user", user_input)

        messages = get_thread(phone_number)
        relay_result = analyze_for_relay(user_input, messages)
        print("🔎 Relay Analysis:", relay_result)

        if relay_result["sensitivity"] >= 7 and not has_open_ticket(phone_number):
            pause_msg = "This sounds important — I'm going to loop Melissa in to make sure we get this just right. Sit tight and we'll follow up shortly!"
            add_message(phone_number, "assistant", pause_msg)
            print(f"Bizzy: {pause_msg}\n")

            ticket_path = create_relay_ticket(
                owner_phone=OWNER_PHONE,
                client_phone=phone_number,
                thread=load_client_thread(phone_number),
                reason=relay_result["reason"],
                sensitivity=relay_result["sensitivity"],
                owner_summary=relay_result.get("owner_summary", "")
            )

            owner_reply = try_owner_response(ticket_path)
            if owner_reply:
                add_message(phone_number, "owner", owner_reply)

                full_thread = get_thread(phone_number)
                thread_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in full_thread])
                system_prompt = "You are Bizzy, a helpful assistant relaying Melissa's input to her client."

                response = ask_bizzy(system_prompt, thread_prompt)
                add_message(phone_number, "assistant", response)
                print(f"Bizzy: {response}\n")
            else:
                print("🟡 Melissa didn’t reply now. Ticket remains open.")
            continue

        # 🧠 GPT follow-up check for open tickets
        if has_open_ticket(phone_number) and owner_has_replied(phone_number):
            thread = load_client_thread(phone_number)
            messages = thread.get("messages", [])
            if not messages:
                print("⚠️ Thread empty. Skipping follow-up.")
                continue

            latest_msg = messages[-1]["content"]

            try:
                if should_follow_up_with_owner(thread, latest_msg):
                    print("📣 GPT suggests Melissa may want to follow up again.")

                    ticket_path = get_active_ticket_path(OWNER_PHONE, phone_number)
                    if ticket_path:
                        owner_reply = try_owner_response(ticket_path)
                        if owner_reply:
                            add_message(phone_number, "owner", owner_reply)

                            full_thread = get_thread(phone_number)
                            thread_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in full_thread])
                            system_prompt = "You are Bizzy, a helpful assistant relaying Melissa's input to her client."

                            response = ask_bizzy(system_prompt, thread_prompt)
                            add_message(phone_number, "assistant", response)
                            print(f"Bizzy: {response}\n")
                        else:
                            print("🟡 Melissa didn’t reply this time. Ticket still open.")
                    continue
            except Exception as e:
                print("❌ Follow-up check error:", e)

        # Default Bizzy reply (non-relay, non-follow-up)
        system_prompt = "You are Bizzy, a helpful assistant for a luxury hairstylist named Melissa."
        thread_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in get_thread(phone_number)])

        response = ask_bizzy(system_prompt, thread_prompt)
        add_message(phone_number, "assistant", response)
        print(f"Bizzy: {response}\n")


if __name__ == "__main__":
    phone_number = input("📱 Enter a client phone number to simulate: ")
    simulate_convo(phone_number)
