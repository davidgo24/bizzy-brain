import argparse
from pathlib import Path
from app.memory.client_memory import archive_client_thread_if_needed

ACTIVE_CONVO_DIR = Path("app/active_convos/client_msgs")

def sweep_all_threads():
    print("\n🔄 Sweeping for stale threads...\n")
    count = 0
    print(f"📁 Looking in: {ACTIVE_CONVO_DIR.resolve()}")
    for file in ACTIVE_CONVO_DIR.glob("*.json"):
        phone_number = file.stem
        was_archived = archive_client_thread_if_needed(phone_number)
        if was_archived:
            count += 1
        else:
            print(f"🟡 Thread for {phone_number} is not stale. Skipping.")

    print(f"\n✅ Sweep complete. Archived {count} stale thread(s).\n")

def reset_thread(phone_number):
    path = ACTIVE_CONVO_DIR / f"{phone_number}.json"
    if path.exists():
        path.unlink()
        print(f"🗑️ Deleted active thread for {phone_number}")
    else:
        print(f"⚠️ No active thread found for {phone_number}")

if __name__ == "__main__":
    print("🚀 CLI loaded")

    parser = argparse.ArgumentParser(description="Bizzy CLI Tools")
    parser.add_argument("--sweep", action="store_true", help="Sweep and archive stale client threads")
    parser.add_argument("--reset", type=str, help="Manually delete a thread by phone number")

    args = parser.parse_args()

    if args.sweep:
        sweep_all_threads()
    elif args.reset:
        reset_thread(args.reset)
    else:
        parser.print_help()
