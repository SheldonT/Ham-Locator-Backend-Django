# keystone/utils/exception_handlers.py
from functools import wraps
from django.http import JsonResponse
from django.db import IntegrityError
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

def handle_auth_exceptions(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except auth.InvalidIdTokenError:
            return JsonResponse({
                'success': False,
                'message': 'Email already registered',
                'data': {}
            }, status=400)
        except auth.ExpiredIdTokenError:
            return JsonResponse({
                'success': False,
                'message': 'Expired ID token',
                'data': {}
            }, status=401)
        except FirebaseError as e:
            return JsonResponse({
                'success': False,
                'message': f'Firebase error: {str(e)}',
                'data': {}
            }, status=400)
        except IntegrityError as e:
            return JsonResponse({
                'success': False,
                'message': f'Database integrity error: {str(e)}',
                'data': {}
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An unexpected error occurred: {str(e)}',
                'data': {}
            }, status=500)
    return wrapper