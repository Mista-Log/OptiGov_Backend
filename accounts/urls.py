from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    # OTPRequestView,
    # OTPVerifyView,
    ProfileView,
    LogoutView, 
    CitizenRegisterView, 
    OrganizationRegisterView, 
    AdminRegisterView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),


    path('register/citizen/', CitizenRegisterView.as_view(), name='citizen-register'),
    path('register/organization/', OrganizationRegisterView.as_view(), name='org-register'),
    path('register/admin/', AdminRegisterView.as_view(), name='admin-register'),
    
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('otp/request/', OTPRequestView.as_view(), name='otp_request'),
    # path('otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
]