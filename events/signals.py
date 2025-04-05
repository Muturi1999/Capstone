from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from django.utils.timezone import now, timedelta
from .google_calendar import add_event_to_google_calendar


@receiver(post_save, sender=Event)
def create_recurring_events(sender, instance, created, **kwargs):
    """Generate future events if recurrence is set."""
    if created and instance.recurring in ['weekly', 'monthly']:
        future_dates = []
        base_date = instance.date_time

        for i in range(1, 5):  
            if instance.recurring == 'weekly':
                future_dates.append(base_date + timedelta(weeks=i))
            elif instance.recurring == 'monthly':
                future_dates.append(base_date + timedelta(weeks=i * 4))

        for future_date in future_dates:
            Event.objects.create(
                title=instance.title,
                description=instance.description,
                date_time=future_date,
                location=instance.location,
                organizer=instance.organizer,
                capacity=instance.capacity,
                recurring='none',
            )

@receiver(post_save, sender=Event)
def sync_event_to_google(sender, instance, created, **kwargs):
    """Sync event to Google Calendar when created."""
    if created:
        event_link = add_event_to_google_calendar(instance)
        print(f"Event synced to Google Calendar: {event_link}")