from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import UpdateView 
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class RegisterView(CreateView):
    template_name = 'authentication/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful! You can now log in.")
        return response

    def form_invalid(self, form):
        if 'password2' in form.errors:
            messages.error(self.request, "Passwords do not match. Please check them.")
        elif 'username' in form.errors:
            messages.error(self.request, "The username is already taken or invalid.")
        elif 'email' in form.errors:
            messages.error(self.request, "The email is already in use or invalid.")
        else:
            messages.error(self.request, "Please correct the errors in the form.")
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('welcome')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url

class WelcomeView(TemplateView):
    template_name = 'authentication/welcome.html'

@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    user.last_login = now()
    user.save()

@receiver(user_logged_out)
def update_last_logout(sender, request, user, **kwargs):
    user.last_login = None  
    user.save()

class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'authentication/profile_settings.html'
    success_url = reverse_lazy('profile-settings')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'authentication/change_password.html'
    success_url = reverse_lazy('profile-settings')
    form_class = PasswordChangeForm  # Usamos el formulario por defecto de Django

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show forms errors"""
        if 'old_password' in form.errors:
            messages.error(self.request, "The current password is incorrect.")
        elif 'new_password2' in form.errors:
            messages.error(self.request, "The new passwords do not match or do not meet the requirements.")
        else:
            messages.error(self.request, "Please correct the errors in the form.")
        return super().form_invalid(form)