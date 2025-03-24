from django.db import models
from django.conf import settings

class ScanResult(models.Model):
    file_name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )
    scan_id = models.CharField(max_length=36, unique=True)  # UUID 
    file_hash = models.CharField(max_length=64, null=True, blank=True)  # SHA-256 
    vt_analysis_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    positives = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    permalink = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scan_results = models.JSONField(null=True, blank=True)
    file_properties = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.file_name} - {self.status}"