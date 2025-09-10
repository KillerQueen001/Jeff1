import speech_recognition as sr

selected_mic_index = 0  # Başlangıçta varsayılan mikrofon (0 çoğu zaman default)

def list_microphones():
    """Tüm mikrofonları listeler"""
    mics = sr.Microphone.list_microphone_names()
    return {i: name for i, name in enumerate(mics)}

def get_current_mic_name():
    """Seçili mikrofon adını döndürür"""
    mics = sr.Microphone.list_microphone_names()
    if selected_mic_index is not None and 0 <= selected_mic_index < len(mics):
        return mics[selected_mic_index]
    return "Mikrofon seçilmedi"

def set_microphone(index: int):
    """Mikrofon ID'sini ayarla"""
    global selected_mic_index
    selected_mic_index = index
    print(f"👉 Mikrofon ayarlandı: {index}")

def listen_command():
    """Anahtar kelime 'jeff' duyulursa komutu döndürür"""
    recognizer = sr.Recognizer()
    if selected_mic_index is None:
        return ""

    try:
        with sr.Microphone(device_index=selected_mic_index) as source:
            print("🎤 Dinleniyor...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        command = recognizer.recognize_google(audio, language="tr-TR").lower()
        print(f"Algılandı: {command}")
        if "jeff" in command:  # anahtar kelime kontrolü
            return command
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"❌ Ses dinleme hatası: {e}")
        return ""
