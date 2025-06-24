from fastapi import FastAPI
from app.memory.client_memory import archive_client_thread_if_needed
from pathlib import Path
import asyncio

ACTIVE_CONVO_DIR = Path("active_convos/client_msgs")

def register_background_tasks(app: FastAPI):
    @app.on_event("startup")
    async def start_sweeper():
        async def sweep_forever():
            while True:
                print("\n🕒 [Auto Sweep] Checking for stale threads...\n")
                count = 0
                for file in ACTIVE_CONVO_DIR.glob("*.json"):
                    phone_number = file.stem
                    was_archived = archive_client_thread_if_needed(phone_number)
                    if was_archived:
                        count += 1
                print(f"✅ [Auto Sweep] Archived {count} thread(s)\n")

                await asyncio.sleep(1800)  # Wait 30 minutes

        asyncio.create_task(sweep_forever())  # Kick off loop in background
