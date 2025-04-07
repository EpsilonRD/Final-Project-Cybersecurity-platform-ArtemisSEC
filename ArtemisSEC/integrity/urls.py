from django.urls import path
from .views import IntegrityCheckView
from .views import IntegrityCheckView, IntegrityHistoryView

app_name = 'integrity'  # Namespace de la aplicación
urlpatterns = [
    path('', IntegrityCheckView.as_view(), name='integrity_check'),
    path('history/', IntegrityHistoryView.as_view(), name='integrity_history'),
]