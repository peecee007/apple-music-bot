import jwt
import datetime

# Replace with your MusicKit identifier and private key
music_kit_id = "your_music_kit_id"
private_key = "your_private_key"

# Generate a developer token
token = jwt.encode({
    "iss": music_kit_id,
    "exp": int(datetime.datetime.now().timestamp()) + 43200,  # 12 hours
    "aud": "app.music"
}, private_key, algorithm="ES256")

print(token)