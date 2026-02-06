from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import json
from datetime import datetime
from hamlocator.models import Logs
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin

class EditRecordView(AuthRequiredMixin, View):
    def post(self, request):
        
        authenticated_user = request.user
        data = json.loads(request.body)
        rid = data.get('recordId')

        field_mapping = {
            'recordId': 'record_id',
            'contactCall': 'contact_call',
            'freq': 'freq',
            'mode': 'mode',
            'sigRepSent': 'sig_rep_sent',
            'sigRepRecv': 'sig_rep_recv',
            'name': 'name',
            'grid': 'grid',
            'serialSent': 'serial_sent',
            'serialRecv': 'serial_recv',
            'comment': 'comment',
            'lat': 'lat',
            'lng': 'lng',
            'country': 'country',
            'details': 'details',
            # removed from mapping as handled separately
            # 'contactDate': 'contact_date',
            # 'contactTime': 'contact_time',
            'utc': 'utc',
        }

        if not rid:
            return JsonResponse({
                'success': False,
                'message': 'Record ID is required to edit a record',
                'data': {}}, status=400)

        try:
            record = Logs.objects.get(record_id=rid, user_id=authenticated_user.userid)
        except Logs.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Record not found, or request unauthorized',
                'data': {}}, status=404)

        #convert and validate the date and time fields.
        try:
            contact_date = None
            contact_time = None

            if 'contactDate' in data:
                contact_date = datetime.strptime(data['contactDate'], '%Y-%m-%d').date()
                record.contact_date = contact_date
                data.pop('contactDate')  # Remove to avoid overwriting later

            if 'contactTime' in data:
                contact_time = datetime.strptime(data['contactTime'], '%H:%M:%S').time()
                record.contact_time = contact_time
                data.pop('contactTime')  # Remove to avoid overwriting later

        except ValueError as e:
            return JsonResponse({
                'success': False,
                'message': f'Invalid date or time format when submitted with edited record: {str(e)}',
                'data': {}}, status=400)
        
        for request_key, model_field in field_mapping.items():
            if request_key in ['contactDate', 'contactTime']:
                continue  # Handled separately
            if request_key in data:
                setattr(record, model_field, data[request_key])

        try:

            record.full_clean()  # Validate the model fields

            record.save()
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error updating record: {str(e)}',
                'data': {}}, status=500)

        return JsonResponse({"success": True,
                             "message": "Record updated successfully",
                             "data": {"record_id": record.record_id}}, status=200)