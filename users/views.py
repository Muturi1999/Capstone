from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from django.contrib.auth import get_user_model
from .models import CustomUser
# from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permissions import IsAdmin
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()

# Admin to assign roles
class AssignRoleView(generics.UpdateAPIView):
    """Admin can assign user roles."""
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        from .serializers import UserSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        new_role = request.data.get('role', None)

        if new_role and new_role in ['admin', 'organizer', 'attendee']:
            user.role = new_role
            user.save()
            return Response({"message": f"Role updated to {new_role}"})
        return Response({"error": "Invalid role"}, status=400)


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully. Check your email for verification."}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)

            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError):
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

# custom jwt for swagger
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=TokenObtainPairSerializer,
        responses={200: TokenObtainPairResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        request_body=TokenRefreshSerializer,
        responses={200: TokenObtainPairResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)