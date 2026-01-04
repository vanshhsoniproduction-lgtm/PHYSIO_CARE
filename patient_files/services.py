import cloudinary.uploader
import cloudinary.utils
from django.conf import settings

def upload_patient_file(file_obj, patient, appointment_id=None, slot_id=None):
    """
    Uploads file to Cloudinary. Uses chunked upload for videos.
    """
    
    # 1. Determine Type
    mime_type = file_obj.content_type
    
    # Defaults
    resource_type = 'raw' 
    folder_type = 'documents'
    
    if mime_type.startswith('image/'):
        resource_type = 'image'
        folder_type = 'images'
    elif mime_type.startswith('video/'):
        resource_type = 'video'
        folder_type = 'videos'
    
    # 2. Build Path
    appt_folder_name = str(appointment_id) if appointment_id else f"pending_slot_{slot_id}"
    folder_path = f"physio-care/patients/{patient.id}_{patient.user.username}/appointments/{appt_folder_name}/{folder_type}"

    # 3. Base Options
    options = {
        "folder": folder_path,
        "resource_type": resource_type,
        "public_id": file_obj.name.split('.')[0], 
        "unique_filename": True,
        "overwrite": False
    }

    # 4. Upload Logic
    response = None

    if resource_type == 'image':
        options["quality"] = "auto"
        options["fetch_format"] = "auto"
        options["width"] = 2000 
        options["crop"] = "limit"
        response = cloudinary.uploader.upload(file_obj, **options)
        
    elif resource_type == 'video':
        # FIX: Use upload_large for videos to prevent timeouts/memory issues
        # Chunk size 6MB (balanced for speed/reliability)
        options["resource_type"] = "video"
        options["chunk_size"] = 6000000 
        options["eager"] = [
            {"quality": "auto", "fetch_format": "auto", "width": 1280, "crop": "limit"}
        ]
        options["eager_async"] = True 
        
        # Using upload_large automatically handles chunking
        response = cloudinary.uploader.upload_large(file_obj, **options)
        
    else:
        # Documents (Raw)
        response = cloudinary.uploader.upload(file_obj, **options)

    # 5. Return Data
    return {
        'url': response.get('secure_url'),
        'public_id': response.get('public_id'),
        'format': response.get('format'),
        'resource_type': resource_type 
    }