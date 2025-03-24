from django.urls import path
from . import views
from .views import ScanView
urlpatterns = [
    path('', ScanView.as_view(), name='scan_ip_domain'),
    path('scan-ip-domain/history/', views.ScanHistoryView.as_view(), name='scan_ip_domain_history'),
    #path('', views.ScanView.as_view(), name='scan_ip_domain'),
    #path('results/<int:pk>/', views.ScanResultsView.as_view(), name='scan_ip_domain_results'),
]