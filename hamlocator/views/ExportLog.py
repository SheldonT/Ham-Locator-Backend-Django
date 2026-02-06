from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from hamlocator.models import Logs
from keystone.mixins.FirebaseAuthRequiredMixin import  FirebaseAuthRequiredMixin as AuthRequiredMixin
from hamlocator.serializers import LogSerializer

class ExportLogView(AuthRequiredMixin, View):

    band_def = [
        { "band": "2200m", "low": 0.1357, "high": 0.1378 },
        { "band": "160m", "low": 1.8, "high": 2 },
        { "band": "80m", "low": 3.5, "high": 4 },
        { "band": "40m", "low": 7, "high": 7.3 },
        { "band": "30m", "low": 10.1, "high": 10.15 },
        { "band": "20m", "low": 14, "high": 14.35 },
        { "band": "17m", "low": 18.068, "high": 18.168 },
        { "band": "15m", "low": 21, "high": 21.45 },
        { "band": "12m", "low": 24.89, "high": 24.99 },
        { "band": "10m", "low": 28, "high": 29.7 },
        { "band": "6m", "low": 50, "high": 54 },
        { "band": "2m", "low": 144, "high": 148 },
        { "band": "1.35m", "low": 222, "high": 225 },
        { "band": "70cm", "low": 430, "high": 450 },
    ]
    
    def get(self, request, format=None):

        authenticated_user = request.user

        records = Logs.objects.filter(user_id=authenticated_user.userid).order_by('contact_date', 'contact_time')

        serializer = LogSerializer(records, many=True)
        records_data = serializer.data

        if format == 'adif':
            adif_record = self.toADIF(records_data)
        elif format == 'csv':
            adif_record = self.toCSV(records_data)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid format specified. Use "adif" or "csv".',
                'data': {}}, status=400)


        response = HttpResponse(adif_record, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="hamlocator_log.adif"'
        return response
    
    def toADIF(self, log):

        timestamp = datetime.now().isoformat()

        adif_record =  f"Exported by Ham-Locator\n \
https://sheldont.github.io/Ham-Locator\n \
<ADIF_VER:5>3.1.0\n \
<CREATED_TIMESTAMP:{timestamp}> {timestamp}\n \
<PROGRAMID:11>Ham-Locator\n \
<PROGRAMVERSION:3>1.1\n \
<eoh>"
        
        for record in log:

            band_name = self.getBand(record['freq'])
            
            if record['contactCall']:
                adif_record += f"<CALL:{len(record['contactCall'])}>{record['contactCall']}"
            if record['contactDate']:
                adif_record += f"<QSO_DATE:{len(record['contactDate'])}>{record['contactDate']}"
            if record['contactTime']:
                adif_record += f"<TIME_ON:{len(record['contactTime'])}>{record['contactTime']}"
            
            adif_record += f"<BAND:{len(band_name)}>{band_name}"
            if record['freq']:
                adif_record += f"<FREQ:{len(str(record['freq']))}>{record['freq']}"
            if record['mode']:
                adif_record += f"<MODE:{len(record['mode'])}>{record['mode']}"
            if record['sigRepSent']:
                adif_record += f"<RST_SENT:{len(str(record['sigRepSent']))}>{record['sigRepSent']}"
            if record['sigRepRecv']:
                adif_record += f"<RST_RCVD:{len(str(record['sigRepRecv']))}>{record['sigRepRecv']}"
            if record['name']:
                adif_record += f"<NAME:{len(record['name'])}>{record['name']}"
            if record['country']:
                adif_record += f"<COUNTRY:{len(record['country'])}>{record['country']}"
            if record['grid']:
                adif_record += f"<GRID_SQUARE:{len(record['grid'])}>{record['grid']}"
            if record['serialSent']:
                adif_record += f"<STX:{len(str(record['serialSent']))}>{record['serialSent']}"
            if record['serialRecv']:
                adif_record += f"<SRX:{len(str(record['serialRecv']))}>{record['serialRecv']}"
            if record['comment']:
                adif_record += f"<COMMENT:{len(record['comment'])}>{record['comment']}"
            adif_record += "<EOR>\n"

        return adif_record
    
    def toCSV(self, log):

        csv_record = "CALL, QSO_DATE, TIME_ON, BAND, FREQ, MODE, RST_SENT, RST_RCVD, NAME, COUNTRY, GRID_SQUARE, STX, SRX, COMMENT\n"

        for record in log:

            band_name = self.getBand(record['freq'])
            
            csv_record += f"{record['contactCall']}, {record['contactDate']}, {record['contactTime']}, {band_name}, {record['freq']}, {record['mode']}, {record['sigRepSent']}, {record['sigRepRecv']}, {record['name']}, {record['country']}, {record['grid']}, {record['serialSent']}, {record['serialRecv']}, {record['comment']}\n"

        return csv_record
    
    def getBand(self, freq):

        for band in self.band_def:
            if float(freq) >= band['low'] and float(freq) <= band['high']:
                return band['band']
        
        return "UNKNOWN"