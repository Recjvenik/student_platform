from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email=None, mobile=None, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email and not mobile:
            raise ValueError('User must have either email or mobile number')
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(email=email, mobile=mobile, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model supporting Google OAuth and OTP login"""
    
    AUTH_TYPE_CHOICES = [
        ('google', 'Google'),
        ('otp', 'OTP'),
    ]
    
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    auth_type = models.CharField(max_length=10, choices=AUTH_TYPE_CHOICES, default='otp')
    google_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    profile_picture = models.URLField(blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email or self.mobile or f'User {self.id}'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name


class OTPLog(models.Model):
    """Model to track OTP generation and verification"""
    
    mobile = models.CharField(max_length=15, db_index=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'otp_logs'
        ordering = ['-created_at']
        verbose_name = 'OTP Log'
        verbose_name_plural = 'OTP Logs'
    
    def __str__(self):
        return f'{self.mobile} - {self.otp} (Verified: {self.verified})'
    
    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expiry