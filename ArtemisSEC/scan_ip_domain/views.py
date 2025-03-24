import socket
import requests
import os
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django import forms
from .models import ScanResult
import logging
from django.views import View
from django.conf import settings 

logger = logging.getLogger(__name__)

ABUSEIPDB_API_KEY = settings.ABUSEIPDB_API_KEY

class ScanForm(forms.Form):
    target = forms.CharField(max_length=255, label="IP or Domain")

class ScanView(LoginRequiredMixin, FormView):
    template_name = 'scan_ip_domain/scan.html'
    form_class = ScanForm
    success_url = reverse_lazy('scan_ip_domain_results')

    def form_valid(self, form):
        target = form.cleaned_data['target']
        logger.info(f"Received target: {target}")

        # Resolve IP or DOMAIN 
        try:
            ip_address = socket.gethostbyname(target)
            logger.info(f"Resolved IP: {ip_address}")
        except socket.gaierror as e:
            logger.error(f"Could not resolve domain to IP: {str(e)}")
            return JsonResponse({'error': 'Could not resolve domain to IP'})

        # AbuseIPDB Request
        abuse_url = 'https://api.abuseipdb.com/api/v2/check'
        abuse_headers = {'Key': ABUSEIPDB_API_KEY, 'Accept': 'application/json'}
        abuse_params = {'ipAddress': ip_address, 'maxAgeInDays': 90}
        try:
            abuse_response = requests.get(abuse_url, headers=abuse_headers, params=abuse_params)
            logger.info(f"AbuseIPDB response status: {abuse_response.status_code}")
        except Exception as e:
            logger.error(f"Error contacting AbuseIPDB: {str(e)}")
            return JsonResponse({'error': f"Error contacting AbuseIPDB: {str(e)}"})

        if abuse_response.status_code != 200:
            logger.error(f"AbuseIPDB API Error: Status {abuse_response.status_code} - {abuse_response.text}")
            return JsonResponse({
                'error': f"API Error: Status {abuse_response.status_code} - {abuse_response.text}"
            })

        abuse_data = abuse_response.json()
        if 'data' not in abuse_data:
            logger.error(f"Unexpected API response: {abuse_response.text}")
            return JsonResponse({
                'error': f"Unexpected API response: {abuse_response.text}"
            })

        # Extract all 
        data = abuse_data['data']
        is_suspicious = data['abuseConfidenceScore'] > 50
        logger.info(f"Abuse Confidence Score: {data['abuseConfidenceScore']} - Suspicious: {is_suspicious}")

        # Save in the database 
        scan_result = ScanResult.objects.create(
            target=target,
            is_suspicious=is_suspicious,
            details=f"Resolved IP: {ip_address}\nAbuse Confidence Score: {data['abuseConfidenceScore']}%"
        )

        # JSON answer 
        response_data = {
            'id': scan_result.id,  # ID for the historial 
            'target': target,
            'is_suspicious': is_suspicious,
            'details': {
                'resolved_ip': ip_address,
                'is_public': 'Yes' if data['isPublic'] else 'No',
                'ip_version': data['ipVersion'],
                'is_whitelisted': 'Yes' if data['isWhitelisted'] else 'No',
                'abuse_score': data['abuseConfidenceScore'],
                'country': f"{data.get('countryName', 'Unknown')} ({data.get('countryCode', 'N/A')})",
                'usage_type': data.get('usageType', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'domain': data.get('domain', 'None'),
                'hostnames': ', '.join(data.get('hostnames', [])) or 'None',
                'total_reports': data['totalReports'],
                'distinct_users': data['numDistinctUsers'],
                'last_reported': data.get('lastReportedAt', 'Never')
            }
        }

        logger.info(f"Returning response: {response_data}")
        return JsonResponse(response_data)

    def form_invalid(self, form):
        logger.error(f"Form invalid: {form.errors}")
        return JsonResponse({'error': 'Invalid input'}, status=400)

class ScanHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        
        # Get the current user's scans, sorted by descending date
        scans = ScanResult.objects.filter().order_by('-scan_date')[:10]  # Últimos 10 escaneos
        history_data = [
            {
                'id': scan.id,
                'target': scan.target,
                'is_suspicious': scan.is_suspicious,
                'scan_date': scan.scan_date.isoformat(),
            }
            for scan in scans
        ]
        return JsonResponse({'history': history_data})