import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musiclibrary
import os
from openai import OpenAI

# ----------------- INITIAL SETUP -----------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = os.getenv("1872851ab58e422b90f57cf5712b9a0f")
client = OpenAI(
    api_key="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"
)   # Reads OPENAI_API_KEY automatically


# ----------------- SPEAK FUNCTION -----------------
def speak(text):
    engine.say(text)
    engine.runAndWait()


# ----------------- AI PROCESS -----------------
def aiprocess(command):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )
    return response.choices[0].message.content


# ----------------- COMMAND HANDLER -----------------
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://www.google.com")

    elif "open facebook" in c:
        webbrowser.open("https://www.facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")

    elif "open instagram" in c:
        webbrowser.open("https://www.instagram.com")

    elif c.startswith("play"):
        song = c.split("play ")[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found")

    elif "news" in c:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "in",
            "apiKey": newsapi
        }

        response = requests.get(url, params=params)
        data = response.json()

        for article in data.get("articles", [])[:5]:
            speak(article["title"])

    else:
        output = aiprocess(c)
        speak(output)


# ----------------- MAIN LOOP -----------------
if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes")

                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.UnknownValueError:
            pass

        except Exception as e:
            print("Error:", e)
