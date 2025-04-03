from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from .serializers import EmailVerificationSerializer, LoginSerializer, RegisterSerializer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg import openapi
from .utils import EmailGen
from rest_framework.views import APIView
import jwt
from django.urls import reverse
User = get_user_model()

# Custom Token Views with Swagger Documentation
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

# Login View (Redirects to Home Page on Success)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        
        # First check if user exists by username
        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active or not user_obj.is_verified:
                return Response(
                    {"error": "Email not verified. Please check your email."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Then authenticate with credentials
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            
            # For API usage - return tokens
            if request.META.get('HTTP_ACCEPT') == 'application/json':
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            
            # For browser - redirect with cookie
            response = redirect('/home/')
            response.set_cookie('access_token', str(refresh.access_token))
            return response

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Registration View
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relative_link = reverse('confirm_email')
            absoluteurl = "http://"+ current_site + relative_link + "?token=" + str(token)
            email_body = f"Hi, {user.username}. Please use the url below to verify your account." + '\n'+ absoluteurl 
            
            data = {
                'email_body': email_body,
                'To' : user.email,
                'subject': "Verify Email"
            }
            EmailGen.send_Email(data)

            # Email verification happens in the serializer
            return Response(
                {"message": "User registered successfully. Check your email for verification."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Email Verification View
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                            type=openapi.TYPE_STRING)
    @swagger_auto_schema(
            manual_parameters= [token_param_config]
    )
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload =  jwt.decode(token, settings.SECRET_KEY, algorithms=[
                'HS256'
            ])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response ({'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.DecodeError:
            return Response({"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        except user.DoesNotExist:
            return Response({'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response ({str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
# Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response = Response(
                {"message": "Successfully logged out"}, 
                status=status.HTTP_205_RESET_CONTENT
            )
            
            # Clear any cookies
            if 'access_token' in request.COOKIES:
                response.delete_cookie('access_token')
                
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Request Password Reset View
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid, token = generate_verification_token(user)
            
            # Use FRONTEND_URL from settings
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            send_mail(
                "Password Reset",
                f"Click the link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        # Always return success to prevent email enumeration
        return Response({"message": "Password reset link sent if email exists"}, status=status.HTTP_200_OK)

# Reset Password View
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')
                if not new_password:
                    return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
                
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# Assign Role View
class AssignRoleView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            role = request.data.get('role')

            if role not in ['admin', 'organizer', 'attendee']:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

            user.role = role
            user.save()
            return Response({"message": f"Role updated to {role} successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Home Page View
class HomePageView(APIView):
    def get(self, request):
        return render(request, 'home.html')

# Login Page View
class LoginPageView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'login.html')
