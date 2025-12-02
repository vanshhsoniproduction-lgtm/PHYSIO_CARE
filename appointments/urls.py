from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.home, name='home'),
    path('recent/', views.recent_appointments, name='recent'),
    path('profile/', views.profile, name='profile'),
    path('book/date/', views.booking_date, name='booking_date'),
    path('book/slots/', views.booking_slots, name='booking_slots'),
    path('book/confirm/<int:slot_id>/', views.booking_confirm, name='booking_confirm'),
]