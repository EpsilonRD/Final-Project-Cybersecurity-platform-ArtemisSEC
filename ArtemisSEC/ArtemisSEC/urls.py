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

#temporal view 
def placeholder_view(request):
    return HttpResponse("Web site underconstruction")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  # Authentication App Urls 
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  #  logout
    path('home/', placeholder_view, name="home"), #home url
    path('scan-now/', placeholder_view, name="scan_now"), #scan now url
    path('news/', placeholder_view, name="news"), # news urls
]
