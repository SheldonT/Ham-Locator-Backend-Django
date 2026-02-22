from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from firebase_admin import auth
import json
from keystone.utils.get_user_model import get_user_model
from keystone.decorators.handle_auth_exceptions import handle_auth_exceptions


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(View):
    @handle_auth_exceptions
    def post(self, request):

        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        user_model = get_user_model()
        custom_claims = user_model.get_custom_claims()

        claims_data = {claim: data.get(claim) for claim in custom_claims}
        
        if not password or not confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'Both password fields are required',
                'data': {}}, status=400)
        
        if password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'Passwords do not match',
                'data': {}}, status=400)
        
        user = auth.create_user(
            email=email,
            password=password
        )
    
    
        if user:
            uid = user.uid

            auth.set_custom_user_claims(uid, claims_data)

            user_model.objects.create(
                userid=uid,
                email=email,
                **claims_data,
            )

            return JsonResponse({
                'success': True,
                'message': 'User created successfully',
                'data': {"user_id": uid}}, status=201)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Failed to create user',
                'data': {}}, status=400)