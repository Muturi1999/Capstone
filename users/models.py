from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using= self._db)
        return user
    def create_superuser(self,username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_active', True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Super user must have is_superuser = True')  
        if extra_fields.get("is_staff") is not True:
            raise ValueError('Staff user must have is_staff = True')  

        return self.create_user(username, email, password, **extra_fields)
        


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)

    
    # Email verification
    # is_active = models.BooleanField(default=False) 
    is_verified = models.BooleanField(default=False)
    
    # Role-based access control
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')
    objects = CustomManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return tokens

    def is_admin(self):
        return self.role == 'admin'
    
    def is_organizer(self):
        return self.role == 'organizer'
    
    def is_attendee(self):
        return self.role == 'attendee'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
