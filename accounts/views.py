from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, PhoneOTP
from .serializer import CreateUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


import random

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
def send_otp(phone):
        if phone:
            key = random.randint(1000, 9999)    
            print(key)
            return key
        
        else:
            return False


        
class validatedPhoneSendOtp(APIView):
    
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
            
            
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    
                    if old.exists():
                        old = old.first()
                        count = old.count
                        
                        if count >10:
                            return Response({'status' : False, 'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'})
                        
                        old.count = count+1
                        old.save()
                        print("count increase", count)
                        
                        return Response({'status': True, 'details':'OTP send successfully'})
                    
                    else:
                        PhoneOTP.objects.create(phone = phone, otp = key)
                        return Response({'status': True, 'details':'OTP send successfully'})
                        
                    
                    
                else:
                    return Response({'status': False, 'detail' : "OTP sending error. Please try after some time."})
            
            
        else:
            return Response({'status': False, 'detail': 'Phone Number is not given in post request'})
        
        
        
        
class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''
    
    def post(self, request, *args, **kwargs):
        phone = request.data .get('phone', False)
        otp_send = request.data.get('otp', False)
        
        if phone and otp_send:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            
            if old.exists():
                old = old.first()
                otp = old.otp
                
                if str(otp_send) == str(otp):
                    old.validated = True
                    old.save()
                    
                    token = get_tokens_for_user(old)
                    
                    return Response({'token':token,'status': True, 'detail' : "OTP matched. please proceed for registration"})
                
                else:
                    return Response({'status': False, 'detail': 'OTP incoorect'})            
        
        
            else:
                return Response({'status': False, 'detail' : "First proceed via sending otp request"})
        
            
        else:
            return Response({'status': False, 'detail' : "Please provide both phone number and otp for validation"})
        
        
        
        
class Register(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        
        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            
            if old.exists():
                old = old.first()
                otp = old.otp
                validated = old.validated
                
                
                if validated is True:
                    temp_data = {'phone':phone, 'password':password}
                    
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    
                    # token = get_tokens_for_user(user)
                    
                    old.delete()
                    return Response({'status': True, 'detail' : "Account created"})
                
                else:
                    return Response({'status': False, 'detail' : "OTP haven't verified. First do that step"})
                
                
            else:
                return Response({'status': False, 'detail' : "Please verfity phone first"})
        
        else:
            return Response({'status': False, 'detail' : "Both phone and password are not set"})

        
        
        
        