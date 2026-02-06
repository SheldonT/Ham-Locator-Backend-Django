
from django.urls import path
from hamlocator.views.CreateRecord import CreateRecordView
from hamlocator.views.GetRecord import GetRecordView
from hamlocator.views.EditRecord import EditRecordView
from hamlocator.views.GetLog import GetLogView
from hamlocator.views.DeleteRecord import DeleteRecordView
from hamlocator.views.ExportLog import ExportLogView

# Ham Locator specific URLs will go here
urlpatterns = [
    path('', GetLogView.as_view()),  # Default to GetLogView for base path
    path('addrecord/', CreateRecordView.as_view()),
    path('getrecord/', GetRecordView.as_view()),
    path('editrecord/', EditRecordView.as_view()),
    path('deleterecord/<str:record_id>/', DeleteRecordView.as_view()),
    path('exportlog/<str:format>/', ExportLogView.as_view()),
]
