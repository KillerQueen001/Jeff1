import os
import shutil
from utils import log_action
from send2trash import send2trash

def create_file(path: str):
    path = os.path.normpath(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write("")
    log_action(f"Dosya oluşturuldu: {path}")
    return f"Dosya oluşturuldu: {path}"

def delete_file(path: str):
    path = os.path.normpath(path)
    if not os.path.exists(path):
        raise FileNotFoundError("Dosya bulunamadı!")
    send2trash(path)
    log_action(f"Dosya çöp kutusuna taşındı: {path}")
    return f"Dosya çöp kutusuna taşındı: {path}"

def rename_file(old_path: str, new_name: str):
    old_path = os.path.normpath(old_path)
    directory = os.path.dirname(old_path)
    new_path = os.path.join(directory, new_name)
    os.rename(old_path, new_path)
    log_action(f"Dosya yeniden adlandırıldı: {old_path} → {new_path}")
    return f"Dosya yeniden adlandırıldı: {old_path} → {new_path}"

def move_file(src: str, dst: str):
    src, dst = os.path.normpath(src), os.path.normpath(dst)
    shutil.move(src, dst)
    log_action(f"Dosya taşındı: {src} → {dst}")
    return f"Dosya taşındı: {src} → {dst}"

def copy_file(src: str, dst: str):
    src, dst = os.path.normpath(src), os.path.normpath(dst)
    shutil.copy(src, dst)
    log_action(f"Dosya kopyalandı: {src} → {dst}")
    return f"Dosya kopyalandı: {src} → {dst}"
