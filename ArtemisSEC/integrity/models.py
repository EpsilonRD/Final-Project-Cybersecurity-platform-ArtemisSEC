from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class IntegrityCheck(models.Model):
    file_name = models.CharField(max_length=255)
    calculated_hash = models.CharField(max_length=64)  # Longitud máxima para SHA-256
    reference_hash = models.CharField(max_length=64)
    algorithm = models.CharField(max_length=10, choices=[('md5', 'MD5'), ('sha256', 'SHA-256')])
    timestamp = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField()

    def __str__(self):
        return f"{self.file_name} ({self.timestamp})"