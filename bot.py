import os
import speech_recognition as sr
import pyttsx3
from pyobjc import *
from MusicKit import MusicKit
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize MusicKit API
music_kit = MusicKit()

# Initialize speech recognition and text-to-speech
r = sr.Recognizer()
engine = pyttsx3.init()

def play_music(artist, song):
    try:
        # Search for music using MusicKit API
        results = music_kit.search(artist + " " + song)
        if results:
            # Play the first result
            music_kit.play(results[0].id)
            engine.say("Playing " + song + " by " + artist)
            engine.runAndWait()
        else:
            engine.say("Sorry, I couldn't find that song.")
            engine.runAndWait()
    except Exception as e:
        logging.error("Error playing music: " + str(e))
        engine.say("Sorry, an error occurred while playing music.")
        engine.runAndWait()

def stop_music():
    try:
        # Stop playing music
        music_kit.stop()
        engine.say("Music stopped.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error stopping music: " + str(e))
        engine.say("Sorry, an error occurred while stopping music.")
        engine.runAndWait()

def pause_music():
    try:
        # Pause playing music
        music_kit.pause()
        engine.say("Music paused.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error pausing music: " + str(e))
        engine.say("Sorry, an error occurred while pausing music.")
        engine.runAndWait()

def resume_music():
    try:
        # Resume playing music
        music_kit.resume()
        engine.say("Music resumed.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error resuming music: " + str(e))
        engine.say("Sorry, an error occurred while resuming music.")
        engine.runAndWait()

def get_artist_info(artist):
    try:
        # Get artist info using MusicKit API
        results = music_kit.search(artist)
        if results:
            engine.say("Here's some info about " + artist)
            engine.runAndWait()
            # Provide artist info
            engine.say(results[0].artistBio)
            engine.runAndWait()
        else:
            engine.say("Sorry, I couldn't find any info about that artist.")
            engine.runAndWait()
    except Exception as e:
        logging.error("Error getting artist info: " + str(e))
        engine.say("Sorry, an error occurred while getting artist info.")
        engine.runAndWait()

def main():
    while True:
        # Listen for voice commands
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio, language="en-US")
                if "play" in command:
                    # Extract artist and song from command
                    parts = command.split("play")[1].strip().split("by")
                    song = parts[0].strip()
                    artist = parts[1].strip() if len(parts) > 1 else ""
                    play_music(artist, song)
                elif "stop" in command:
                    stop_music()
                elif "pause" in command:
                    pause_music()
                elif "resume" in command:
                    resume_music()
                elif "info" in command:
                    # Extract artist from command
                    artist = command.split("info")[1].strip()
                    get_artist_info(artist)
                else:
                    engine.say("Sorry, I didn't understand that command.")
                    engine.runAndWait()
            except sr.UnknownValueError:
                engine.say("Sorry, I didn't catch that.")
                engine.runAndWait()
            except Exception as e:
                logging.error("Error handling command: " + str(e))
                engine.say("Sorry, an error occurred while handling your command.")
                engine.runAndWait()

if __name__ == "__main__":
    main()