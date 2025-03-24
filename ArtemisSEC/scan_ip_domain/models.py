from django.db import models

# Create your models here.
from django.db import models

class ScanResult(models.Model):
    target = models.CharField(max_length=255)  # IP or DOMAIN
    is_suspicious = models.BooleanField(default=False)
    details = models.TextField(blank=True, null=True)
    scan_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.target} - {'Suspicious' if self.is_suspicious else 'Clean'}"