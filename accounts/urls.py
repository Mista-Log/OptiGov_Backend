from django.urls import path
from . import views

urlpatterns = [
    # Signup endpoints
    path('citizen/signup/', views.CitizenSignupView.as_view(), name='citizen-signup'),
    path('organization/signup/', views.OrganizationSignupView.as_view(), name='organization-signup'),
    path('admin/signup/', views.AdminSignupView.as_view(), name='admin-signup'),
    
    # Login/logout endpoints
    path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.logout_view, name='logout'),
    
    # # Profile endpoint
    # path('auth/profile/', views.profile_view, name='profile'),
]



# from django.urls import path
# from .views import (
#     RegisterView,
#     LoginView,
#     # OTPRequestView,
#     # OTPVerifyView,
#     ProfileView,
#     LogoutView, 
#     CitizenRegisterView, 
#     OrganizationRegisterView, 
#     AdminRegisterView, 
#     CitizenLoginView, 
#     OrganizationLoginView, 
#     AdminLoginView, 
#     LogoutView
# )

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),


#     path('register/citizen/', CitizenRegisterView.as_view(), name='citizen-register'),
#     path('register/organization/', OrganizationRegisterView.as_view(), name='org-register'),
#     path('register/admin/', AdminRegisterView.as_view(), name='admin-register'),
#     path('login/citizen/', CitizenLoginView.as_view(), name='citizen-login'),
#     path('login/organization/', OrganizationLoginView.as_view(), name='organization-login'),
#     path('login/admin/', AdminLoginView.as_view(), name='admin-login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
    
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     # path('otp/request/', OTPRequestView.as_view(), name='otp_request'),
#     # path('otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),
#     path('profile/', ProfileView.as_view(), name='profile'),
# ]