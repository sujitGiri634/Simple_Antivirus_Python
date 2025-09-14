import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def append_log(filename, text):
    """Write logs into logs/<filename>"""
    log_path = os.path.join(LOG_DIR, filename)
    entry = f"[{now()}] {text}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
