from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.db.models import Q, Count, F, Sum
from django.db import transaction
from django.contrib import messages
from appointments.models import Appointment, DailySlot, Review
from accounts.models import Patient
from appointments.utils import generate_slots_for_date
from datetime import datetime, timedelta

# --- Auth Views ---

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('adminpanel:home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('adminpanel:home')
            else:
                messages.error(request, "Access denied. Staff only.")
    else:
        form = AuthenticationForm()
    return render(request, 'adminpanel/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('adminpanel:login')

# --- Main Tabs ---

@login_required
def home(request):
    if not request.user.is_staff:
        return redirect('adminpanel:login')
        
    today = timezone.now().date()
    
    # Today's Meetings: 
    # Show CONFIRMED or PENDING.
    # EXCLUDE 'COMPLETED' (Marked as read/met) to remove them from the active list.
    today_appointments = Appointment.objects.filter(
        slot__date=today,
        status__in=['CONFIRMED', 'PENDING'] 
    ).exclude(status='COMPLETED').select_related('patient', 'slot').order_by('slot__time')
    
    # Upcoming Meetings (Tomorrow onwards)
    upcoming_appointments = Appointment.objects.filter(
        slot__date__gt=today,
        status__in=['CONFIRMED', 'PENDING']
    ).select_related('patient', 'slot').order_by('slot__date', 'slot__time')
    
    # Check for repeated patients (UI logic)
    for appt in today_appointments:
        appt.is_repeated = Appointment.objects.filter(
            patient=appt.patient, 
            created_at__lt=appt.created_at
        ).exists()
        
    for appt in upcoming_appointments:
        appt.is_repeated = Appointment.objects.filter(
            patient=appt.patient, 
            created_at__lt=appt.created_at
        ).exists()

    # Statistics
    total_patients = Patient.objects.count()
    
    # Pending Payments: Price set (not null), Payment Pending, Not Free
    pending_payments_count = Appointment.objects.filter(
        payment_status='PENDING',
        fee__isnull=False,
        is_free=False,
        status__in=['CONFIRMED', 'COMPLETED']
    ).count()
    
    # Today's Revenue (Paid)
    revenue_data = Appointment.objects.filter(
        payment_status='PAID', 
        updated_at__date=today
    ).aggregate(Sum('fee'))
    today_revenue = revenue_data['fee__sum'] if revenue_data['fee__sum'] else 0

    context = {
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'active_tab': 'home',
        'stats': {
            'total_patients': total_patients,
            'pending_payments': pending_payments_count,
            'today_revenue': today_revenue
        }
    }
    return render(request, 'adminpanel/home.html', context)

@login_required
def patients(request):
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(
            Q(full_name__icontains=query) | 
            Q(phone__icontains=query)
        ).order_by('full_name')
    else:
        patients = Patient.objects.all().order_by('-created_at')[:20] 
        
    context = {
        'patients': patients,
        'query': query,
        'active_tab': 'patients'
    }
    return render(request, 'adminpanel/patients.html', context)

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = patient.appointments.all().order_by('-slot__date', '-slot__time')
    
    today = timezone.now().date()
    dates = []
    for i in range(14): 
        d = today + timedelta(days=i)
        dates.append({
            'value': d.strftime('%Y-%m-%d'),
            'label': d.strftime('%a, %d %b')
        })
        
    context = {
        'patient': patient,
        'appointments': appointments,
        'dates': dates,
        'active_tab': 'patients'
    }
    return render(request, 'adminpanel/patient_detail.html', context)

@login_required
def payments(request):
    # Pending / Failed
    pending = Appointment.objects.filter(
        payment_status__in=['PENDING', 'FAILED'],
        fee__isnull=False,
        is_free=False
    ).select_related('patient', 'slot').order_by('slot__date')
    
    # Paid or Free
    paid = Appointment.objects.filter(
        Q(payment_status='PAID') | Q(is_free=True)
    ).select_related('patient', 'slot').order_by('-updated_at')[:50]
    
    context = {
        'pending': pending,
        'paid': paid,
        'active_tab': 'payments'
    }
    return render(request, 'adminpanel/payments.html', context)

@login_required
def reviews(request):
    reviews_list = Review.objects.all().select_related('patient').order_by('-created_at')
    
    context = {
        'reviews': reviews_list,
        'active_tab': 'reviews'
    }
    return render(request, 'adminpanel/reviews.html', context)

@login_required
def settings(request):
    return render(request, 'adminpanel/settings.html', {'active_tab': 'settings'})

# --- Actions ---

@login_required
def delete_appointment(request, appointment_id):
    if request.method == 'POST':
        appt = get_object_or_404(Appointment, id=appointment_id)
        slot = appt.slot
        
        appt.delete()
        
        if slot.booked_count > 0:
            slot.booked_count = F('booked_count') - 1
            slot.save()
            
        messages.success(request, "Appointment deleted successfully.")
        return redirect('adminpanel:home')
    return redirect('adminpanel:home')

@login_required
def approve_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    return redirect('adminpanel:reviews')

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('adminpanel:reviews')

@login_required
def get_slots_for_date(request):
    date_str = request.GET.get('date')
    if not date_str:
        return render(request, 'adminpanel/components/slot_options.html', {'slots': []})
        
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    generate_slots_for_date(date_obj)
    
    slots = DailySlot.objects.filter(date=date_obj).order_by('time')
    return render(request, 'adminpanel/components/slot_options.html', {'slots': slots})

@login_required
def doctor_book_appointment(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        slot_id = request.POST.get('slot_id')
        
        # Fee logic from Doctor Booking Form
        is_free = request.POST.get('is_free') == 'on'
        fee = request.POST.get('fee')
        
        with transaction.atomic():
            slot = get_object_or_404(DailySlot.objects.select_for_update(), id=slot_id)
            
            if slot.is_full:
                messages.error(request, "Slot is full.")
                return redirect('adminpanel:patient_detail', patient_id=patient_id)
            
            appt = Appointment(
                patient=patient,
                slot=slot,
                status='CONFIRMED',
                payment_status='PENDING',
                booking_source='DOCTOR',
                is_free=is_free
            )
            
            # If Doctor sets fee now, assign it. Otherwise leave None.
            if not is_free and fee:
                appt.fee = fee
            elif is_free:
                appt.fee = None
            
            appt.save()
            
            slot.booked_count = F('booked_count') + 1
            slot.save()
            
            messages.success(request, "Appointment scheduled successfully.")
            
    return redirect('adminpanel:patient_detail', patient_id=patient_id)

@login_required
def update_fee(request, appointment_id):
    """
    Handles 'Mark as Read / Completed' and assigning fees.
    """
    if request.method == 'POST':
        appt = get_object_or_404(Appointment, id=appointment_id)
        
        # Logic for "Mark as Met / Completed"
        if request.POST.get('mark_completed') == 'true':
            appt.status = 'COMPLETED'
            
            is_free = request.POST.get('is_free') == 'on'
            fee_amount = request.POST.get('fee')
            
            if is_free:
                appt.is_free = True
                appt.fee = None
                # Free means payment logic is effectively done
            elif fee_amount:
                appt.fee = fee_amount
                appt.is_free = False
                # Payment status remains PENDING until patient pays via their portal
            
            appt.save()
            messages.success(request, "Appointment marked as completed and removed from active view.")
            
        return redirect('adminpanel:home')

@login_required
def mark_paid(request, appointment_id):
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.payment_status = 'PAID'
    appt.save()
    messages.success(request, "Marked as Paid.")
    return redirect('adminpanel:payments')