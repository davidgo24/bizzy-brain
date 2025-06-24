from pathlib import Path
import json


def load_latest_thread(phone_number: str) -> dict | None:
    archive_dir = Path(f"client_msgs_archive/{phone_number}")
    if not archive_dir.exists():
        return None
    
    json_files = sorted(
        archive_dir.glob("*json"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    if not json_files:
        return None
    

    latest_path = json_files[0]
    print(f"[🧠 Loaded] Most recent thread: {latest_path.name}")

    with open(latest_path, "r") as f:
        return json.load(f)
    
