import speech_recognition as sr
from gtts import gTTS
import datetime
import os
import wikipedia
import requests
import pyjokes
import time
import pygame
from pygame import mixer
import random
import threading
import sys
from googletrans import Translator, LANGUAGES
import webbrowser
import psutil
import tempfile
import feedparser  # For RSS news fallback

# ----------------- INIT -----------------
pygame.init()
mixer.init()
recognizer = sr.Recognizer()

# ----------------- SPEAK -----------------
def speak(text):
    try:
        print(f"[Jarvis speaking]: {text}")
        tts = gTTS(text=text, lang="en")
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_file.close()
        tts.save(tmp_file.name)

        if mixer.music.get_busy():
            mixer.music.stop()
            try:
                mixer.music.unload()
            except:
                pass

        mixer.music.load(tmp_file.name)
        mixer.music.play()

        while mixer.music.get_busy():
            time.sleep(0.2)

        mixer.music.stop()
        try:
            mixer.music.unload()
        except:
            pass

        os.remove(tmp_file.name)
    except Exception as e:
        print("Error in speak():", e)

# ----------------- LISTEN -----------------
def listen(timeout=5, phrase_time_limit=7):
    with sr.Microphone() as source:
        print("[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"[Heard]: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("[Timeout: No speech]")
            return ""
        except sr.UnknownValueError:
            print("[Could not understand]")
            return ""
        except sr.RequestError:
            speak("Network error")
            return ""

# ----------------- FILE & APP MAPPINGS -----------------
files = {
    "resume": "C:/Users/PRATYUSHA/Documents/resume.pdf",
    "python3": "C:/Users/PRATYUSHA/Documents/python3.py",
    "kona": "C:/Users/PRATYUSHA/Documents/kona.txt"
}

spotify_urls = {
    "chill": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
    "pop": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
    "focus": "https://open.spotify.com/playlist/37i9dQZF1DX8Uebhn9wzrS"
}

# ----------------- FEATURES -----------------
def tell_time():
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"The time is {now}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def motivate():
    quotes = [
        "Don't watch the clock. Do what it does. Keep going.",
        "The secret of getting ahead is getting started.",
        "The harder you work, the greater you’ll feel when you succeed."
    ]
    speak(random.choice(quotes))

def get_weather(city="Hyderabad"):
    api_key = "f611056fb87fc43c62cbd43099d329d2"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
        else:
            speak("Sorry, I couldn't fetch the weather.")
    except:
        speak("Network error while fetching weather.")

def get_news():
    api_key = "b1f47ac8dc6c41749178a54f36c2022c"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        print("[DEBUG] News API response:", data)
        articles = data.get("articles", [])[:5]

        if articles:
            speak("Here are the top news headlines from NewsAPI.")
            for i, article in enumerate(articles, 1):
                title = article.get("title", "No title")
                if title.strip() == "":
                    title = "No headline available"
                speak(f"Headline {i}: {title}")
        else:
            # Fallback to BBC RSS feed
            speak("NewsAPI returned no headlines. Fetching from BBC RSS feed...")
            feed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
            entries = feed.entries[:5]
            for i, entry in enumerate(entries, 1):
                speak(f"Headline {i}: {entry.title}")
    except Exception as e:
        print("News fetch error:", e)
        speak("Network error while fetching news. Trying BBC RSS feed...")
        try:
            feed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
            entries = feed.entries[:5]
            for i, entry in enumerate(entries, 1):
                speak(f"Headline {i}: {entry.title}")
        except:
            speak("Sorry, I couldn't fetch any news right now.")

def wikipedia_search():
    speak("What should I search on Wikipedia?")
    topic = listen()
    if topic:
        try:
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except:
            speak("Sorry, I couldn't find anything on Wikipedia.")
    else:
        speak("I didn’t catch the topic.")

def calculator():
    speak("What should I calculate?")
    expr = listen()
    if expr:
        try:
            result = eval(expr)
            speak(f"The result is {result}")
        except:
            speak("Sorry, I could not calculate that.")
    else:
        speak("I didn't hear a calculation.")

def play_spotify():
    speak("Which playlist should I play? (chill, pop, focus)")
    choice = listen()
    url = spotify_urls.get(choice, spotify_urls["chill"])
    webbrowser.open(url)
    speak(f"Playing {choice} playlist on Spotify")

def meditation_mode():
    default_audio = "C:/Users/PRATYUSHA/Music/meditation.mp3"
    if os.path.exists(default_audio):
        mixer.music.load(default_audio)
        mixer.music.play()
        speak("Starting meditation mode")
    else:
        speak("Meditation audio not found")

def set_alarm():
    speak("Set hour:")
    h = int(listen())
    speak("Set minute:")
    m = int(listen())
    speak(f"Alarm set for {h}:{m}")
    def alarm_thread():
        while True:
            now = datetime.datetime.now()
            if now.hour == h and now.minute == m:
                speak("Time's up! Wake up!")
                break
            time.sleep(20)
    threading.Thread(target=alarm_thread, daemon=True).start()

def open_file():
    speak("Which file should I open?")
    name = listen()
    path = files.get(name, None)
    if path and os.path.exists(path):
        os.startfile(path)
        speak(f"Opening {name}")
    else:
        speak("File not found.")

def translate_text():
    speak("What text should I translate?")
    text = listen()
    if text:
        speak("Which language should I translate to?")
        lang_name = listen()
        lang_code = None
        for code, name in LANGUAGES.items():
            if lang_name.lower() in name.lower():
                lang_code = code
                break
        if not lang_code:
            lang_code = "en"
        translator = Translator()
        translated = translator.translate(text, dest=lang_code)
        speak(translated.text)
    else:
        speak("I didn’t catch the text.")

def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com/")
    speak("Opening WhatsApp Web")

def add_reminder():
    speak("What should I remind you about?")
    reminder = listen()
    if reminder:
        with open("reminders.txt", "a") as f:
            f.write(reminder + "\n")
        speak("Reminder saved.")
    else:
        speak("I didn’t catch the reminder.")

def show_reminders():
    if os.path.exists("reminders.txt"):
        with open("reminders.txt", "r") as f:
            reminders = f.readlines()
        if reminders:
            speak("Here are your reminders:")
            for r in reminders:
                speak(r.strip())
        else:
            speak("You have no reminders.")
    else:
        speak("No reminders saved.")

def google_calendar_events():
    speak("Google Calendar integration not configured yet.")

def play_youtube():
    speak("What should I play on YouTube?")
    topic = listen()
    if topic:
        url = f"https://www.youtube.com/results?search_query={topic}"
        webbrowser.open(url)
        speak(f"Here are the results for {topic} on YouTube")

def system_status():
    battery = psutil.sensors_battery()
    if battery:
        speak(f"Battery is at {battery.percent} percent")
        if battery.power_plugged:
            speak("Charger is connected")
        else:
            speak("Charger is not connected")
    else:
        speak("Sorry, I couldn't fetch battery status.")

def dictionary_meaning():
    speak("Which word do you want me to define?")
    word = listen()
    if word:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            meaning = response.json()[0]["meanings"][0]["definitions"][0]["definition"]
            speak(f"The meaning of {word} is {meaning}")
        else:
            speak("Sorry, I couldn't find the meaning.")
    else:
        speak("I didn’t catch the word.")

def rock_paper_scissors():
    speak("Let's play Rock Paper Scissors. Say your choice.")
    user = listen()
    choices = ["rock", "paper", "scissors"]
    comp = random.choice(choices)
    speak(f"I chose {comp}")
    if user == comp:
        speak("It's a tie!")
    elif (user == "rock" and comp == "scissors") or \
         (user == "paper" and comp == "rock") or \
         (user == "scissors" and comp == "paper"):
        speak("You win!")
    else:
        speak("I win!")

def shutdown():
    speak("Shutting down Jarvis. Goodbye!")
    sys.exit()

# ----------------- MAIN LOOP -----------------
def main():
    speak("Jarvis activated")
    while True:
        query = listen(timeout=6, phrase_time_limit=10)
        if not query:
            continue

        if "time" in query:
            tell_time()
        elif "joke" in query:
            tell_joke()
        elif "motivate" in query or "quote" in query:
            motivate()
        elif "weather" in query or "temperature" in query:
            speak("Which city?")
            city = listen()
            get_weather(city) if city else get_weather()
        elif "news" in query or "headlines" in query:
            get_news()
        elif "wikipedia" in query:
            wikipedia_search()
        elif "spotify" in query or "play music" in query:
            play_spotify()
        elif "meditate" in query:
            meditation_mode()
        elif "alarm" in query:
            set_alarm()
        elif "open file" in query:
            open_file()
        elif "translate" in query:
            translate_text()
        elif "whatsapp" in query:
            open_whatsapp()
        elif "add reminder" in query:
            add_reminder()
        elif "show reminders" in query:
            show_reminders()
        elif "calendar" in query:
            google_calendar_events()
        elif "youtube" in query:
            play_youtube()
        elif "battery" in query or "status" in query:
            system_status()
        elif "meaning" in query or "dictionary" in query:
            dictionary_meaning()
        elif "rock paper scissors" in query or "game" in query:
            rock_paper_scissors()
        elif "shutdown" in query or "exit" in query or "quit" in query:
            shutdown()
        else:
            speak("Sorry, I didn’t understand that command.")

if __name__ == "__main__":
    main()
