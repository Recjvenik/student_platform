from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import User, OTPLog
import random
import requests

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


class HomeView(View):
    """Landing page - shows different content for authenticated vs non-authenticated users"""
    
    def get(self, request):
        # Always show the home page, but with different content based on auth status
        return render(request, 'home.html')


class LoginView(View):
    """Login page with options for Google OAuth and Mobile OTP"""
    
    def get(self, request):
        # Redirect authenticated users to profile start
        if request.user.is_authenticated:
            return redirect('profile_start')
        return render(request, 'accounts/login.html')

class LogoutView(View):
    """Custom logout view"""
    
    def get(self, request):
        logout(request)
        return redirect('home')
    
    def post(self, request):
        logout(request)
        return redirect('home')
    
# class MobileLoginView(View):
#     """Mobile number login - sends OTP"""
    
#     def get(self, request):
#         # Redirect authenticated users to profile start
#         if request.user.is_authenticated:
#             return redirect('profile_start')
#         return render(request, 'accounts/mobile_login.html')
    
#     def post(self, request):
#         mobile = request.POST.get('mobile', '').strip()
        
#         if not mobile or len(mobile) < 10:
#             return JsonResponse({'success': False, 'message': 'Invalid mobile number'})
        
#         # Generate OTP
#         otp = generate_otp()
#         expiry = timezone.now() + timedelta(seconds=settings.OTP_EXPIRY_SECONDS)
        
#         # Store OTP in database
#         OTPLog.objects.create(
#             mobile=mobile,
#             otp=otp,
#             expiry=expiry
#         )
        
#         # For POC: Print OTP to console (in production, send via SMS)
#         print(f'\n{"="*50}')
#         print(f'OTP for {mobile}: {otp}')
#         print(f'Valid for {settings.OTP_EXPIRY_SECONDS} seconds')
#         print(f'{"="*50}\n')
        
#         return JsonResponse({
#             'success': True,
#             'message': f'OTP sent successfully! (Check console for POC)',
#             'mobile': mobile
#         })

class MobileLoginView(View):
    """Mobile number login - sends OTP using 2Factor API"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile_start')
        return render(request, 'accounts/mobile_login.html')

    def post(self, request):
        mobile = request.POST.get('mobile', '').strip()

        # Validate mobile number
        if not mobile or len(mobile) < 10:
            return JsonResponse({'success': False, 'message': 'Invalid mobile number'})

        # Generate OTP
        otp = generate_otp()
        expiry = timezone.now() + timedelta(seconds=settings.OTP_EXPIRY_SECONDS)

        # Store OTP in DB
        OTPLog.objects.create(
            mobile=mobile,
            otp=otp,
            expiry=expiry
        )
        print('otp: ', otp, )
        # Normalize number with +91
        if not mobile.startswith("+91"):
            mobile = "+91" + mobile
        # 2Factor API URL
        api_key = settings.TWO_FACTOR_API_KEY
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobile}/{otp}/OneCore"

        try:
            response = requests.get(url, timeout=5)
            result = response.json()

            if result.get("Status") != "Success":
                return JsonResponse({
                    'success': False,
                    'message': "Failed to send OTP. Please try again."
                })

        except Exception as e:
            # Log the error
            print("2Factor API Error:", str(e))
            return JsonResponse({
                'success': False,
                'message': "OTP service unavailable. Please try again later."
            })

        return JsonResponse({
            'success': True,
            'message': "OTP sent successfully!",
            'mobile': mobile
        })
    
class VerifyOTPView(View):
    """Verify OTP and create/login user"""
    
    def get(self, request):
        # Redirect authenticated users to profile start
        if request.user.is_authenticated:
            return redirect('profile_start')
            
        mobile = request.GET.get('mobile', '')
        return render(request, 'accounts/verify_otp.html', {'mobile': mobile})
    
    def post(self, request):
        mobile = request.POST.get('mobile', '').strip()
        otp = request.POST.get('otp', '').strip()
        
        if not mobile or not otp:
            return JsonResponse({'success': False, 'message': 'Mobile and OTP are required'})
        
        # Get the most recent unverified OTP for this mobile
        try:
            otp_log = OTPLog.objects.filter(
                mobile=mobile,
                otp=otp,
                verified=False
            ).latest('created_at')
        except OTPLog.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid OTP'})
        
        # Check if OTP is expired
        if otp_log.is_expired():
            return JsonResponse({'success': False, 'message': 'OTP has expired'})
        
        # Mark OTP as verified
        otp_log.verified = True
        otp_log.verified_at = timezone.now()
        otp_log.save()
        
        # Get or create user
        user, created = User.objects.get_or_create(
            mobile=mobile,
            defaults={
                'auth_type': 'otp',
                'is_active': True
            }
        )
        
        # Log the user in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return JsonResponse({
            'success': True,
            'message': 'Login successful!',
            'redirect': '/profile/start/'
        })