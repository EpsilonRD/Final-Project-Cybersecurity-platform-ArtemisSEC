from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CustomUser

User = get_user_model() 

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')
    academic_level = forms.ChoiceField(choices=User._meta.get_field('academic_level').choices, label='Academic Level')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'academic_level', 'password1', 'password2')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError('Birth date cannot be in the future.')
        return birth_date

from django.contrib.auth.forms import PasswordChangeForm

class PasswordChangeFormCustom(PasswordChangeForm):
    # This class is for modified the form of change password if need it .
    pass


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'academic_level')