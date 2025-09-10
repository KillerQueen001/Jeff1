import os
from datetime import datetime, timedelta
from utils import LOG_FILE

def read_logs():
    if not os.path.exists(LOG_FILE):
        return "Henüz log kaydı yok."
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()

def read_recent_logs(minutes: int):
    if not os.path.exists(LOG_FILE):
        return "Henüz log kaydı yok."

    cutoff = datetime.now() - timedelta(minutes=minutes)
    result = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            timestamp_str = line.split("]")[0][1:]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            if timestamp >= cutoff:
                result.append(line.strip())

    return "\n".join(result) if result else f"Son {minutes} dakikada işlem yok."
