from django.urls import path
from .views import LoginView, MobileLoginView, VerifyOTPView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/mobile/', MobileLoginView.as_view(), name='mobile_login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]