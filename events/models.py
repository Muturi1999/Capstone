from django.db import models
from django.conf import settings


class Event(models.Model):
    RECURRING_CHOICES = [
        ('none', 'No Recurrence'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('AI', 'Artificial Intelligence'),
        ('Economics', 'Economics'),
        ('finance', 'Finance'),
        ('Business', 'Business'),
        ('Startup', 'Startups & Entrepreneurship'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Data_science', 'Data Science'),
        ('Blockchain', 'Blockchain'),
        ('Cloud', 'Cloud Computing'),
        ('machine_learning', 'Machine Learning'),
        ('Software_dev', 'Software Development'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='tech')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    recurring = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')

    def __str__(self):
        return f"{self.title} ({self.get_recurring_display()})"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """To Prevent double bookings, Users can only book an event once.
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


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.rating} Stars)"
