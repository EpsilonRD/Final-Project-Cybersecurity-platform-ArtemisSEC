from django.contrib import admin

# Register your models here.

from .models import ScanResult

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'user', 'scan_id', 'status', 'positives', 'total', 'created_at')
    list_filter = ('status', 'user', 'created_at')
    search_fields = ('file_name', 'scan_id', 'user__username')
    readonly_fields = ('scan_results', 'file_properties', 'permalink', 'vt_analysis_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False