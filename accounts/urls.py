from django.urls import path
from .views import (
    UserRegistrationView, LoginView, OTPVerifyView, UserDeleteView, UserListView,
    IssueCreateView, IssueListView, ServiceCreateView, ServiceListView, 
    ServiceRetrieveView, ServiceUpdateView, ServiceDeleteView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('delete/', UserDeleteView.as_view(), name='delete-user'),
    path('users/', UserListView.as_view(), name='list-users'),
    path('issues/create/', IssueCreateView.as_view(), name='create-issue'),
    path('issues/list/', IssueListView.as_view(), name='list-issues'),

    # Service endpoints with /services/ prefix
    path('services/create/', ServiceCreateView.as_view(), name='create-service'),
    path('services/list/', ServiceListView.as_view(), name='list-services'),
    path('services/retrieve/', ServiceRetrieveView.as_view(), name='retrieve-service'),
    path('services/update/', ServiceUpdateView.as_view(), name='update-service'),
    path('services/delete/', ServiceDeleteView.as_view(), name='delete-service'),
] 