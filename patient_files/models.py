from django.db import models
from accounts.models import Patient
from appointments.models import Appointment

class PatientFile(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='files')
    # Nullable to allow uploads before appointment creation (linked via temp logic)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    
    title = models.CharField(max_length=255) # Custom name
    file_url = models.URLField(max_length=500)
    public_id = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    
    # Technical fields for tracking temp uploads
    temp_slot_id = models.IntegerField(null=True, blank=True, help_text="Used to link files during booking before appointment creation")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.patient.full_name})"

    class Meta:
        ordering = ['-uploaded_at']