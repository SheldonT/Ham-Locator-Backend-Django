from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import uuid
import json
from datetime import datetime
from hamlocator.models import Logs
from hamlocator.serializers import LogSerializer
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin

class CreateRecordView(AuthRequiredMixin, View):
    def post(self, request):
        
        authenticated_user = request.user
        data = json.loads(request.body)

        data["recordId"] = str(uuid.uuid4())
        data["userId"] = authenticated_user.userid

        print(data)

        log_serializer = LogSerializer(data=data)

        if log_serializer.is_valid():
            log_serializer.save()
            return JsonResponse({
                'success': True,
                'message': 'Record created successfully',
                'data': {"record_id": log_serializer.data['recordId']}}, status=201)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Data validation error creating record object',
                'data': log_serializer.errors}, status=400)

        #convert and validate the date and time fields.
        # try:
        #     contact_date = None
        #     contact_time = None

        #     if 'contactDate' in data:
        #         contact_date = datetime.strptime(data['contactDate'], '%Y-%m-%d').date()

        #     if 'contactTime' in data:
        #         contact_time = datetime.strptime(data['contactTime'], '%H:%M:%S').time()
        # except ValueError as e:
        #     return JsonResponse({
        #         'success': False,
        #         'message': f'Invalid date or time format when submitted with new record: {str(e)}',
        #         'data': {}}, status=400)

        # try:

        #     record = Logs(
        #         record_id=uuid.uuid4(),
        #         user_id=authenticated_user.userid,
        #         contact_call=data.get('contactCall'),
        #         freq=data.get('freq'),
        #         mode=data.get('mode'),
        #         sig_rep_sent=data.get('sigRepSent'),
        #         sig_rep_recv=data.get('sigRepRecv'),
        #         name=data.get('name'),
        #         grid=data.get('grid'),
        #         serial_sent=data.get('serialSent'),
        #         serial_recv=data.get('serialRecv'),
        #         comment=data.get('comment'),
        #         lat=data.get('lat'),
        #         lng=data.get('lng'),
        #         country=data.get('country'),
        #         details=data.get('details'),
        #         contact_date=contact_date,
        #         contact_time=contact_time,
        #         utc=data.get('utc'),
        #     )
        #     record.full_clean()  # Validate the model fields

        #     record.save()
        # except Exception as e:
        #     return JsonResponse({
        #         'success': False,
        #         'message': f'Data validation error creating record object: {str(e)}',
        #         'data': {}}, status=400)
        
        # return JsonResponse({
        #     'success': True,
        #     'message': 'Record created successfully',
        #     'data': {"record_id": record.record_id}}, status=201)