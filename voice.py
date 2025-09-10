import speech_recognition as sr

selected_mic_index = None  # Seçilen mikrofon ID'si

def list_microphones():
    """Tüm mikrofonları listeler"""
    try:
        mics = sr.Microphone.list_microphone_names()
        return {i: name for i, name in enumerate(mics)}
    except Exception as e:
        print(f"❌ Mikrofon listelenemedi: {e}")
        return {}

def set_microphone(index: int):
    """Mikrofon ID'sini ayarla"""
    global selected_mic_index
    selected_mic_index = index
    print(f"👉 Mikrofon ayarlandı: {index}")

def listen_command():
    """Seçili mikrofondan komut dinle"""
    recognizer = sr.Recognizer()

    if selected_mic_index is None:
        return "Mikrofon seçilmedi!"

    try:
        with sr.Microphone(device_index=selected_mic_index) as source:
            print("🎤 Komut dinleniyor...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        command = recognizer.recognize_google(audio, language="tr-TR").lower()
        print(f"Algılandı: {command}")
        return command
    except sr.UnknownValueError:
        print("❌ Ses anlaşılamadı.")
        return ""
    except sr.RequestError as e:
        print(f"❌ API hatası: {e}")
        return ""
    except Exception as e:
        print(f"❌ Dinleme hatası: {e}")
        return ""

def listen_for_wake_word():
    """Sadece 'jeff uyan' kelimesini bekler"""
    recognizer = sr.Recognizer()
    if selected_mic_index is None:
        return False

    try:
        with sr.Microphone(device_index=selected_mic_index) as source:
            print("🎤 'Jeff uyan' komutu bekleniyor...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        command = recognizer.recognize_google(audio, language="tr-TR").lower()
        print(f"Wake word algılandı: {command}")
        return "jeff uyan" in command
    except Exception as e:
        print(f"❌ Wake word hatası: {e}")
        return False
