from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from keystone.utils.cookies import set_auth_cookie


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        user = authenticate(request)
        tokens = request.firebase_tokens if hasattr(request, 'firebase_tokens') else None

        if user is not None and tokens is not None:
            response = JsonResponse({'success':True,
                                     'message': 'User logged in successfully',
                                     "data": user.userid}, status=200)
            
            set_auth_cookie(response, 'idToken', tokens['idToken'], max_age=int(tokens['expiresIn']))
            set_auth_cookie(response, 'refreshToken', tokens['refreshToken'], max_age=settings.REFRESH_TOKEN_EXPIRY_DAYS)

            return response
        
        elif user is not None:
            return JsonResponse({'success': True,
                                 'message': 'User already has valid id token', 
                                "data": {"user_id": user.userid}}, status=200)
        
        else:
            return JsonResponse({'success': False,
                                 'message': 'Invalid credentials or no valid token',
                                 'data': {}}, status=401)
            