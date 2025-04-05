from django.urls import path
from .views import (
    HomePageView,
    LoginPageView,
    LoginView,
    LogoutView,
    RegisterUserView,
    RequestPasswordResetView,
    ResetPasswordView,
    VerifyEmailView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    AssignRoleView
)

urlpatterns = [
    # Authentication endpoints
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    
    # Password reset
    path('api/request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('api/reset-password/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    
    # JWT auth with swagger
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # Email verification 
    path('api/verify-email/', VerifyEmailView.as_view(), name='confirm_email'),

    # Admin to assign roles
    path('api/user/<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    
    # Page views
    path('login-page/', LoginPageView.as_view(), name='login-page'),
    path('home/', HomePageView.as_view(), name='home-page'),
]