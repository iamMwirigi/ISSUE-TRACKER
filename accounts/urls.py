from django.urls import path
from .views import (
    LoginView, OTPVerifyView, UserRegistrationView, UserDeleteView, UserListView, IssueCreateView,
    ProjectCreateView, ProjectListView, ProjectRetrieveView, ProjectUpdateView, ProjectDeleteView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('delete/', UserDeleteView.as_view(), name='delete-user'),
    path('users/', UserListView.as_view(), name='list-users'),
    path('api/issues/create/', IssueCreateView.as_view(), name='create-issue'),

    # Project endpoints with /api/projects/ prefix
    path('api/projects/create/', ProjectCreateView.as_view(), name='create-project'),
    path('api/projects/list/', ProjectListView.as_view(), name='list-projects'),
    path('api/projects/retrieve/', ProjectRetrieveView.as_view(), name='retrieve-project'),
    path('api/projects/update/', ProjectUpdateView.as_view(), name='update-project'),
    path('api/projects/delete/', ProjectDeleteView.as_view(), name='delete-project'),
] 