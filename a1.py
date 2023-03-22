import speech_recognition as sr

def recognize_speech(recognizer, audio):
    try:
        return recognizer.recognize_google(audio, language="pl-PL")
    except sr.UnknownValueError:
        return "Nieznane"
    except sr.RequestError as e:
        return f"Błąd: {e}"

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Nasłuchiwanie...")
    while True:
        audio = recognizer.listen(source)
        text = recognize_speech(recognizer, audio)
        print(text)
