from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from .models import PatientFile
from accounts.models import Patient
import cloudinary
import cloudinary.utils
import time

@login_required
def get_upload_signature(request):
    """
    Step 1: Frontend asks for a secure signature to upload directly to Cloudinary.
    """
    patient = getattr(request.user, 'patient', None)
    if not patient:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Get params from request
    folder_type = request.GET.get('folder_type', 'documents') # images/videos/documents
    slot_id = request.GET.get('slot_id')
    appointment_id = request.GET.get('appointment_id')
    
    # Construct Folder Path
    appt_folder_name = str(appointment_id) if appointment_id else f"pending_slot_{slot_id}"
    folder_path = f"physio-care/patients/{patient.id}_{patient.user.username}/appointments/{appt_folder_name}/{folder_type}"

    timestamp = int(time.time())

    # Params to sign
    params_to_sign = {
        "timestamp": timestamp,
        "folder": folder_path,
        "source": "uw", # upload widget / direct
    }

    # Add transformations for videos/images to sign them too
    if folder_type == 'videos':
        params_to_sign["eager"] = "q_auto,f_auto,w_1280,c_limit"
        params_to_sign["eager_async"] = True
    elif folder_type == 'images':
        params_to_sign["quality"] = "auto"
        params_to_sign["fetch_format"] = "auto"

    # Generate Signature
    signature = cloudinary.utils.api_sign_request(params_to_sign, settings.CLOUDINARY_STORAGE['API_SECRET'])

    return JsonResponse({
        'signature': signature,
        'timestamp': timestamp,
        'api_key': settings.CLOUDINARY_STORAGE['API_KEY'],
        'cloud_name': settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        'folder': folder_path,
        'eager': params_to_sign.get('eager', None)
    })

@login_required
@require_POST
def save_file_metadata(request):
    """
    Step 2: Frontend calls this AFTER successful upload to Cloudinary.
    """
    patient = getattr(request.user, 'patient', None)
    if not patient:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    title = request.POST.get('title')
    url = request.POST.get('url')
    public_id = request.POST.get('public_id')
    resource_type = request.POST.get('resource_type')
    slot_id = request.POST.get('slot_id')
    appointment_id = request.POST.get('appointment_id')

    if not all([title, url, public_id, resource_type]):
        return JsonResponse({'error': 'Missing data'}, status=400)

    # Map resource_type to model choices
    file_type = 'document'
    if resource_type == 'image': file_type = 'image'
    elif resource_type == 'video': file_type = 'video'

    # Save to DB
    p_file = PatientFile.objects.create(
        patient=patient,
        appointment_id=appointment_id if appointment_id else None,
        temp_slot_id=slot_id if not appointment_id else None,
        title=title,
        file_url=url,
        public_id=public_id,
        file_type=file_type
    )

    return JsonResponse({
        'id': p_file.id,
        'title': p_file.title,
        'type': p_file.file_type
    })

# ... delete_file aur list_files views same rahenge ...
@login_required
@require_POST
def delete_file(request, file_id):
    # (Pichle code wala logic same rahega)
    patient = getattr(request.user, 'patient', None)
    p_file = get_object_or_404(PatientFile, id=file_id)
    if patient and p_file.patient != patient:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Cloudinary se bhi delete kar sakte hain (Optional)
    p_file.delete()
    return JsonResponse({'success': True})

@login_required
def list_files(request, patient_id=None):
    # (Pichle code wala logic same rahega)
    if patient_id and request.user.is_staff:
        target_patient = get_object_or_404(Patient, id=patient_id)
    else:
        target_patient = getattr(request.user, 'patient', None)
        if not target_patient:
            return redirect('appointments:home')
            
    files = PatientFile.objects.filter(patient=target_patient).order_by('-uploaded_at')
    context = {'files': files, 'target_patient': target_patient, 'is_admin': request.user.is_staff}
    return render(request, 'patient_files/file_list.html', context)