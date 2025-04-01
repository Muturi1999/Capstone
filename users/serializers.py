from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import CustomUser

User = get_user_model()

# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         # login is false until email is verified
#         user.is_active = False  
#         user.save()
#         return user
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .utils import generate_verification_token 

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "password"]

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         user.is_active = False 
#         user.save()

#         # Generate verification link
#         uid, token = generate_verification_token(user)
#         verification_url = f"http://127.0.0.1:8000/api/verify-email/{uid}/{token}/"

#         # Send verification email
#         send_mail(
#             "Verify Your Email",
#             f"Click the link to verify your email: {verification_url}",
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             fail_silently=False,
#         )

#         return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.is_active = False  # Prevent login until verification
        user.save()

        # Generate email verification token
        uid, token = generate_verification_token(user)
        verification_url = f"http://127.0.0.1:8000/api/verify-email/{uid}/{token}/"

        # Send verification email
        send_mail(
            "Verify Your Email",
            f"Click the link to verify your email: {verification_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user
