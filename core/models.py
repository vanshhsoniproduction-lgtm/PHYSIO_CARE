from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    # Storing date as a DateField
    date = models.DateField()
    # Storing time as a simple string (e.g., "09:00") since minutes are fixed
    time_slot = models.CharField(max_length=10)
    symptoms = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time_slot}"