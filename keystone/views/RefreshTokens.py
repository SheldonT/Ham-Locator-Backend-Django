from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from keystone.utils.cookies import set_auth_cookie
from keystone.utils.refresh_tokens import refresh_firebase_token


class RefreshTokensView(View):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')

        if not refresh_token:
            return JsonResponse({'success': False,
                                 'message': 'No refresh token found in cookies',
                                 'data': {}}, status=400)
        
        try:
            new_tokens = refresh_firebase_token(refresh_token)
            print (f"New tokens: {new_tokens}")
            if new_tokens:
                response = JsonResponse({'success': True,
                                         'message': 'Tokens refreshed successfully',
                                         'data': {
                                             'expiresIn': new_tokens['expires_in']
                                         }}, status=200)
                
                set_auth_cookie(response, 'idToken', new_tokens['id_token'], max_age=int(new_tokens['expires_in']))
                set_auth_cookie(response, 'refreshToken', new_tokens['refresh_token'], max_age=settings.REFRESH_TOKEN_EXPIRY_DAYS)

                return response
            else:
                return JsonResponse({'success': False,
                                     'message': 'Failed to refresh tokens',
                                     'data': {}}, status=400)
        except Exception as e:
            print(f"Error refreshing tokens: {e}")
            return JsonResponse({'success': False,
                                 'message': 'Error occurred while refreshing tokens',
                                 'data': {}}, status=500)