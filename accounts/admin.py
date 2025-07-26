from django.contrib import admin
from .models import User, Office, Service, Issue

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_admin', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_active', 'created_at')
    search_fields = ('username', 'phone_number')

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'office', 'created_at')
    list_filter = ('office', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('type', 'status', 'priority', 'reporter', 'service', 'office', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'service', 'office', 'created_at')
    search_fields = ('type', 'description')
    readonly_fields = ('reporter', 'created_at')
