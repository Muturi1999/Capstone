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
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permissions import IsAdmin
from rest_framework_simplejwt import views as jwt_views


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

# Registration endpoint
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user).access_token

            # Email verification URL
            verification_url = request.build_absolute_uri(
                reverse('verify-email') + f"?token={str(token)}"
            )

            # Sending email
            send_mail(
                subject="Verify your email",
                message=f"Click here to verify your email: {verification_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response({"message": "Check your email to verify your account"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Email Verification Endpoint
class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            user = CustomUser.objects.get(auth_token=token)
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified, you can now login."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

# Login with JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_verified'] = user.is_verified  
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
