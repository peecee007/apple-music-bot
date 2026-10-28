import jwt
import time
import requests

def generate_apple_music_token(key_id, team_id, private_key_file):
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    headers = {
        'alg': 'ES256',
        'kid': key_id
    }

    payload = {
        'iss': team_id,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600 * 12  # 12 hrs
    }

    token = jwt.encode(payload, private_key, algorithm='ES256', headers=headers)
    return token if isinstance(token, str) else token.decode('utf-8')

def search_song(token, term):
    url = f"https://api.music.apple.com/v1/catalog/us/search?term={term}&types=songs&limit=1"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()
