from django.urls import path
from .views import (
    LoginView, OTPVerifyView, UserRegistrationView, UserDeleteView, UserListView, IssueCreateView, IssueListView,
    ProjectCreateView, ProjectListView, ProjectRetrieveView, ProjectUpdateView, ProjectDeleteView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp-verify'),
    path('delete/', UserDeleteView.as_view(), name='delete-user'),
    path('users/', UserListView.as_view(), name='list-users'),
    path('issues/create/', IssueCreateView.as_view(), name='create-issue'),
    path('issues/list/', IssueListView.as_view(), name='list-issues'),

    # Project endpoints with /projects/ prefix
    path('projects/create/', ProjectCreateView.as_view(), name='create-project'),
    path('projects/list/', ProjectListView.as_view(), name='list-projects'),
    path('projects/retrieve/', ProjectRetrieveView.as_view(), name='retrieve-project'),
    path('projects/update/', ProjectUpdateView.as_view(), name='update-project'),
    path('projects/delete/', ProjectDeleteView.as_view(), name='delete-project'),
] 