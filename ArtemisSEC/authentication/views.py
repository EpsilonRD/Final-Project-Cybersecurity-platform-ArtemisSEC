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
    form_class = CustomUserCreationForm  # Custom Form 
    success_url = reverse_lazy('login')  # Rediret to login view after register 

    def form_valid(self, form):
        # Save new User 
        response = super().form_valid(form)
        messages.success(self.request, "Successful registration! Now you can log in.")
        return response 

# Generic login view using  LoginView
class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('welcome')  # Welcome Website after Login 

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url

class WelcomeView(TemplateView):
    template_name = 'authentication/welcome.html'

# When user login 
@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    user.last_login = now()
    user.save()

# When user close section 
@receiver(user_logged_out)
def update_last_logout(sender, request, user, **kwargs):
    user.last_login = None  
    user.save()


# View to edit the profile 
class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'authentication/profile_settings.html'
    success_url = reverse_lazy('profile-settings')  # Redirect to after change 

    def get_object(self):
        # Return the user who is doing the Request 
        return self.request.user

    def form_valid(self, form):
        # If form is valid save susscefully 
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)

# View to change password 
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'authentication/change_password.html'
    success_url = reverse_lazy('profile-settings')

    def form_valid(self, form):
        # When password is changed still keep user section Note: This policy might be changed in the future
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been updated successfully!')
        return super().form_valid(form)
