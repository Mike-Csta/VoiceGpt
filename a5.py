import speech_recognition as sr
import pyttsx3
import openai
import json

# Inicjalizacja silnika mowy
engine = pyttsx3.init()

# Inicjalizacja rozpoznawania mowy
r = sr.Recognizer()

# Ustawienie imienia asystenta
name = "Mistrzu"

# Funkcja do odtwarzania tekstu
def speak(text):
    engine.say(text)
    engine.runAndWait()

def send_query_to_openai(text):
    openai.api_key = "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"
    openai.organization = "org-OoztSZ0bl4hd36f4gED0N8bj"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś asystentem głosowym"},
            {"role": "user", "content": text},
        ],
        temperature=0,
        stream=True
    )

    zdanie = ""

    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        y =  json.loads(str(chunk_message))

        if 'content' in y:
            text = y['content']
            zdanie += text  # concatenate the text

            if '.' in zdanie:
                speak(zdanie)
                zdanie = ""


# Funkcja do rozpoznawania mowy
def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="pl-PL")
        print(f"Rozpoznano: {text}")
        speak("Czekaj, daj mi pomyśleć")
        ans = send_query_to_openai(text)
        speak("Już ci mówię.")
        speak(ans)
        return text.lower()
    except sr.UnknownValueError:
        print("Nie rozpoznano mowy")
        return ""
    except sr.RequestError as e:
        print(f"Błąd podczas rozpoznawania mowy: {e}")
        return ""

# Główna pętla programu
while True:
    speak("Witaj, nazywam się Adolf. Jak mogę ci pomóc?")
    command = recognize_speech()

    if name.lower() in command:
        speak(f"Tak, słucham {name}")

        speak("Cześć, jak mogę ci pomóc?")

        while True:
            command = recognize_speech()

            if "do widzenia" in command:
                speak("Do zobaczenia!")
                break

    else:
        speak(f"Nie słyszę imienia {name}. Spróbuj ponownie.")
