from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Patient
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Patient
        fields = ['full_name', 'email', 'phone', 'dob', 'gender', 'country', 'address']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Patient.objects.filter(phone=phone).exists():
            raise ValidationError("Phone number already registered.")
        return phone

    def save(self, commit=True):
        # Create User
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        # Use email as username
        user = User.objects.create_user(username=email, email=email, password=password)
        
        # Create Patient
        patient = super().save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username_input = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_input and password:
            user = None
            # Try to find user by email
            if '@' in username_input:
                try:
                    user_obj = User.objects.get(email=username_input)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            else:
                # Try to find user by phone (via Patient model)
                try:
                    patient = Patient.objects.get(phone=username_input)
                    user = authenticate(username=patient.user.username, password=password)
                except Patient.DoesNotExist:
                    pass
            
            if not user:
                raise ValidationError("Invalid credentials.")
            
            self.user_cache = user
        
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)
