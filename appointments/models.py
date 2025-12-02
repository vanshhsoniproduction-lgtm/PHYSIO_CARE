from django.db import models
from accounts.models import Patient
from django.utils import timezone

class SlotTemplate(models.Model):
    time = models.TimeField(unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['time']
    def __str__(self):
        return self.time.strftime("%I:%M %p")

class DailySlot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField(default=1)
    booked_count = models.PositiveIntegerField(default=0)
    # Removed price field entirely from here as it's now dynamic per appointment
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = ('date', 'time')
        ordering = ['date', 'time']
    def __str__(self):
        return f"{self.date} - {self.time.strftime('%I:%M %p')}"
    @property
    def is_full(self):
        return self.booked_count >= self.capacity

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    BOOKING_SOURCE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey(DailySlot, on_delete=models.CASCADE, related_name='appointments')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED') # Default confirmed for patient booking
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    booking_source = models.CharField(max_length=10, choices=BOOKING_SOURCE_CHOICES, default='PATIENT')
    symptoms = models.TextField(blank=True, null=True)
    
    # Fee is NOW NULLABLE and has NO DEFAULT. Set by Doctor.
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    
    # Razorpay Fields
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.full_name} - {self.slot}"

class Review(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)