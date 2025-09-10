from modes import writing_mode, management_mode, observe_mode

def handle_command(command: str):
    if command == "yazma":
        text = input("Yazılacak metni gir: ")
        print(writing_mode.write_text(text))

    elif command == "yönetim":
        print("Yönetim seçenekleri: oluştur, sil, adlandır, taşı, kopyala")
        choice = input("Seçimin: ")

        if choice == "oluştur":
            path = input("Dosya yolu: ")
            print(management_mode.create_file(path))

        elif choice == "sil":
            path = input("Dosya yolu: ")
            print(management_mode.delete_file(path))

        elif choice == "adlandır":
            old = input("Eski dosya yolu: ")
            new = input("Yeni dosya adı: ")
            print(management_mode.rename_file(old, new))

        elif choice == "taşı":
            src = input("Kaynak dosya: ")
            dst = input("Hedef klasör: ")
            print(management_mode.move_file(src, dst))

        elif choice == "kopyala":
            src = input("Kaynak dosya: ")
            dst = input("Hedef klasör: ")
            print(management_mode.copy_file(src, dst))

    elif command == "gözlem":
        print("1. Tüm loglar\n2. Son X dakika")
        choice = input("Seçimin: ")
        if choice == "1":
            print(observe_mode.read_logs())
        elif choice == "2":
            minutes = int(input("Dakika: "))
            print(observe_mode.read_recent_logs(minutes))

    else:
        print("Bilinmeyen komut!")
