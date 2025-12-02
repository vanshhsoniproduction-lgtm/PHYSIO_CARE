from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Signup fields
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, unique=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
