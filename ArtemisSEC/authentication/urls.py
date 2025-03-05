from django.urls import path
from . import views
from .views import ProfileSettingsView, ChangePasswordView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('profile-settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]