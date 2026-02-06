
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from firebase_admin import auth
import requests
import os
import json
from keystone.utils.get_user_model import get_user_model
from keystone.decorators.handle_auth_exceptions import handle_auth_exceptions
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin

class EditUserView(AuthRequiredMixin, View):
    @handle_auth_exceptions
    def post(self, request):
        
        authenticated_user = request.user
        data = json.loads(request.body)

        email = data.pop('email', None)
        password = data.pop('password', None)
        confirm_password = data.pop('confirm_password', None)


        if email:
            auth.update_user(
                authenticated_user.userid,
                email=email
            )
            authenticated_user.email = email

        if (password == confirm_password) and (password and confirm_password):
            auth.update_user(
                authenticated_user.userid,
                password=password
            )

        for key, value in data.items():
            if hasattr(authenticated_user, key):
                setattr(authenticated_user, key, value)

        authenticated_user.save()

        if data:
            auth.set_custom_user_claims(
                authenticated_user.userid,
                data
            )

        return JsonResponse({'success': True,
                            'message': 'User updated successfully', 
                            'data': {"user_id": authenticated_user.userid}}, status=201)