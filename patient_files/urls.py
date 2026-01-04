from django.urls import path
from . import views

app_name = 'patient_files'

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    path('view/', views.list_files, name='my_files'), # For patient
    path('view/<int:patient_id>/', views.list_files, name='admin_view_files'), # For admin
]