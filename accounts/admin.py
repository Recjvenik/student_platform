from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    
    list_display = ['id', 'email', 'mobile', 'name', 'auth_type', 'is_active', 'date_joined']
    list_filter = ['auth_type', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'mobile', 'name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'mobile', 'password')}),
        ('Personal Info', {'fields': ('name', 'profile_picture')}),
        ('Authentication', {'fields': ('auth_type', 'google_uid')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'name', 'password1', 'password2'),
        }),
    )


@admin.register(OTPLog)
class OTPLogAdmin(admin.ModelAdmin):
    """OTP Log admin"""
    
    list_display = ['mobile', 'otp', 'created_at', 'expiry', 'verified', 'verified_at']
    list_filter = ['verified', 'created_at']
    search_fields = ['mobile', 'otp']
    readonly_fields = ['created_at', 'verified_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False