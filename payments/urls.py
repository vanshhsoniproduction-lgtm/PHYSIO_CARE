from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<int:appointment_id>/', views.payment_initiate, name='initiate'),
    path('verify/', views.payment_verify, name='verify'),
]