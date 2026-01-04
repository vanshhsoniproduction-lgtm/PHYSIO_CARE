from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from .models import PatientFile
from .services import upload_patient_file
from accounts.models import Patient
import json

@login_required
def upload_file(request):
    """AJAX Upload View"""
    if request.method == 'POST':
        patient = getattr(request.user, 'patient', None)
        if not patient:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        title = request.POST.get('title')
        file_obj = request.FILES.get('file')
        slot_id = request.POST.get('slot_id') # For pending appointments
        appointment_id = request.POST.get('appointment_id') # For existing appointments

        if not file_obj or not title:
            return JsonResponse({'error': 'Missing file or title'}, status=400)

        # SERVER-SIDE VALIDATION
        # Size limits: 9MB (Image/Doc), 90MB (Video)
        file_size_mb = file_obj.size / (1024 * 1024)
        mime = file_obj.content_type
        
        is_video = mime.startswith('video/')
        limit = 90 if is_video else 9

        if file_size_mb > limit:
            return JsonResponse({'error': f'File too large. Limit is {limit}MB.'}, status=400)
        
        # Doc logic: Reject > 9MB (Images/Videos are compressed by Cloudinary, but we check raw size first)
        if not is_video and not mime.startswith('image/') and file_size_mb > 9:
             return JsonResponse({'error': 'Documents must be under 9MB.'}, status=400)

        try:
            # Upload to Cloudinary
            data = upload_patient_file(file_obj, patient, appointment_id, slot_id)
            
            # Save to DB
            p_file = PatientFile.objects.create(
                patient=patient,
                appointment_id=appointment_id if appointment_id else None,
                temp_slot_id=slot_id if not appointment_id else None,
                title=title,
                file_url=data['url'],
                public_id=data['public_id'],
                file_type=data['resource_type']
            )
            
            return JsonResponse({
                'id': p_file.id,
                'title': p_file.title,
                'url': p_file.file_url,
                'type': p_file.file_type
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@require_POST
def delete_file(request, file_id):
    """AJAX Delete View"""
    patient = getattr(request.user, 'patient', None)
    
    # Allow patient owner OR admin
    p_file = get_object_or_404(PatientFile, id=file_id)
    
    if patient and p_file.patient != patient:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    if not patient and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Note: We keep file in Cloudinary or delete it? 
    # For now, just delete DB record to act as "soft delete" or implement cloudinary destroy.
    # Implementing destroy for cleanliness:
    import cloudinary.uploader
    try:
        cloudinary.uploader.destroy(p_file.public_id, resource_type="video" if p_file.file_type == 'video' else "image")
    except:
        pass # Ignore cloudinary errors

    p_file.delete()
    return JsonResponse({'success': True})

@login_required
def list_files(request, patient_id=None):
    """
    View for viewing files. 
    If patient_id provided (and user is staff), show that patient's files.
    Otherwise show current user's files.
    """
    if patient_id and request.user.is_staff:
        target_patient = get_object_or_404(Patient, id=patient_id)
    else:
        target_patient = getattr(request.user, 'patient', None)
        if not target_patient:
            return redirect('appointments:home')
            
    # Group by date logic can be done in template or here. 
    # Let's send QuerySet ordered by date.
    files = PatientFile.objects.filter(patient=target_patient).order_by('-uploaded_at')
    
    context = {
        'files': files,
        'target_patient': target_patient,
        'is_admin': request.user.is_staff
    }
    return render(request, 'patient_files/file_list.html', context)