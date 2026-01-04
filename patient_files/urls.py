from django.urls import path
from . import views

app_name = 'patient_files'

urlpatterns = [
    path('get-signature/', views.get_upload_signature, name='get_signature'), # NEW
    path('save-metadata/', views.save_file_metadata, name='save_metadata'),   # NEW
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    path('view/', views.list_files, name='my_files'),
    path('view/<int:patient_id>/', views.list_files, name='admin_view_files'),
]