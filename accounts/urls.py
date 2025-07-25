from django.urls import path
from .views import LoginView, OTPVerifyView, UserRegistrationView, UserDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('delete/', UserDeleteView.as_view(), name='delete-user'),
] 