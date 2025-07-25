import random
import string
import time
import requests
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import phonenumbers
from rest_framework import serializers

# In-memory OTP store (for demo; use cache/redis in prod)
otp_store = {}
OTP_EXPIRY_SECONDS = 300

# SMS API credentials
SMS_USERNAME = "mzigosms"
SMS_API_KEY = "91e59dfce79a61c35f3904acb2c71c27aeeef34f847f940fafb4c29674f8805c"
SMS_SENDER = "iGuru"  # Always use 'iGuru' as sender name
SMS_URL = "https://sms.movesms.co.ke/api/compose"  # Example endpoint, update if needed

def send_otp_sms(phone_number, otp):
    payload = {
        "username": SMS_USERNAME,
        "api_key": SMS_API_KEY,
        "sender": SMS_SENDER,
        "to": phone_number,
        "message": f"Your OTP code is: {otp}",
        "msgtype": 5,
        "dlr": 0
    }
    try:
        response = requests.post(SMS_URL, data=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[SMS ERROR] {e}")
        return False

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # Generate OTP
        otp = ''.join(random.choices(string.digits, k=6))
        otp_store[user.phone_number] = {'otp': otp, 'timestamp': time.time()}
        # Send OTP via SMS
        sent = send_otp_sms(user.phone_number, otp)
        if not sent:
            return Response({'detail': 'Failed to send OTP.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': 'OTP sent to your phone number.'}, status=status.HTTP_200_OK)

class OTPVerifyView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        otp_data = otp_store.get(user.phone_number)
        if not otp_data:
            return Response({'detail': 'OTP not found or expired.'}, status=status.HTTP_400_BAD_REQUEST)
        if time.time() - otp_data['timestamp'] > OTP_EXPIRY_SECONDS:
            del otp_store[user.phone_number]
            return Response({'detail': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)
        if otp != otp_data['otp']:
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        # OTP is valid, delete it
        del otp_store[user.phone_number]
        # Generate JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class UserDeleteView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'detail': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)
