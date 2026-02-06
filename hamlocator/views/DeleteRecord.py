from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from hamlocator.models import Logs
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin

class DeleteRecordView(AuthRequiredMixin, View):
    def delete(self, request, record_id=None):
        
        authenticated_user = request.user

        if not record_id:
            return JsonResponse({
                'success': False,
                'message': 'Record ID is required',
                'data': {}}, status=400)

        try:
            record = Logs.objects.get(record_id=record_id, user_id=authenticated_user.userid)
        except Logs.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Record not found, or request unauthorized',
                'data': {}}, status=404)

        record.delete()

        return JsonResponse({
            'success': True,
            'message': 'Record deleted successfully',
            'data': {}}, status=200)