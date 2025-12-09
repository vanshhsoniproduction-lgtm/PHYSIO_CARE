from datetime import timedelta, datetime
from django.utils import timezone
from django.db import models
from .models import SlotTemplate, DailySlot

def generate_slots_for_date(date):
    """Generates DailySlots for a given date based on active SlotTemplates."""
    templates = SlotTemplate.objects.filter(is_active=True)
    created_slots = []
    for template in templates:
        # FIX: Removed 'price' from defaults as it is no longer in DailySlot model
        slot, created = DailySlot.objects.get_or_create(
            date=date,
            time=template.time,
            defaults={'capacity': 1} 
        )
        if created:
            created_slots.append(slot)
    return created_slots

def get_slot_suggestions(date, time_obj):
    """
    Returns suggestions if a slot is full:
    1. Next available slot today
    2. Previous available slot today
    3. Same time tomorrow
    """
    suggestions = []
    
    # 1. Next available slot today
    next_slot = DailySlot.objects.filter(
        date=date, 
        time__gt=time_obj, 
        is_active=True
    ).exclude(booked_count__gte=models.F('capacity')).order_by('time').first()
    
    if next_slot:
        suggestions.append({
            'type': 'Next Available Today',
            'slot': next_slot
        })

    # 2. Previous available slot today
    prev_slot = DailySlot.objects.filter(
        date=date, 
        time__lt=time_obj, 
        is_active=True
    ).exclude(booked_count__gte=models.F('capacity')).order_by('-time').first()
    
    if prev_slot:
        suggestions.append({
            'type': 'Previous Available Today',
            'slot': prev_slot
        })

    # 3. Same time tomorrow
    tomorrow = date + timedelta(days=1)
    # Ensure slots exist for tomorrow
    if not DailySlot.objects.filter(date=tomorrow).exists():
        generate_slots_for_date(tomorrow)
        
    same_time_tomorrow = DailySlot.objects.filter(
        date=tomorrow, 
        time=time_obj, 
        is_active=True
    ).exclude(booked_count__gte=models.F('capacity')).first()

    if same_time_tomorrow:
        suggestions.append({
            'type': 'Same Time Tomorrow',
            'slot': same_time_tomorrow
        })
        
    return suggestions