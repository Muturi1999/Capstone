from django.urls import path
from .views import RegisterUser, VerifyEmail, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AssignRoleView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),

    # jwt auth
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # admin to asignroles
    path('user/<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
]
