from django.urls import path
from .views import LoginView, OTPVerifyView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
] 