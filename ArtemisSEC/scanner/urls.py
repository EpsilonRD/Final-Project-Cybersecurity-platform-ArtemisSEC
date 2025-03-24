from django.urls import path
from . import views

app_name = 'scanner'  # Define el namespace
urlpatterns = [
    path('', views.index, name='index'),                    # /scanner/
    path('scanner/', views.index, name='scanner'),          # /scanner/scanner/
    path('upload/', views.upload_file, name='upload_file'), # /scanner/upload/
    path('result/<str:scan_id>/', views.get_scan_result, name='get_scan_result'), # /scanner/result/<scan_id>/
    path('history/', views.get_scan_history, name='get_scan_history'),  # /scanner/history/
]