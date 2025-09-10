import os
from datetime import datetime

LOG_FILE = os.path.join("logs", "actions.log")

def log_action(action: str):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {action}\n")
