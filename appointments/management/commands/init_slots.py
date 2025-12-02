from django.core.management.base import BaseCommand
from appointments.models import SlotTemplate
from datetime import time

class Command(BaseCommand):
    help = 'Initialize standard slot templates (6 AM to 10 PM)'

    def handle(self, *args, **kwargs):
        # 6 AM to 10 PM (22:00)
        start_hour = 6
        end_hour = 22

        created_count = 0
        for hour in range(start_hour, end_hour + 1):
            t = time(hour, 0)
            obj, created = SlotTemplate.objects.get_or_create(time=t)
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} slot templates'))
