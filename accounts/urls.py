from django.urls import path, include
from .views import validatedPhoneSendOtp, ValidateOTP, Register

urlpatterns = [
    path('validate_phone/', validatedPhoneSendOtp.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
]