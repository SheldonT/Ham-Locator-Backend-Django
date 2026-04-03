from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
from keystone.utils.cookies import delete_auth_cookie
from firebase_admin import auth
from keystone.decorators.handle_auth_exceptions import handle_auth_exceptions

class FirebaseAuthRequiredMixin(View):
    @handle_auth_exceptions
    def dispatch(self, request, *args, **kwargs):
        user = authenticate(request)

        if not user:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        request.user = user
        response = super().dispatch(request, *args, **kwargs)

        id_token = request.COOKIES.get('idToken')

        if id_token:
            try:
                decoded_token = auth.verify_id_token(id_token, check_revoked=True)

                exp_time = decoded_token.get('exp')
                current_time = datetime.timestamp(datetime.now())
                time_until_expiry = exp_time - current_time if exp_time else 0

                # if the id token is expiring in less than 5 minutes, signal the client to refresh
                if time_until_expiry < 300:
                    response['X-Token-Refresh'] = 'true'

            except auth.RevokedIdTokenError:

                delete_auth_cookie(response, 'idToken')
                delete_auth_cookie(response, 'refreshToken')
                return JsonResponse({'success': False,
                                    'message': 'Token has been revoked. Please log in again.',
                                    'data': {}}, status=401)
            except auth.InvalidIdTokenError:
                delete_auth_cookie(response, 'idToken')
                delete_auth_cookie(response, 'refreshToken')
                return JsonResponse({'success': False,
                                    'message': 'Invalid authentication token.',
                                    'data': {}}, status=401)
            except auth.ExpiredIdTokenError:
                delete_auth_cookie(response, 'idToken')
                delete_auth_cookie(response, 'refreshToken')
                return JsonResponse({'success': False,
                                    'message': 'Authentication token has expired.',
                                    'data': {}}, status=401)
            except Exception as e:
                # For any other error, treat as unauthorized
                delete_auth_cookie(response, 'idToken')
                delete_auth_cookie(response, 'refreshToken')
                return JsonResponse({'success': False,
                                    'message': 'Authentication failed.',
                                    'data': {}}, status=401)
        else:
            delete_auth_cookie(response, 'idToken')
            delete_auth_cookie(response, 'refreshToken')
            return JsonResponse({'success': False,
                                'message': 'Authentication required to access this resource',
                                'data': {}}, status=401)

        return response
