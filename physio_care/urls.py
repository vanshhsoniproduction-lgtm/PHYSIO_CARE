from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('custom-admin/', include('adminpanel.urls')),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('files/', include('patient_files.urls')),
    path('payments/', include('payments.urls')), # NEW: Payments App
]