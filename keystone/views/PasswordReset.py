# This would go in keystone/views/ if you want it
import requests
import os
from firebase_admin import auth
from rest_framework.views import APIView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlparse, parse_qs


class PasswordResetView(APIView):
    def post(self, request):

        email_address = request.data.get('email')
        use_firebase_pw_reset = getattr(settings, "USE_FIREBASE_PW_RESET", None)

        oob_code = request.data.get('oobCode')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not email_address:
            return JsonResponse({
                'success': False,
                'message': 'Email address is required',
                'data': {}}, status=400)
        
        try:
            if oob_code and new_password:

                if new_password != confirm_password:
                    return JsonResponse({
                        'success': False,
                        'message': 'Passwords do not match',
                        'data': {}}, status=400)
                
                # Verify the oobCode and get the email associated with it
                reset_url = f"https://identitytoolkit.googleapis.com/v1/accounts:resetPassword?key={os.getenv('FIREBASE_API_KEY')}" if getattr(settings, "FIREBASE_PW_RESET_API", None) is None else settings.FIREBASE_PW_RESET_API
                payload = {
                    'oobCode': oob_code,
                    'newPassword': new_password
                }
                response = requests.post(reset_url, json=payload)
                response.raise_for_status()  # Raise an error for bad responses

                return JsonResponse({
                    'success': True,
                    'message': 'Password reset successfully',
                    'data': {} }, status=200)

            if use_firebase_pw_reset:
                reset_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.getenv('FIREBASE_API_KEY')}" if getattr(settings, "FIREBASE_PW_RESET_API", None) is None else settings.FIREBASE_PW_RESET_API

                payload = {
                    'requestType': 'PASSWORD_RESET',
                    'email': email_address
                }
                response = requests.post(reset_url, json=payload)
                response.raise_for_status()  # Raise an error for bad responses
            else:

                link = auth.generate_password_reset_link(email_address)

                custom_url = getattr(settings, "KEYSTONE_CUSTOM_PASSWORD_RESET_URL", None)

                if custom_url:
                    reset_link = f"{custom_url}?oobCode={link.split('oobCode=')[1]}"
                else:
                    reset_link = link

                subject = getattr(settings, "KEYSTONE_RESET_PASSWORD_EMAIL_SUBJECT", "Reset your Keystone password")
                text_template = getattr(settings, "KEYSTONE_RESET_PASSWORD_EMAIL_TEXT_TEMPLATE", f"To reset your password, click the following link: {reset_link}\nIf you did not request a password reset, you can ignore this email.")
                email_template = render_to_string('email/password_reset.html', {'reset_link': reset_link})

                send_mail(
                    subject,
                    text_template,
                    settings.DEFAULT_FROM_EMAIL,
                    [email_address],
                    html_message=email_template,)
                
            return JsonResponse({
                'success': True,
                'message': 'Password reset link generated and sent to email',
                'data': {} }, status=200)

        # error handling when using Firebase Admin SDK to get pasword reset link.
        except auth.UserNotFoundError:
            return JsonResponse({
                'success': False,
                'message': 'Password reset link generated and sent to email',
                'data': {} }, status=200)

        except requests.exceptions.HTTPError as http_err:
            return JsonResponse(
                {'success': False,
                'message': 'Password reset link generated and sent to email',
                'data': {} }, status=200)
        
        except Exception as e:
            return JsonResponse(
                {'success': False,
                'message': 'An unknown error occurred while generating password reset link',
                'data': {} }, status=500)