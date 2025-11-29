from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from core.models import Appointment

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'adminpanel/login.html', {'form': form})

@login_required
def admin_dashboard(request):
    # Get all appointments, ordered by date and time
    appointments = Appointment.objects.all().order_by('-date', 'time_slot')
    return render(request, 'adminpanel/dashboard.html', {'appointments': appointments})

@login_required
def mark_completed(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'COMPLETED'
    appointment.save()
    return redirect('admin_dashboard')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')