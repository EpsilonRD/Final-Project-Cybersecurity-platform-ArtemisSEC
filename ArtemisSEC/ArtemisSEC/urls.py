"""
URL configuration for ArtemisSEC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

# Temporal view 
def placeholder_view(request):
    return HttpResponse("Web site under construction")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  # Authentication App Urls
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Logout
    #path('', placeholder_view, name="home"),  # Home URL (/)
    path('scan-now/', placeholder_view, name="scan_now"),  # Scan now URL
    #path('news/', placeholder_view, name="news"),  # News URL
    path('scanner/', include('scanner.urls')),  # Scanner URLs /scanner/
    path('scan-ip-domain/', include('scan_ip_domain.urls')),  # App scan ip domain /scan-ip-domain/
    path('integrity/', include('integrity.urls')),
    path('', include('news.urls')), #News APP 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
