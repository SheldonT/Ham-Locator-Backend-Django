from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from datetime import datetime
from hamlocator.models import Logs
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin
from hamlocator.serializers import LogSerializer

class GetLogView(AuthRequiredMixin, View):

    #TODO: Add filtering by date range and/or location
    #TODO: Add option to get log stats (total number by country, etc.)
    def get(self, request):

        authenticated_user = request.user

        try:
            page = int(request.GET.get('page', 1))
            page_size = min(int(request.GET.get('page_size', 20)), 1000)  # Limit page size to 1000. Temporary solution until we implement cursor-based pagination on frontend.
            descend = request.GET.get('descend', 'true').lower() == 'true'
        except ValueError:  
            return JsonResponse({
                'success': False,
                'message': 'Invalid pagination parameters',
                'data': {}}, status=400)
        
        if page < 1 or page_size < 1:
            return JsonResponse({
                'success': False,
                'message': 'Page and page_size must be positive integers',
                'data': {}
            }, status=400)
        
        offset = (page - 1) * page_size

        if descend:
            order_by = ['-contact_date', '-contact_time']
        else:
            order_by = ['contact_date', 'contact_time']

        records = Logs.objects.filter(user_id=authenticated_user.userid).order_by(*order_by)[offset:offset + page_size]

        total_count = Logs.objects.filter(user_id=authenticated_user.userid).count()

        serializer = LogSerializer(records, many=True)
        records_data = serializer.data

        return JsonResponse({
            'success': True,
            'message': f'Retrieved {len(records_data)} records',
            'data': {
                'records': records_data,
                'total_count': total_count,
                'page': page,
                'page_size': page_size,
            }
        })