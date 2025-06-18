import sys
import json
import os

def replay_thread(phone_number):
    path = f"memory/{phone_number}.json"
    if not os.path.exists(path):
        print("❌ No thread found for this number!")
        return
    
    with open(path, 'r') as f:
        thread = json.load(f)

    print(f"--- Replaying thread for {phone_number} ---\n")
    for msg in thread:
        role = msg["role"].capitalize()
        timestamp = msg.get("timestamp", "no timestamp")
        print(f'[{timestamp}] {role}: {msg['content']}\n')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/replay_thread.py <phone_number>")
    else:
        replay_thread(sys.argv[1])