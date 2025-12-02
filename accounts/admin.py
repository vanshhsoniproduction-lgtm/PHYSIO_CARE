from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'gender', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('gender', 'created_at')
