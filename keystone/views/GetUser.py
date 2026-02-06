from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import requests
import os
import json
from keystone.utils.get_user_model import get_user_model
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin

class GetUserView(AuthRequiredMixin, View):
    def get(self, request):
        
        authenticated_user = request.user
        custom_claims = authenticated_user.get_custom_claims(include_system_fields=True)

        if authenticated_user:

            user_data = {}

            for claim in custom_claims:
                user_data[claim] = getattr(authenticated_user, claim, None)

            return JsonResponse({
                'success': True,
                'message': 'User retrieved successfully',
                'data': user_data}, status=200)
        else:
            return JsonResponse({'success': False,
                                 'message': 'User not found',
                                 'data': {}}, status=404)