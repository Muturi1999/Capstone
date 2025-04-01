from django.urls import path
from .views import RegisterUserView, VerifyEmailView
# from .views import RegisterUserView, CustomTokenObtainPairView, VerifyEmail

from rest_framework_simplejwt.views import TokenRefreshView
from .views import AssignRoleView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),

    # jwt auth
    # path('login/', CustomTokenOUserbtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # testnewtoken and emailverification
    path("verify-email/<uid>/<token>/", VerifyEmailView.as_view(), name="verify-email"),

    # admin to asignroles
    path('user/<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
]

