from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Define qué campos se mostrarán en la lista de usuarios en el panel de administración
    exclude = ('last_login', 'registration_date',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'academic_level', 'is_staff', 'is_active')
    list_filter = ('academic_level', 'is_staff', 'is_active', 'registration_date')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Sección para editar los detalles del usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'academic_level')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Sección de los campos al agregar un nuevo usuario desde el panel de administración
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'birth_date', 'academic_level', 'password1', 'password2')}
        ),
    )

    ordering = ('username',)

# Registrar el modelo con la configuración personalizada
admin.site.register(CustomUser, CustomUserAdmin)