import uuid
import hashlib
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ScanResult
import os
from django.conf import settings 

API_KEY = settings.VIRUSTOTAL_API_KEY
HEADERS = {"x-apikey": API_KEY}

@login_required
def index(request):
    return render(request, 'scanner/index.html')

@csrf_exempt
@login_required
def upload_file(request):
    if request.method != 'POST' or not request.FILES.get('file'):
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    uploaded_file = request.FILES['file']
    # Calculating the  hash SHA-256 of the file 
    sha256_hash = hashlib.sha256()
    for chunk in uploaded_file.chunks():
        sha256_hash.update(chunk)
    file_hash = sha256_hash.hexdigest()

    # Generating an unique scan_id
    scan_id = str(uuid.uuid4())

    # Verifying  if there is an register 
    try:
        scan = ScanResult.objects.get(file_hash=file_hash, user=request.user)
        if scan.status == 'completed':
            return JsonResponse({
                'success': True,
                'scan_id': scan.scan_id,
                'message': 'File already analyzed and stored'
            })
    except ScanResult.DoesNotExist:
        pass  # continuing if does not exits 

    # Verifying if virus total does have an analysis 
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        # Creating a register with the current data 
        scan = ScanResult.objects.create(
            file_name=uploaded_file.name,
            user=request.user,
            scan_id=scan_id,
            file_hash=file_hash
        )
        result = response.json()
        attributes = result.get('data', {}).get('attributes', {})
        stats = attributes.get('last_analysis_stats', {})
        scan.positives = stats.get('malicious', 0) + stats.get('suspicious', 0)
        scan.total = sum(stats.values())
        scan.permalink = f"https://www.virustotal.com/gui/file/{file_hash}"
        scan.scan_results = attributes.get('last_analysis_results', {})
        scan.file_properties = {
            'md5': attributes.get('md5'),
            'sha1': attributes.get('sha1'),
            'sha256': file_hash,
            'size_kb': attributes.get('size', 0) / 1024,
            'file_type': attributes.get('type_description')
        }
        scan.status = 'completed'
        scan.save()
        return JsonResponse({
            'success': True,
            'scan_id': scan_id,
            'message': 'File already analyzed by VirusTotal'
        })

    # Upload the file if there is no previous 
    scan = ScanResult.objects.create(
        file_name=uploaded_file.name,
        user=request.user,
        scan_id=scan_id,
        file_hash=file_hash
    )
    url = "https://www.virustotal.com/api/v3/files"
    uploaded_file.seek(0)
    files = {"file": (uploaded_file.name, uploaded_file)}
    try:
        response = requests.post(url, headers=HEADERS, files=files)
        response.raise_for_status()
        result = response.json()
        analysis_id = result.get('data', {}).get('id')
        if analysis_id:
            scan.vt_analysis_id = analysis_id
            scan.save()
            return JsonResponse({
                'success': True,
                'scan_id': scan_id,
                'message': 'File uploaded successfully'
            })
    except requests.exceptions.RequestException as e:
        scan.status = 'error'
        scan.save()
        return JsonResponse({
            'success': False,
            'message': f'Error uploading file: {str(e)}'
        })

@login_required
def get_scan_result(request, scan_id):
    try:
        scan = ScanResult.objects.get(scan_id=scan_id, user=request.user)
        if scan.status == 'completed':
            return JsonResponse({
                'success': True,
                'completed': True,
                'positives': scan.positives,
                'total': scan.total,
                'permalink': scan.permalink,
                'scan_results': scan.scan_results,
                'file_properties': scan.file_properties
            })

        #If not complete, checking the analysis status
        url = f"https://www.virustotal.com/api/v3/files/{scan.file_hash}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            result = response.json()
            attributes = result.get('data', {}).get('attributes', {})
            stats = attributes.get('last_analysis_stats', {})
            scan.positives = stats.get('malicious', 0) + stats.get('suspicious', 0)
            scan.total = sum(stats.values())
            scan.permalink = f"https://www.virustotal.com/gui/file/{scan.file_hash}"
            scan.scan_results = attributes.get('last_analysis_results', {})
            scan.file_properties = {
                'md5': attributes.get('md5'),
                'sha1': attributes.get('sha1'),
                'sha256': scan.file_hash,
                'size_kb': attributes.get('size', 0) / 1024,
                'file_type': attributes.get('type_description')
            }
            scan.status = 'completed'
            scan.save()
            return JsonResponse({
                'success': True,
                'completed': True,
                'positives': scan.positives,
                'total': scan.total,
                'permalink': scan.permalink,
                'scan_results': scan.scan_results,
                'file_properties': scan.file_properties
            })
        else:
# If the file has not yet been fully analyzed, check the current analysis
            if scan.vt_analysis_id:
                url = f"https://www.virustotal.com/api/v3/analyses/{scan.vt_analysis_id}"
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()
                result = response.json()
                attributes = result.get('data', {}).get('attributes', {})
                if attributes.get('status') == 'completed':
                    file_url = f"https://www.virustotal.com/api/v3/files/{scan.file_hash}"
                    file_response = requests.get(file_url, headers=HEADERS)
                    file_response.raise_for_status()
                    file_result = file_response.json()
                    file_attributes = file_result.get('data', {}).get('attributes', {})
                    stats = file_attributes.get('last_analysis_stats', {})
                    scan.positives = stats.get('malicious', 0) + stats.get('suspicious', 0)
                    scan.total = sum(stats.values())
                    scan.permalink = f"https://www.virustotal.com/gui/file/{scan.file_hash}"
                    scan.scan_results = file_attributes.get('last_analysis_results', {})
                    scan.file_properties = {
                        'md5': file_attributes.get('md5'),
                        'sha1': file_attributes.get('sha1'),
                        'sha256': scan.file_hash,
                        'size_kb': file_attributes.get('size', 0) / 1024,
                        'file_type': file_attributes.get('type_description')
                    }
                    scan.status = 'completed'
                    scan.save()
                    return JsonResponse({
                        'success': True,
                        'completed': True,
                        'positives': scan.positives,
                        'total': scan.total,
                        'permalink': scan.permalink,
                        'scan_results': scan.scan_results,
                        'file_properties': scan.file_properties
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f'Scan for {scan_id} still in progress, please try again later'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f'No analysis ID found for {scan_id}'
                })

    except ScanResult.DoesNotExist:
# If it does not exist in the database, try to get it directly from VirusTotal
        url = f"https://www.virustotal.com/api/v3/files/{scan_id}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            # I need to modified this funtion later 
            file_hash = scan_id
            scan = ScanResult.objects.create(
                scan_id=str(uuid.uuid4()),
                user=request.user,
                file_name="Unknown",
                file_hash=file_hash
            )
            result = response.json()
            attributes = result.get('data', {}).get('attributes', {})
            stats = attributes.get('last_analysis_stats', {})
            scan.positives = stats.get('malicious', 0) + stats.get('suspicious', 0)
            scan.total = sum(stats.values())
            scan.permalink = f"https://www.virustotal.com/gui/file/{file_hash}"
            scan.scan_results = attributes.get('last_analysis_results', {})
            scan.file_properties = {
                'md5': attributes.get('md5'),
                'sha1': attributes.get('sha1'),
                'sha256': file_hash,
                'size_kb': attributes.get('size', 0) / 1024,
                'file_type': attributes.get('type_description')
            }
            scan.status = 'completed'
            scan.save()
            return JsonResponse({
                'success': True,
                'completed': True,
                'positives': scan.positives,
                'total': scan.total,
                'permalink': scan.permalink,
                'scan_results': scan.scan_results,
                'file_properties': scan.file_properties
            })
        else:
            return JsonResponse({
                'success': False,
                'message': f'Scan with ID {scan_id} not found for this user or in VirusTotal'
            })
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'message': f'Error checking scan results: {str(e)}'
        })
    


#History View


@login_required
def get_scan_history(request):
    scans = ScanResult.objects.filter(user=request.user).order_by('-created_at')
    history = [
        {
            'file_name': scan.file_name,
            'status': scan.status,
            'created_at': scan.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'scan_id': scan.scan_id
        }
        for scan in scans
    ]
    return JsonResponse({'success': True, 'history': history})


