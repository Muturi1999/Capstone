from django.db import models
from django.conf import settings

# event model
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Booking model
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """To Prevent double bookings,Users can only book an event once
        If an event is deleted, its bookings are also deleted."""
        unique_together = ('user', 'event') 

    def __str__(self):
        return f"{self.user.username} booked {self.event.title}"

class Waitlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='waitlist')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Prevent double entries for waiting list."""
        unique_together = ('user', 'event')  

    def __str__(self):
        return f"{self.user.username} is on the waitlist for {self.event.title}"
