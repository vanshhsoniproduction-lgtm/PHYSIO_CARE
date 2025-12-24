from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .models import Appointment, DailySlot, Review
from .utils import generate_slots_for_date
from datetime import datetime, timedelta

# --- DASHBOARD VIEW (Fixes AttributeError) ---
# physio_care/appointments/views.py

@login_required
def home(request):
    # --- FIX START: Handle users without a Patient profile (e.g., Admins) ---
    if not hasattr(request.user, 'patient'):
        if request.user.is_staff:
            return redirect('adminpanel:home')
        # If not staff and no patient profile, force re-login/signup
        return redirect('accounts:auth')
    # --- FIX END ---

    patient = request.user.patient
    today = timezone.now().date()
    
    # 1. Today's Meetings (Confirmed, Completed, Pending)
    today_appointments = Appointment.objects.filter(
        patient=patient,
        slot__date=today,
        status__in=['CONFIRMED', 'COMPLETED', 'PENDING']
    ).order_by('slot__time')
    
    # 2. Upcoming Meetings (Tomorrow onwards)
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        slot__date__gt=today,
        status__in=['CONFIRMED', 'PENDING']
    ).order_by('slot__date', 'slot__time')
    
    # 3. Pending Payments (Completed sessions with a fee set, not yet paid)
    pending_payments = Appointment.objects.filter(
        patient=patient,
        payment_status='PENDING',
        fee__isnull=False,
        is_free=False,
        status='COMPLETED'
    ).order_by('-slot__date')
    
    context = {
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_payments': pending_payments,
        'active_tab': 'home'
    }
    return render(request, 'appointments/home.html', context)
# --- BOOKING VIEWS ---

@login_required
def booking_date(request):
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
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return redirect('appointments:booking_date')
    
    generate_slots_for_date(date_obj)
    slots = DailySlot.objects.filter(date=date_obj).order_by('time')
    
    return render(request, 'appointments/booking_slots.html', {'date': date_obj, 'slots': slots})

@login_required
def booking_confirm(request, slot_id):
    slot = get_object_or_404(DailySlot, id=slot_id)
    
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        
        with transaction.atomic():
            # Lock the slot to prevent double booking
            slot = get_object_or_404(DailySlot.objects.select_for_update(), id=slot_id)
            
            if slot.is_full:
                messages.error(request, "Slot was just taken.")
                return redirect('appointments:booking_slots', date=slot.date)

            # Create Appointment (Without Payment)
            Appointment.objects.create(
                patient=request.user.patient,
                slot=slot,
                symptoms=symptoms,
                status='CONFIRMED', 
                payment_status='PENDING',
                fee=None, # Fee is set by Doctor later
                is_free=False
            )
            
            slot.booked_count = F('booked_count') + 1
            slot.save()
            
        messages.success(request, "Appointment booked successfully!")
        return redirect('appointments:home')

    return render(request, 'appointments/booking_confirm.html', {'slot': slot})

# --- OTHER VIEWS ---

@login_required
def recent_appointments(request):
    patient = request.user.patient
    history = Appointment.objects.filter(patient=patient).order_by('-slot__date', '-slot__time')
    
    context = {
        'appointments': history,
        'active_tab': 'recent'
    }
    return render(request, 'appointments/recent.html', context)

@login_required
def profile(request):
    patient = request.user.patient
    try:
        existing_review = patient.review
    except Review.DoesNotExist:
        existing_review = None
        
    if request.method == 'POST' and 'submit_review' in request.POST:
        if not existing_review:
            Review.objects.create(
                patient=patient,
                rating=request.POST.get('rating'),
                comment=request.POST.get('comment')
            )
            messages.success(request, "Review submitted successfully!")
            return redirect('appointments:profile')
    
    return render(request, 'appointments/profile.html', {
        'patient': patient, 
        'review': existing_review, 
        'active_tab': 'profile'
    })