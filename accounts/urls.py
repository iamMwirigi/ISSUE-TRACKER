from django.urls import path
from .views import (
    UserRegistrationView, LoginView, OTPVerifyView, UserDeleteView, UserListView,
    IssueCreateView, IssueListView, ServiceCreateView, ServiceListView, 
    ServiceRetrieveView, ServiceUpdateView, ServiceDeleteView,
    OfficeCreateView, OfficeListView, OfficeRetrieveView, OfficeUpdateView, OfficeDeleteView
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

    # Office endpoints with /offices/ prefix
    path('offices/create/', OfficeCreateView.as_view(), name='create-office'),
    path('offices/list/', OfficeListView.as_view(), name='list-offices'),
    path('offices/retrieve/', OfficeRetrieveView.as_view(), name='retrieve-office'),
    path('offices/update/', OfficeUpdateView.as_view(), name='update-office'),
    path('offices/delete/', OfficeDeleteView.as_view(), name='delete-office'),
] 