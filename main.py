import sys
from commands import handle_command

def main():
    print("=== Jeff1 Asistan Başlatıldı ===")
    print("Komut bekleniyor... (örn: yazma, yönetim, gözlem, çıkış)")

    while True:
        command = input("> ").strip().lower()
        if command == "çıkış":
            print("Jeff1 kapatılıyor...")
            sys.exit(0)
        handle_command(command)

if __name__ == "__main__":
    main()
