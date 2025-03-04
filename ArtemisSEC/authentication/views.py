from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .forms import CustomUserCreationForm  # Asegúrate de importar el formulario personalizado
from .models import CustomUser

# Create your views here.

class RegisterView(CreateView):
    template_name = 'authentication/register.html'
    form_class = CustomUserCreationForm  # Usa el formulario personalizado
    success_url = reverse_lazy('login')  # Redirige a la vista de login después del registro

    def form_valid(self, form):
        # Guarda el nuevo usuario
        response = super().form_valid(form)
        messages.success(self.request, "Successful registration! Now you can log in.")
        return response 

# Vista de login utilizando la vista genérica LoginView
class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('welcome')  # Redirige a la página de bienvenida

    def get_success_url(self):
        return self.success_url

class WelcomeView(TemplateView):
    template_name = 'authentication/welcome.html'

# Cuando el usuario inicia sesión
@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    user.last_login = now()
    user.save()

# Cuando el usuario cierra sesión
@receiver(user_logged_out)
def update_last_logout(sender, request, user, **kwargs):
    user.last_login = None  # O puedes dejar el valor anterior
    user.save()
