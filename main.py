import tkinter as tk
from tkinter import messagebox, scrolledtext
import speech_recognition as sr
import pyttsx3
from apple_music_api import search_song, generate_apple_music_token
import json
import time
import logging

# Load config
with open("config.json") as f:
    config = json.load(f)

KEY_ID = config["key_id"]
TEAM_ID = config["team_id"]
PRIVATE_KEY_FILE = config["private_key_file"]

# Logging setup
logging.basicConfig(filename="command_log.txt", level=logging.INFO)

# Speech
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Get developer token
token_cache = {"token": None, "timestamp": 0}

def get_token():
    if not token_cache["token"] or time.time() - token_cache["timestamp"] > 3600:
        token_cache["token"] = generate_apple_music_token(KEY_ID, TEAM_ID, PRIVATE_KEY_FILE)
        token_cache["timestamp"] = time.time()
    return token_cache["token"]

# GUI Actions
def speak(text):
    engine.say(text)
    engine.runAndWait()

def log_command(command):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    logging.info(f"{timestamp} {command}")
    output.insert(tk.END, f"{timestamp} {command}\n")

def handle_command(cmd):
    log_command(cmd)
    speak(f"You said: {cmd}")

    if "play" in cmd.lower():
        token = get_token()
        term = cmd.split("play", 1)[-1].strip()
        results = search_song(token, term)
        try:
            song = results['results']['songs']['data'][0]
            title = song['attributes']['name']
            artist = song['attributes']['artistName']
            url = song['attributes']['url']
            speak(f"Found {title} by {artist}")
            output.insert(tk.END, f"🎵 {title} by {artist}\n🔗 {url}\n\n")
        except Exception as e:
            speak("Sorry, I couldn't find that song.")
            output.insert(tk.END, "❌ Song not found.\n")

    elif "exit" in cmd.lower():
        speak("Goodbye!")
        root.quit()
    else:
        speak("Sorry, I don't understand that command.")
        output.insert(tk.END, "❓ Unknown command.\n")

def on_listen():
    with sr.Microphone() as source:
        output.insert(tk.END, "🎙 Listening...\n")
        audio = recognizer.listen(source)
        try:
            cmd = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, cmd)
            handle_command(cmd)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except Exception as e:
            speak("Error with speech recognition.")

def on_submit():
    cmd = entry.get()
    if cmd:
        handle_command(cmd)

# GUI Setup
root = tk.Tk()
root.title("Voice Music Assistant")
root.geometry("600x400")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

submit_btn = tk.Button(btn_frame, text="Submit", command=on_submit)
submit_btn.pack(side=tk.LEFT, padx=10)

listen_btn = tk.Button(btn_frame, text="🎙 Listen", command=on_listen)
listen_btn.pack(side=tk.LEFT)

output = scrolledtext.ScrolledText(root, height=15, width=70)
output.pack(pady=10)

root.mainloop()
