import speech_recognition as sr
import pyttsx3
import openai
import json
from gtts import gTTS
import os
import pygame
import tempfile
from pydub import AudioSegment
import threading
import eel

# Inicjalizacja Eel i ustawienie folderu z plikami interfejsu
eel.init("web")
# Inicjalizacja silnika mowy


running = True

engine = pyttsx3.init()

# Inicjalizacja rozpoznawania mowy
r = sr.Recognizer()

# Ustawienie imienia asystenta
name = "Mistrzu"

def play_mp3(filename):
    # inicjalizacja biblioteki Pygame
    pygame.init()
    
    # ustawienie parametrów audio
    pygame.mixer.init()
    
    # wczytanie pliku dźwiękowego
    sound = pygame.mixer.Sound(filename)
    
    # odtworzenie pliku dźwiękowego
    sound.play()
    
    # oczekiwanie na zakończenie odtwarzania
    while pygame.mixer.get_busy():
        continue
    
    # wyłączenie biblioteki Pygame




# Funkcja do odtwarzania tekstu
i=1
pygame.mixer.init()
def speed_change(sound, speed=1.2):
    # Mnożenie przez speed zmienia prędkość dźwięku
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def speak(text):
    tts = gTTS(text=text, lang='pl', slow=False)

    # Tworzenie unikalnej nazwy pliku tymczasowego
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_audio_path = fp.name

    tts.save(temp_audio_path)

    # Przyśpieszenie dźwięku przy użyciu pydub
    sound = AudioSegment.from_file(temp_audio_path, format="mp3")
    fast_sound = speed_change(sound, 1.3)
    fast_sound.export(temp_audio_path, format="mp3", bitrate="500k")

    # Odtwarzanie dźwięku za pomocą modułu pygame.mixer
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(100)

    # Zatrzymanie odtwarzania i usunięcie pliku dźwiękowego
    pygame.mixer.music.stop()
    # os.remove(temp_audio_path)


conversation_history = []

def send_query_to_openai(text):
    global conversation_history
    
    openai.api_key = "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"
    openai.organization = "org-OoztSZ0bl4hd36f4gED0N8bj"

    conversation_history.append({"role": "user", "content": text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "jesteś moim prywatnym nauczycielem angielskiego ale rozmawiamy tylko po polsku."},
            *conversation_history
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
                print(zdanie)
                speak(zdanie)
              
                zdanie = ""

    conversation_history.append({"role": "assistant", "content": zdanie.strip()})



# Funkcja do rozpoznawania mowy
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="pl-PL")
        print(f"Rozpoznano: {text}")
        # threading.Thread(target=speak, args=("więc tak.",)).start()
        ans = send_query_to_openai(text)
        if ans:  # Dodaj ten warunek
            speak(ans)
        return text.lower()
    except sr.UnknownValueError:
        print("Nie rozpoznano mowy")
        return ""
    except sr.RequestError as e:
        print(f"Błąd podczas rozpoznawania mowy: {e}")
        return ""

# Główna pętla programu

x=0
@eel.expose
def start_script():
    global running
    running = True
    x = 0
    while running:
        if x == 0:
            speak("Witaj, Jestem od teraz twoim nauczycielem angielskiego, w czym mogę pomóc?")
            command = recognize_speech()
            x = 1
        else:
            # play_mp3("b.mp3")
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
                    send_query_to_openai(command)
        else:
            print("xD")


@eel.expose
def stop_script():
    global running
    running = False

@eel.expose
def change_intro_text(new_text):
    global intro_text
    intro_text = new_text

@eel.expose
def change_system_text(new_text):
    global system_text
    system_text = new_text

# Uruchomienie aplikacji Eel
eel.start("index.html", size=(800, 600))
