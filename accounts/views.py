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
from .models import User, Office, Service, Issue
import phonenumbers
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
import uuid

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
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        role = 'admin' if user.is_admin or user.is_superuser else 'user'
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': role,
        }, status=status.HTTP_200_OK)

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

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'username', 'phone_number', 'is_admin', 'created_at', 'password')
        return Response(list(users), status=status.HTTP_200_OK)

class UserDeleteView(APIView):
    def post(self, request):
        user_id = request.data.get('id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number']

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['id', 'name', 'location']

class ServiceSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'created_by', 'office', 'created_at']
        read_only_fields = ['id', 'created_at']

class IssueSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = Issue
        fields = ['id', 'type', 'description', 'status', 'reporter', 'service', 'office', 'assigned_to', 'attachments', 'created_at']
        read_only_fields = ['id', 'created_at', 'reporter']

class IssueCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Handle both JSON and multipart form data
        data = request.data.copy()
        files = request.FILES
        
        # If there are files, add them to the data
        if files:
            data['attachments'] = files.get('attachments')
        
        serializer = IssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save(reporter=request.user)
            return Response({
                'id': serializer.data['id'],
                'type': serializer.data['type'],
                'description': serializer.data['description'],
                'status': serializer.data['status'],
                'reporter': serializer.data['reporter'],
                'service': serializer.data['service'],
                'office': serializer.data['office'],
                'assigned_to': serializer.data['assigned_to'],
                'attachments': serializer.data.get('attachments'),
                'created_at': serializer.data['created_at'],
                'message': 'Issue created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class IssueListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        issues = Issue.objects.select_related('reporter', 'service', 'office', 'assigned_to').all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ServiceCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'description': serializer.data['description'],
                'created_by': serializer.data['created_by'],
                'office': serializer.data['office'],
                'created_at': serializer.data['created_at'],
                'message': 'Service created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ServiceListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        services = Service.objects.select_related('created_by', 'office').all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ServiceRetrieveView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        service_id = request.data.get('id')
        try:
            service = Service.objects.select_related('created_by', 'office').get(id=service_id)
        except Service.DoesNotExist:
            return Response({'detail': 'Service not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ServiceUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        service_id = request.data.get('id')
        try:
            service = Service.objects.select_related('created_by', 'office').get(id=service_id)
        except Service.DoesNotExist:
            return Response({'detail': 'Service not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'description': serializer.data['description'],
                'created_by': serializer.data['created_by'],
                'office': serializer.data['office'],
                'created_at': serializer.data['created_at'],
                'message': 'Service updated successfully.'
            }, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ServiceDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        service_id = request.data.get('id')
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({'detail': 'Service not found.'}, status=status.HTTP_404_NOT_FOUND)
        service.delete()
        return Response({'message': 'Service deleted successfully.'}, status=status.HTTP_200_OK)
