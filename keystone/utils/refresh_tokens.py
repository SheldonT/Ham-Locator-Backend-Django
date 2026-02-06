import requests
import os

def refresh_firebase_token(refresh_token):
    auth_url = "https://securetoken.googleapis.com/v1/token"
    api_key = os.getenv('FIREBASE_API_KEY')
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    
    response = requests.post(f"{auth_url}?key={api_key}", data=payload)

    if response.status_code == 200:

        return {"id_token": response.json().get('id_token'),
                "refresh_token": response.json().get('refresh_token'),
                "expires_in": response.json().get('expires_in')}
    else:
        return None