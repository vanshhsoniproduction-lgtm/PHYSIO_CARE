from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('dashboard/', views.home, name='home'),
    path('patients/', views.patients, name='patients'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('payments/', views.payments, name='payments'),
    path('reviews/', views.reviews, name='reviews'),
    path('settings/', views.settings, name='settings'),
    
    # Actions
    path('appointment/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('appointment/update-fee/<int:appointment_id>/', views.update_fee, name='update_fee'),
    path('appointment/mark-paid/<int:appointment_id>/', views.mark_paid, name='mark_paid'),
    
    path('review/approve/<int:review_id>/', views.approve_review, name='approve_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    # AJAX / HTMX
    path('api/get-slots/', views.get_slots_for_date, name='get_slots'),
    path('book/<int:patient_id>/', views.doctor_book_appointment, name='doctor_book'),
]