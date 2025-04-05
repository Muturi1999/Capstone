from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
# from .utils import generate_verification_token

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")
        
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password"]
    
    def validate(self, data):
        """
        Validate that passwords match
        """
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        
        return data
    
    def create(self, validated_data):
        # Remove confirm_password from the data used to create the user
        validated_data.pop('confirm_password', None)
        
        # Create inactive user that requires verification
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
             
        return user
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length= 555)

    class Meta:
        model = User
        fields = ['token']
        
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing user profile information"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'email', 'is_verified', 'date_joined']