from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('mark-completed/<int:appointment_id>/', views.mark_completed, name='mark_completed'),
    path('logout/', views.admin_logout, name='admin_logout'),
]