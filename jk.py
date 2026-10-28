import requests
import jwt

# Replace with your MusicKit identifier and secret key
music_kit_id = "your_music_kit_id"
secret_key = "your_secret_key"

# Generate a MusicKit token
token = jwt.encode({"iss": music_kit_id}, secret_key, algorithm="ES256")

# Use the MusicKit API to search for music
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.music.apple.com/v1/catalog/us/search", headers=headers)

print(response.json())