from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import EventBooking

@shared_task
def send_event_reminder():
    """Send email reminders for upcoming events."""
    upcoming_events = EventBooking.objects.filter(event__date_time__date=now().date())

    for booking in upcoming_events:
        send_mail(
            subject=f"Reminder: {booking.event.title} is tomorrow!",
            message=f"Hello {booking.user.username},\n\n"
                    f"Don't forget about your event: {booking.event.title} happening tomorrow at {booking.event.date_time}.",
            from_email="noreply@eventapp.com",
            recipient_list=[booking.user.email],
        )
