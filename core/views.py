from django.shortcuts import render
from appointments.models import Review

def landing_page(request):
    # Fetch approved reviews to display on the landing page
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:5]
    return render(request, "core/landing.html", {'reviews': reviews})