import os
import speech_recognition as sr
import pyttsx3
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Mock MusicKit class for testing
class DummyMusicKit:
    def search(self, query):
        logging.info(f"Searching for: {query}")
        # Return dummy data
        return [{'id': '123', 'artistBio': f'{query} is a popular artist known for great music.'}]

    def play(self, track_id):
        logging.info(f"Playing track with ID: {track_id}")

    def stop(self):
        logging.info("Music stopped.")

    def pause(self):
        logging.info("Music paused.")

    def resume(self):
        logging.info("Music resumed.")

# Initialize MusicKit API
music_kit = DummyMusicKit()

# Initialize speech recognition and text-to-speech
r = sr.Recognizer()
engine = pyttsx3.init()

def play_music(artist, song):
    try:
        results = music_kit.search(artist + " " + song)
        if results:
            music_kit.play(results[0]['id'])
            engine.say(f"Playing {song} by {artist}")
        else:
            engine.say("Sorry, I couldn't find that song.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error playing music: " + str(e))
        engine.say("Sorry, an error occurred while playing music.")
        engine.runAndWait()

def stop_music():
    try:
        music_kit.stop()
        engine.say("Music stopped.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error stopping music: " + str(e))
        engine.say("Sorry, an error occurred while stopping music.")
        engine.runAndWait()

def pause_music():
    try:
        music_kit.pause()
        engine.say("Music paused.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error pausing music: " + str(e))
        engine.say("Sorry, an error occurred while pausing music.")
        engine.runAndWait()

def resume_music():
    try:
        music_kit.resume()
        engine.say("Music resumed.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error resuming music: " + str(e))
        engine.say("Sorry, an error occurred while resuming music.")
        engine.runAndWait()

def get_artist_info(artist):
    try:
        results = music_kit.search(artist)
        if results:
            engine.say(f"Here's some info about {artist}")
            engine.say(results[0].get('artistBio', 'No artist bio available.'))
        else:
            engine.say("Sorry, I couldn't find any info about that artist.")
        engine.runAndWait()
    except Exception as e:
        logging.error("Error getting artist info: " + str(e))
        engine.say("Sorry, an error occurred while getting artist info.")
        engine.runAndWait()

def main():
    while True:
        with sr.Microphone() as source:
            print("Listening for command...")
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio, language="en-US").lower()
                logging.info("Recognized command: " + command)

                if "play" in command:
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
                    artist = command.split("info")[1].strip()
                    get_artist_info(artist)
                elif "exit" in command or "quit" in command:
                    engine.say("Goodbye.")
                    engine.runAndWait()
                    break
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
