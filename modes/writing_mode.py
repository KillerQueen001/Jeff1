import pyautogui
from utils import log_action

def write_text(text: str):
    pyautogui.typewrite(text, interval=0.05)
    log_action(f"Yazma modu ile yazıldı: {text}")
    return f"Metin yazıldı: {text}"
