import speech_recognition as sr
import pyttsx3
import openai
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
    # answer = "pogoda"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "jesteś asystentem głosowym"},
            {"role": "user", "content": text},
        ],
    )
    print(response.choices[0].message.content)
    answer = response.choices[0].message.content.split("[👨HITLER]")[1]
    return answer


# Funkcja do rozpoznawania mowy
def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # Rozpoznawanie mowy
        text = r.recognize_google(audio, language="pl-PL")
        print(f"Rozpoznano: {text}")
        speak("czekaj, daj pomyśleć, nie moja wina że nie wykupiłeś premium śmieciu, teraz będziesz czekał")
        ans = send_query_to_openai(text)
        speak("Już ci mówie.")
        speak(ans)
        speak("W ogóle mówmy sobie po imieniu majk. Nazywam się Adolf")
        return text.lower()
    except sr.UnknownValueError:
        print("Nie rozpoznano mowy")
        return ""
    except sr.RequestError as e:
        print(f"Błąd podczas rozpoznawania mowy: {e}")
        return ""

# Główna pętla programu
while True:
    # Oczekiwanie na komendę
    speak("Witaj przyjacialu. Nazywam się Adolf . Jak mogę ci pomóc?")
    command = recognize_speech()

    # Sprawdzanie, czy mówiący użył imienia asystenta
    if name.lower() in command:
        speak(f"Tak, słucham {name}")

        # Rozpoczęcie rozmowy
        speak("Cześć, jak mogę ci pomóc?")

        # Pętla rozmowy
        while True:
            command = recognize_speech()

            if "do widzenia" in command:
                speak("Do zobaczenia!")
                break

            # Tutaj można dodać więcej przypadków obsługiwanych przez asystenta

    else:
        speak(f"Nie słyszę imienia {name}. Spróbuj ponownie.")
