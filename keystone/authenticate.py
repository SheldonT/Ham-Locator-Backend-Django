from firebase_admin import auth
import requests
import os
import json
#from .models import Users
from keystone.utils.get_user_model import get_user_model
from keystone.models import KeystoneUser


class User:
    """Generic user class that holds Firebase claims as properties"""
    def __init__(self, **kwargs):
        # Set basic attributes
        self.uid = kwargs.get('uid')
        self.email = kwargs.get('email')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        
        # Set any extra custom claims dynamically
        for key, value in kwargs.items():
            if key not in ['uid', 'email', 'created_at', 'updated_at']:
                setattr(self, key, value)
    


class FirebaseAuthenticationBackend:
    def authenticate(self, request):

        if request is None:
            return None
        
        firebase_token = request.COOKIES.get('idToken')
        
        try:
            decoded_token = auth.verify_id_token(firebase_token, check_revoked=True)

            uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            
            try:
                user_model = get_user_model()
                user, created = user_model.objects.get_or_create(uid=uid, defaults={'email': email})
            except Exception as model_error:
                # If model lookup fails, return a User instance with all Firebase claims as properties
                print(f"Model lookup failed, returning User object: {model_error}")
                return User(**decoded_token)
            
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
            uid = decoded_token['uid']
            
            try:
                # Try to use the model if available
                user_model = get_user_model()
                # Pass only known fields to the model
                model_defaults = {
                    'email': decoded_token.get('email'),
                }
                user, created = user_model.objects.get_or_create(uid=uid, defaults=model_defaults)
                return user
            except Exception as model_error:
                # If model lookup fails, return a User instance with all Firebase claims as properties
                print(f"Model lookup failed, returning User object: {model_error}")
                return User(**decoded_token)

        except Exception as e:
            print(f"Token verification failed: {e}")
            return None