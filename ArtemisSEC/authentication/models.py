from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Last Login", auto_now=True)  # Nuevo campo
    
    ACADEMIC_LEVEL_CHOICES = [
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('other', 'Other'),
    ]
    academic_level = models.CharField(
        max_length=20, 
        choices=ACADEMIC_LEVEL_CHOICES, 
        default='student', 
        verbose_name="Academic Level"
    )

    # Add unique related_name for the fields causing conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique reverse accessor name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique reverse accessor name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
