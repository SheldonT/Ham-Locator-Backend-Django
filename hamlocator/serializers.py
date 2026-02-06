from rest_framework import serializers
from hamlocator.models import Logs

class LogSerializer(serializers.ModelSerializer):

    # Map JSON key "contactCall" to model field "contact_call"
    # Everything coming from the frontend uses camelCase
    recordId = serializers.CharField(source='record_id')
    userId = serializers.CharField(source='user_id', max_length=255, allow_blank=False, allow_null=False)
    contactCall = serializers.CharField(source='contact_call', max_length=255, allow_blank=False, allow_null=False)
    sigRepSent = serializers.IntegerField(source='sig_rep_sent', allow_null=True)
    sigRepRecv = serializers.IntegerField(source='sig_rep_recv', allow_null=True)
    serialSent = serializers.IntegerField(source='serial_sent', allow_null=True)
    serialRecv = serializers.IntegerField(source='serial_recv', allow_null=True)
    contactDate = serializers.DateField(source='contact_date', allow_null=False)
    contactTime = serializers.TimeField(source='contact_time', allow_null=False)
    utc = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Logs
        #fields = '__all__'
        fields = ['recordId', 'userId', 'contactCall', 'freq', 'mode',
                  'sigRepSent', 'sigRepRecv', 'name', 'grid', 
                  'serialSent', 'serialRecv', 'comment', 'lat', 'lng',
                  'country', 'details', 'contactDate', 'contactTime', 'utc']