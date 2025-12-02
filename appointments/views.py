from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Appointment, DailySlot, Review
from .utils import generate_slots_for_date, get_slot_suggestions
from datetime import datetime, timedelta

@login_required
def home(request):
    patient = request.user.patient
    today = timezone.now().date()
    
    # Today's Meetings
    today_appointments = Appointment.objects.filter(
        patient=patient,
        slot__date=today,
        status__in=['PENDING', 'CONFIRMED', 'CANCELLED']
    ).order_by('slot__time')
    
    # Upcoming Meetings (Tomorrow onwards)
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        slot__date__gt=today,
        status__in=['PENDING', 'CONFIRMED', 'CANCELLED']
    ).order_by('slot__date', 'slot__time')
    
    # Pending Payments
    pending_payments = Appointment.objects.filter(
        patient=patient,
        payment_status='PENDING',
        status__in=['PENDING', 'CONFIRMED', 'COMPLETED']
    )
    
    context = {
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_payments': pending_payments,
        'active_tab': 'home'
    }
    return render(request, 'appointments/home.html', context)

@login_required
def recent_appointments(request):
    patient = request.user.patient
    today = timezone.now().date()
    
    # Past appointments (Completed or Date passed)
    past_appointments = Appointment.objects.filter(
        patient=patient,
        slot__date__lt=today
    ).order_by('-slot__date', '-slot__time')
    
    # Completed OR Cancelled from today
    today_history = Appointment.objects.filter(
        patient=patient,
        slot__date=today,
        status__in=['COMPLETED', 'CANCELLED']
    )
    
    all_past = (past_appointments | today_history).distinct().order_by('-slot__date', '-slot__time')
    
    context = {
        'appointments': all_past,
        'active_tab': 'recent'
    }
    return render(request, 'appointments/recent.html', context)

@login_required
def profile(request):
    patient = request.user.patient
    
    # Review Logic
    existing_review = None
    try:
        existing_review = patient.review
    except Review.DoesNotExist:
        pass
        
    if request.method == 'POST':
        if 'submit_review' in request.POST:
            if not existing_review:
                rating = request.POST.get('rating')
                comment = request.POST.get('comment')
                Review.objects.create(
                    patient=patient,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Review submitted successfully!")
                return redirect('appointments:profile')
    
    context = {
        'patient': patient,
        'review': existing_review,
        'active_tab': 'profile'
    }
    return render(request, 'appointments/profile.html', context)

@login_required
def booking_date(request):
    # Check if patient already has ANY appointment
    if Appointment.objects.filter(patient=request.user.patient).exists():
        messages.info(request, "You already have a history with us. Please contact the clinic for follow-up appointments.")
        return redirect('appointments:home')

    # Generate next 7 days
    today = timezone.now().date()
    dates = []
    for i in range(7):
        d = today + timedelta(days=i)
        dates.append({
            'value': d.strftime('%Y-%m-%d'),
            'label': d.strftime('%a, %d %b'),
            'is_today': i == 0
        })
        
    return render(request, 'appointments/booking_date.html', {'dates': dates})

@login_required
def booking_slots(request):
    date_str = request.GET.get('date')
    if not date_str:
        return redirect('appointments:booking_date')
        
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Ensure slots exist
    slots = generate_slots_for_date(date_obj)
    
    # Refresh slots from DB to get latest status
    slots = DailySlot.objects.filter(date=date_obj).order_by('time')
    
    context = {
        'date': date_obj,
        'slots': slots
    }
    return render(request, 'appointments/booking_slots.html', context)

from django.db import transaction
from django.db.models import F

@login_required
def booking_confirm(request, slot_id):
    # Double check restriction
    if Appointment.objects.filter(patient=request.user.patient).exists():
        messages.error(request, "You cannot book additional appointments online.")
        return redirect('appointments:home')

    # Use select_for_update to lock the row
    with transaction.atomic():
        slot = get_object_or_404(DailySlot.objects.select_for_update(), id=slot_id)
        
        if request.method == 'POST':
            # Double booking check
            if slot.is_full:
                messages.error(request, "This slot was just booked by someone else.")
                # Get suggestions
                suggestions = get_slot_suggestions(slot.date, slot.time)
                return render(request, 'appointments/booking_full.html', {
                    'slot': slot,
                    'suggestions': suggestions
                })
                
            # Create Appointment
            symptoms = request.POST.get('symptoms')
            Appointment.objects.create(
                patient=request.user.patient,
                slot=slot,
                symptoms=symptoms,
                status='CONFIRMED', # Auto confirm for now
                payment_status='PENDING'
            )
            
            # Update slot capacity safely
            slot.booked_count = F('booked_count') + 1
            slot.save()
            
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointments:home')
            
    return render(request, 'appointments/booking_confirm.html', {'slot': slot})
