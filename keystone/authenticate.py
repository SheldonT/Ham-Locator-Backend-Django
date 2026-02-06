from firebase_admin import auth
import requests
import os
import json
#from .models import Users
from keystone.utils.get_user_model import get_user_model

class FirebaseAuthenticationBackend:
    def authenticate(self, request):

        if request is None:
            return None
        
        firebase_token = request.COOKIES.get('idToken')
        
        try:
            decoded_token = auth.verify_id_token(firebase_token, check_revoked=True)

            uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            
            user_model = get_user_model()
            user, created = user_model.objects.get_or_create(userid=uid, defaults={'email': email})
            
            return user
        except Exception as e:
            print(f"Token Authentication Failed. Looking for user credentials: {e}")
        
        #email = request.POST.get('email', '')
        #password = request.POST.get('password', '')
        
        try:
            data = json.loads(request.body)
            email = data.get('username')
            password = data.get('passwd')

            if email and password:
                tokens = self.firebase_authenticate(email, password)
                
                if tokens:
                    user = self.get_user(tokens['idToken'])

                    request.firebase_tokens = tokens  # Attach tokens to request for later use

                    return user
        except Exception as e:
            print(f"Email/Password Authentication Failed. Token may have been revoked or invalid: {e}")
            
        return None
            
    def firebase_authenticate(self, email, password):
        auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        api_key = os.getenv('FIREBASE_API_KEY')
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True}
        
        response = requests.post(f"{auth_url}?key={api_key}", data=payload)

        if response.status_code == 200:
            user_data = response.json()

            return {
                'idToken': user_data['idToken'],
                'refreshToken': user_data['refreshToken'],
                'expiresIn': user_data['expiresIn'],  # Seconds (usually 3600)
            }
        
        return None
    
    
    def get_user(self, token):

        try:
            decoded_token = auth.verify_id_token(token, check_revoked=True)
            user_id = decoded_token['uid']

            user_data = {
                'email': decoded_token.get('email'),
                'call': decoded_token.get('callsign'),
                'country': decoded_token.get('country'),
                'lat': decoded_token.get('lat'),
                'lng': decoded_token.get('lng'),
                'gridloc': decoded_token.get('gridloc'),
                'privilege': decoded_token.get('privilege'),
                'units': decoded_token.get('units'),
                'itu': decoded_token.get('itu'),
                'utc': decoded_token.get('utc'),
            }
            user_model = get_user_model()
            user, created = user_model.objects.get_or_create(userid=user_id, defaults=user_data)
            return user

        except Exception as e:
            print(f"Token verification failed: {e}")
            return None