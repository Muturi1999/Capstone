from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = 'users.CustomUser'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Email verification
    is_verified = models.BooleanField(default=False)  

    # Role-based access control
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')

    def is_admin(self):
        return self.role == 'admin'

    def is_organizer(self):
        return self.role == 'organizer'

    def is_attendee(self):
        return self.role == 'attendee'

    def __str__(self):
        return f"{self.username} ({self.role})"
