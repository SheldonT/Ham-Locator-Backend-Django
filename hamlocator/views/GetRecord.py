from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from datetime import datetime
from hamlocator.models import Logs
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin
from hamlocator.serializers import LogSerializer

class GetRecordView(AuthRequiredMixin, View):
    def get(self, request):
        
        authenticated_user = request.user
        rid = request.GET.get('rid')
        
        if not rid:
            return JsonResponse({
                'success': False,
                'message': 'Record ID is required',
                'data': {}}, status=400)

        try:
            record = Logs.objects.get(record_id=rid, user_id=authenticated_user.userid)
        except Logs.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Record not found, or request unauthorized',
                'data': {}}, status=404)

        serializer = LogSerializer(record)
        record_data = serializer.data

        return JsonResponse({
            'success': True,
            'message': 'Record retrieved successfully',
            'data': record_data}, status=200)