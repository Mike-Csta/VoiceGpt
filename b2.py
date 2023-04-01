import speech_recognition as sr

# Create a recognizer instance
r = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    # Adjust for ambient noise
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    # Continuously listen for speech input
    while True:
        # Listen for speech input and recognize it
        audio = r.listen(source)
        try:
            # Recognize speech using Google Speech Recognition
            text = r.recognize_google(audio)
            # Print the recognized text in real-time
            print("Real-time output: " + text)
        except sr.UnknownValueError:
            # Handle unrecognized speech input
            print("Could not understand audio")
        except sr.RequestError as e:
            # Handle errors with the speech recognition service
            print("Could not request results; {0}".format(e))
