from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from django.contrib import messages

def landing_page(request):
    # Calculate specific dates: Today, Tomorrow, Day After
    today = timezone.now().date()
    dates = [
        {'value': today.strftime('%Y-%m-%d'), 'label': 'Today'},
        {'value': (today + timedelta(days=1)).strftime('%Y-%m-%d'), 'label': 'Tomorrow'},
        {'value': (today + timedelta(days=2)).strftime('%Y-%m-%d'), 'label': 'Day After Tomorrow'},
    ]

    # Generate Time Slots (09:00 to 17:00)
    time_slots = []
    for hour in range(9, 18): # 9 AM to 5 PM
        time_slots.append(f"{hour:02d}:00")

    if request.method == "POST":
        name = request.POST.get('full-name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        symptoms = request.POST.get('message')

        # Save to Database
        appointment = Appointment(
            name=name,
            phone_number=phone,
            date=date,
            time_slot=time,
            symptoms=symptoms
        )
        appointment.save()
        
        # You might want to add a success message logic here or redirect
        return render(request, "core/landing.html", {
            "dates": dates, 
            "time_slots": time_slots,
            "success": True # Flag to show success popup/message
        })

    return render(request, "core/landing.html", {"dates": dates, "time_slots": time_slots})