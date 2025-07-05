from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import User
from .serializers import (
    CitizenSignupSerializer, OrganizationSignupSerializer, 
    AdminSignupSerializer, LoginSerializer, UserProfileSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.exceptions import TokenError


class CitizenSignupView(generics.CreateAPIView):
    serializer_class = CitizenSignupSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token
        # token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Citizen account created successfully',
            'user': UserProfileSerializer(user).data,
            # 'token': token.key
        }, status=status.HTTP_201_CREATED)

class OrganizationSignupView(generics.CreateAPIView):
    serializer_class = OrganizationSignupSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token
        # token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Organization account created successfully',
            'user': UserProfileSerializer(user).data,
            # 'token': token.key
        }, status=status.HTTP_201_CREATED)

class AdminSignupView(generics.CreateAPIView):
    serializer_class = AdminSignupSerializer
    permission_classes = [AllowAny]  # Change to admin-only in production
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token
        # token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Admin account created successfully',
            'user': UserProfileSerializer(user).data,
            # 'token': token.key
        }, status=status.HTTP_201_CREATED)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get or create token
        # token, created = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

# class LogoutView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         from django.contrib.auth import logout
#         logout(request)
#         return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user = serializer.validated_data['user']
               
        
#         # if not user.is_verified:
#         #     return Response({
#         #         'error': 'Please verify your account before logging in.',
#         #         'user_id': user.id,
#         #         'requires_verification': True
#         #     }, status=status.HTTP_400_BAD_REQUEST)
        
        
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': UserProfileSerializer(user).data
#         })

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     serializer = LoginSerializer(data=request.data, context={'request': request})
#     serializer.is_valid(raise_exception=True)
    
#     user = serializer.validated_data['user']
#     login(request, user)
    
#     # Get or create token
#     # token, created = Token.objects.get_or_create(user=user)
    
#     return Response({
#         'message': 'Login successful',
#         'user': UserProfileSerializer(user).data,
#         # 'token': token.key
#     }, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     try:
#         # Delete the token
#         request.user.auth_token.delete()
#         return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
#     except:
#         return Response({'message': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def profile_view(request):
#     serializer = UserProfileSerializer(request.user)
#     return Response(serializer.data)




# Create your views here.
# from rest_framework import status, generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView

# # from rest_framework import RefreshToken
# from django.contrib.auth import get_user_model
# from django.core.cache import cache
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import User, OTPVerification
# from .serializers import (
#     UserRegistrationSerializer, 
#     LoginSerializer, 
#     OTPRequestSerializer,
#     OTPVerifySerializer,
#     UserProfileSerializer
# )
# # from .utils import generate_otp, send_sms_otp
# from django.utils import timezone
# from datetime import timedelta
# import logging
# from rest_framework_simplejwt.tokens import RefreshToken
# logger = logging.getLogger(__name__)
# from rest_framework import generics
# from .serializers import CitizenProfileSerializer, OrganizationProfileSerializer, AdminProfileSerializer
# from .models import CitizenProfile, OrganizationProfile, AdminProfile
# from rest_framework.permissions import IsAdminUser
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import CitizenLoginSerializer, OrganizationLoginSerializer, AdminLoginSerializer
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken




# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
        
#         return Response({
#             'message': 'User registered successfully. Please verify your email/phone to activate your account.',
#             'user_id': user.id,
#             'email': user.email,
#             'role': user.role
#         }, status=status.HTTP_201_CREATED)

# class CitizenRegisterView(generics.CreateAPIView):
#     queryset = CitizenProfile.objects.all()
#     serializer_class = CitizenProfileSerializer

# class OrganizationRegisterView(generics.CreateAPIView):
#     queryset = OrganizationProfile.objects.all()
#     serializer_class = OrganizationProfileSerializer

# class AdminRegisterView(generics.CreateAPIView):
#     queryset = AdminProfile.objects.all()
#     serializer_class = AdminProfileSerializer
#     permission_classes = [IsAdminUser]  # Only existing superusers can add more




# class CitizenLoginView(TokenObtainPairView):
#     serializer_class = CitizenLoginSerializer

# class OrganizationLoginView(TokenObtainPairView):
#     serializer_class = OrganizationLoginSerializer

# class AdminLoginView(TokenObtainPairView):
#     serializer_class = AdminLoginSerializer




# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception:
#             return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)






# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user = serializer.validated_data['user']
               
        
#         # if not user.is_verified:
#         #     return Response({
#         #         'error': 'Please verify your account before logging in.',
#         #         'user_id': user.id,
#         #         'requires_verification': True
#         #     }, status=status.HTTP_400_BAD_REQUEST)
        
        
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': UserProfileSerializer(user).data
#         })

# class OTPRequestView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = OTPRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         verification_type = serializer.validated_data['verification_type']
        
#         try:
#             if verification_type == 'email':
#                 email = serializer.validated_data['email']
#                 user = User.objects.get(email=email)
#                 otp_code = generate_otp()
                
#                 # Store OTP in database
#                 OTPVerification.objects.create(
#                     user=user,
#                     verification_type='email',
#                     code=otp_code,
#                     expires_at=timezone.now() + timedelta(minutes=10)
#                 )
                
#                 # Send OTP via email
#                 send_mail(
#                     'OptiGov - Email Verification Code',
#                     f'Your verification code is: {otp_code}. This code will expire in 10 minutes.',
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                     fail_silently=False,
#                 )
                
#                 return Response({
#                     'message': 'OTP sent to your email successfully.',
#                     'verification_type': 'email'
#                 })
            
#             elif verification_type == 'phone':
#                 phone_number = serializer.validated_data['phone_number']
#                 user = User.objects.get(phone_number=phone_number)
#                 otp_code = generate_otp()
                
#                 # Store OTP in database
#                 OTPVerification.objects.create(
#                     user=user,
#                     verification_type='phone',
#                     code=otp_code,
#                     expires_at=timezone.now() + timedelta(minutes=10)
#                 )
                
#                 # Send OTP via SMS
#                 sms_sent = send_sms_otp(phone_number, otp_code)
#                 if not sms_sent:
#                     return Response({
#                         'error': 'Failed to send SMS. Please try again.'
#                     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
#                 return Response({
#                     'message': 'OTP sent to your phone successfully.',
#                     'verification_type': 'phone'
#                 })
                
#         except User.DoesNotExist:
#             return Response({
#                 'error': 'User not found with provided email/phone number.'
#             }, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             logger.error(f"OTP request error: {str(e)}")
#             return Response({
#                 'error': 'Failed to send OTP. Please try again.'
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class OTPVerifyView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = OTPVerifySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         verification_type = serializer.validated_data['verification_type']
#         code = serializer.validated_data['code']
        
#         try:
#             if verification_type == 'email':
#                 email = serializer.validated_data['email']
#                 user = User.objects.get(email=email)
#             else:
#                 phone_number = serializer.validated_data['phone_number']
#                 user = User.objects.get(phone_number=phone_number)
            
#             # Find valid OTP
#             otp_verification = OTPVerification.objects.filter(
#                 user=user,
#                 verification_type=verification_type,
#                 code=code,
#                 is_used=False,
#                 expires_at__gt=timezone.now()
#             ).first()
            
#             if not otp_verification:
#                 return Response({
#                     'error': 'Invalid or expired OTP code.'
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             # Mark OTP as used and verify user
#             otp_verification.is_used = True
#             otp_verification.save()
            
#             user.is_verified = True
#             user.save()
            
#             # Generate tokens for automatic login
#             refresh = RefreshToken.for_user(user)
            
#             return Response({
#                 'message': 'Account verified successfully.',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': UserProfileSerializer(user).data
#             })
            
#         except User.DoesNotExist:
#             return Response({
#                 'error': 'User not found.'
#             }, status=status.HTTP_404_NOT_FOUND)

# class ProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_object(self):
#         return self.request.user

# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'message': 'Logged out successfully.'})
#         except Exception as e:
#             return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.core.validators import RegexValidator

# class User(AbstractUser):
#     USER_TYPES = (
#         ('citizen', 'Citizen'),
#         ('organization', 'Organization'),
#         ('admin', 'Admin/Regulator'),
#     )
    
#     user_type = models.CharField(max_length=20, choices=USER_TYPES)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, blank=True)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

# class CitizenProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     national_id = models.CharField(max_length=20, unique=True, blank=True)
#     address = models.TextField(blank=True)
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class OrganizationProfile(models.Model):
#     ORGANIZATION_TYPES = (
#         ('ngo', 'NGO'),
#         ('company', 'Company'),
#         ('government', 'Government Agency'),
#         ('educational', 'Educational Institution'),
#     )
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization_profile')
#     organization_name = models.CharField(max_length=200)
#     organization_type = models.CharField(max_length=20, choices=ORGANIZATION_TYPES)
#     registration_number = models.CharField(max_length=50, unique=True)
#     contact_person = models.CharField(max_length=100)
#     address = models.TextField()
#     website = models.URLField(blank=True)
    
#     def __str__(self):
#         return self.organization_name

# class AdminProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
#     department = models.CharField(max_length=100)
#     position = models.CharField(max_length=100)
#     employee_id = models.CharField(max_length=20, unique=True)
#     permissions_level = models.IntegerField(default=1)  # 1-5 scale
    
#     def __str__(self):
#         return f"{self.user.username} - {self.department}"