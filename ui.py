import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from modes import management_mode, writing_mode, observe_mode
import voice
import threading
import time



class JeffUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeff1 Asistan")
        self.root.geometry("950x600")

        # Başlangıçta sidebar oluştur
        self.sidebar_expanded = True
        self.sidebar = tk.Frame(root, width=200, bg="#222")
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(root, bg="#333")
        self.main_area.pack(side="right", expand=True, fill="both")

        self.create_sidebar_buttons()
        self.show_home()

        # Wake word thread'ini başlat
        self.wake_thread = threading.Thread(target=self.wake_listener, daemon=True)
        self.wake_thread.start()

    def close_to_tray(self):
        """UI'yi gizle (ama program kapanmaz)"""
        self.root.withdraw()

    def wake_listener(self):
        """Arka planda sürekli 'jeff uyan' bekler"""
        while True:
            time.sleep(1)
            if not self.root.winfo_viewable():  # pencere gizlenmiş
                woke = voice.listen_for_wake_word()
                if woke:
                    print("👉 Wake word algılandı: Jeff geri açılıyor")
                    self.root.after(0, self.root.deiconify)
    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.pack_forget()
            self.sidebar = tk.Frame(self.root, width=60, bg="#222")
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_expanded = False
        else:
            self.sidebar.pack_forget()
            self.sidebar = tk.Frame(self.root, width=200, bg="#222")
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_expanded = True
        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        toggle_btn = tk.Button(self.sidebar, text="☰", command=self.toggle_sidebar,
                               bg="#111", fg="white", relief="flat", padx=10, pady=10)
        toggle_btn.pack(fill="x")

        buttons = [
            ("🏠 Ana Sayfa", self.show_home),
            ("✍️ Yazma", self.show_writing),
            ("🗂️ Yönetim", self.show_management),
            ("👀 Gözlem", self.show_observe),
            ("🎤 Sesli Komut", self.handle_voice),
            ("🎙️ Mikrofon Seç", self.select_microphone),
            ("🚪 Gizle", self.close_to_tray)  # ❌ yerine gizle butonu
        ]


        for text, cmd in buttons:
            btn = tk.Button(self.sidebar, text=text if self.sidebar_expanded else text[0],
                            command=cmd, bg="#444", fg="white", relief="flat", padx=10, pady=10)
            btn.pack(fill="x", pady=2)
    def handle_voice(self):
        command = voice.listen_command()

        if "yazma" in command:
            self.show_writing()
        elif "yönetim" in command:
            self.show_management()
        elif "gözlem" in command:
            self.show_observe()
        elif "ana sayfa" in command:
            self.show_home()
        else:
            messagebox.showinfo("Jeff1", f"Komut anlaşılamadı: {command}")

    def select_microphone(self):
        """UI üzerinden mikrofon seçme ekranı"""
        win = tk.Toplevel(self.root)
        win.title("Mikrofon Seçimi")

        mics = voice.list_microphones()
        tk.Label(win, text="Kullanmak istediğin mikrofonu seç:").pack(pady=5)

        combo = ttk.Combobox(win, values=[f"{i}: {name}" for i, name in mics.items()], width=60)
        combo.pack(pady=5)

        def set_mic():
            if combo.current() >= 0:
                mic_id = list(mics.keys())[combo.current()]
                voice.set_microphone(mic_id)
                self.selected_mic = mic_id
                messagebox.showinfo("Jeff1", f"Mikrofon seçildi: {mics[mic_id]}")
                win.destroy()

        ttk.Button(win, text="Seç", command=set_mic).pack(pady=10)

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main()
        tk.Label(self.main_area, text="Jeff1 Asistan'a Hoş Geldin!",
                 bg="#333", fg="white", font=("Arial", 22)).pack(pady=40)

    def show_writing(self):
        self.clear_main()
        tk.Label(self.main_area, text="✍️ Yazma Modu", bg="#333", fg="white", font=("Arial", 18)).pack(pady=15)

        entry = tk.Entry(self.main_area, width=50)
        entry.pack(pady=5)

        def write_text():
            try:
                msg = writing_mode.write_text(entry.get())
                messagebox.showinfo("Jeff1", msg)
            except Exception as e:
                messagebox.showerror("Hata", str(e))

        tk.Button(self.main_area, text="Yaz", command=write_text,
                  bg="#555", fg="white").pack(pady=10)

    def show_management(self):
        self.clear_main()
        tk.Label(self.main_area, text="🗂️ Yönetim Modu", bg="#333", fg="white", font=("Arial", 18)).pack(pady=10)

        notebook = ttk.Notebook(self.main_area)
        notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # --- Oluştur ---
        create_tab = tk.Frame(notebook, bg="#333")
        notebook.add(create_tab, text="📄 Oluştur")
        path_entry_c = tk.Entry(create_tab, width=60)
        path_entry_c.pack(pady=10)
        ttk.Button(create_tab, text="Dosya Oluştur",
                   command=lambda: self.handle_action(lambda: management_mode.create_file(path_entry_c.get()))).pack(pady=5)

        # --- Sil ---
        delete_tab = tk.Frame(notebook, bg="#333")
        notebook.add(delete_tab, text="🗑️ Sil")
        path_entry_d = tk.Entry(delete_tab, width=60)
        path_entry_d.pack(pady=10)
        ttk.Button(delete_tab, text="Dosya Sil",
                   command=lambda: self.handle_action(lambda: management_mode.delete_file(path_entry_d.get()))).pack(pady=5)

        # --- Yeniden Adlandır ---
        rename_tab = tk.Frame(notebook, bg="#333")
        notebook.add(rename_tab, text="✏️ Adlandır")
        old_entry = tk.Entry(rename_tab, width=60)
        old_entry.pack(pady=5)
        new_entry = tk.Entry(rename_tab, width=60)
        new_entry.pack(pady=5)
        ttk.Button(rename_tab, text="Yeniden Adlandır",
                   command=lambda: self.handle_action(lambda: management_mode.rename_file(old_entry.get(), new_entry.get()))).pack(pady=5)

        # --- Taşı ---
        move_tab = tk.Frame(notebook, bg="#333")
        notebook.add(move_tab, text="📂 Taşı")
        src_entry_m = tk.Entry(move_tab, width=60)
        src_entry_m.pack(pady=5)
        dst_entry_m = tk.Entry(move_tab, width=60)
        dst_entry_m.pack(pady=5)
        ttk.Button(move_tab, text="Dosya Taşı",
                   command=lambda: self.handle_action(lambda: management_mode.move_file(src_entry_m.get(), dst_entry_m.get()))).pack(pady=5)

        # --- Kopyala ---
        copy_tab = tk.Frame(notebook, bg="#333")
        notebook.add(copy_tab, text="📑 Kopyala")
        src_entry_cp = tk.Entry(copy_tab, width=60)
        src_entry_cp.pack(pady=5)
        dst_entry_cp = tk.Entry(copy_tab, width=60)
        dst_entry_cp.pack(pady=5)
        ttk.Button(copy_tab, text="Dosya Kopyala",
                   command=lambda: self.handle_action(lambda: management_mode.copy_file(src_entry_cp.get(), dst_entry_cp.get()))).pack(pady=5)

    def show_observe(self):
        self.clear_main()
        tk.Label(self.main_area, text="👀 Gözlem Modu", bg="#333", fg="white", font=("Arial", 18)).pack(pady=10)

        frame = tk.Frame(self.main_area, bg="#333")
        frame.pack(pady=5)

        tk.Label(frame, text="Son X dakika: ", bg="#333", fg="white").pack(side="left")
        minutes_entry = tk.Entry(frame, width=5)
        minutes_entry.pack(side="left", padx=5)

        text_area = scrolledtext.ScrolledText(self.main_area, wrap="word", width=90, height=25, bg="#111", fg="white")
        text_area.pack(padx=10, pady=10)

        def show_all():
            logs = observe_mode.read_logs()
            text_area.delete("1.0", "end")
            text_area.insert("1.0", logs)

        def show_recent():
            try:
                minutes = int(minutes_entry.get())
                logs = observe_mode.read_recent_logs(minutes)
                text_area.delete("1.0", "end")
                text_area.insert("1.0", logs)
            except ValueError:
                messagebox.showerror("Hata", "Dakika değeri geçerli değil!")

        ttk.Button(frame, text="Tüm Loglar", command=show_all).pack(side="left", padx=5)
        ttk.Button(frame, text="Filtrele", command=show_recent).pack(side="left", padx=5)

        # Başlangıçta tüm loglar
        show_all()

    def handle_action(self, action_func):
        try:
            msg = action_func()
            messagebox.showinfo("Başarılı", msg)
        except Exception as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = JeffUI(root)
    root.mainloop()
