import speech_recognition as sr

selected_mic_index = None  # Seçilen mikrofon ID'si

def list_microphones():
    """Tüm mikrofonları listeler"""
    mics = sr.Microphone.list_microphone_names()
    return {i: name for i, name in enumerate(mics)}

def set_microphone(index: int):
    """Mikrofon ID'sini ayarla"""
    global selected_mic_index
    selected_mic_index = index

def listen_command():
    """Seçili mikrofondan komut dinle"""
    recognizer = sr.Recognizer()

    if selected_mic_index is None:
        return "Mikrofon seçilmedi!"

    with sr.Microphone(device_index=selected_mic_index) as source:
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="tr-TR")
        return command.lower()
    except:
        return ""

def listen_for_wake_word():
    """Sadece 'jeff uyan' kelimesini bekler"""
    recognizer = sr.Recognizer()
    if selected_mic_index is None:
        return False

    try:
        with sr.Microphone(device_index=selected_mic_index) as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language="tr-TR").lower()
            return "jeff uyan" in command
    except:
        return False
