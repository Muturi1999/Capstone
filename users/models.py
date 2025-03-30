from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Email verification
    is_verified = models.BooleanField(default=False)  

    def __str__(self):
        return self.username
