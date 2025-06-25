from datetime import datetime
import pytz

PST = pytz.timezone("America/Los_Angeles")

def now_pst() -> datetime:
    return datetime.now(PST)

def format_pst(dt: datetime) -> str:
    return dt.astimezone(PST).strftime("%Y-%m-%d %I:%M %p")

def format_filename_timestamp(dt: datetime) -> str:
    """Safe timestamp format for filenames (e.g., 2025-06-25T07-12-14PM)"""
    return dt.astimezone(PST).strftime("%Y-%m-%dT%I-%M-%S%p")
