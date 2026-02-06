from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from firebase_admin import auth
from keystone.decorators.handle_auth_exceptions import handle_auth_exceptions

class LogoutView(View):
    @handle_auth_exceptions
    def post(self, request):

        id_token = request.COOKIES.get('idToken')
        #response_data = {'status': True, 'message': 'User logged out successfully', 'data': {}}
        #response_status = 200

        if not id_token:
            #return JsonResponse({'error': 'No id token found in cookies. No user authenticated'}, status=400)
            response_data = {'status': False, 'message': 'No id token found in cookies. No user authenticated', 'data': {}}
            response_status = 400
        else:    
            try:
                user_id = auth.verify_id_token(id_token, check_revoked=True).get('uid')
                auth.revoke_refresh_tokens(user_id)

                response_data = {'status': True, 'message': 'User logged out successfully', 'data': {"user_id": user_id}}
                response_status = 200

            except Exception as e:
                response_data = {'status': False, 'message': 'Failed to revoke tokens.', 'data': {e}}
                response_status = 400
        
        response = JsonResponse(response_data, status=response_status)
        response.delete_cookie('idToken')
        response.delete_cookie('refreshToken')

        return response