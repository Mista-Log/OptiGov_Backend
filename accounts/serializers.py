from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, CitizenProfile, OrganizationProfile, AdminProfile

class CitizenSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    national_id = serializers.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone', 
                 'first_name', 'last_name', 'national_id']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm and profile fields
        validated_data.pop('password_confirm')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        national_id = validated_data.pop('national_id', '')
        
        # Create user
        user = User.objects.create_user(
            user_type='citizen',
            **validated_data
        )
        
        # Create citizen profile
        CitizenProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            national_id=national_id
        )
        
        return user

class OrganizationSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    organization_name = serializers.CharField(max_length=200)
    organization_type = serializers.ChoiceField(choices=OrganizationProfile.ORGANIZATION_TYPES)
    registration_number = serializers.CharField(max_length=50)
    contact_person = serializers.CharField(max_length=100)
    address = serializers.CharField()
    website = serializers.URLField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone',
                 'organization_name', 'organization_type', 'registration_number',
                 'contact_person', 'address', 'website']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm and profile fields
        validated_data.pop('password_confirm')
        organization_name = validated_data.pop('organization_name')
        organization_type = validated_data.pop('organization_type')
        registration_number = validated_data.pop('registration_number')
        contact_person = validated_data.pop('contact_person')
        address = validated_data.pop('address')
        website = validated_data.pop('website', '')
        
        # Create user
        user = User.objects.create_user(
            user_type='organization',
            **validated_data
        )
        
        # Create organization profile
        OrganizationProfile.objects.create(
            user=user,
            organization_name=organization_name,
            organization_type=organization_type,
            registration_number=registration_number,
            contact_person=contact_person,
            address=address,
            website=website
        )
        
        return user

class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    department = serializers.CharField(max_length=100)
    position = serializers.CharField(max_length=100)
    employee_id = serializers.CharField(max_length=20)
    permissions_level = serializers.IntegerField(default=1)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone',
                 'department', 'position', 'employee_id', 'permissions_level']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm and profile fields
        validated_data.pop('password_confirm')
        department = validated_data.pop('department')
        position = validated_data.pop('position')
        employee_id = validated_data.pop('employee_id')
        permissions_level = validated_data.pop('permissions_level', 1)
        
        # Create user
        user = User.objects.create_user(
            user_type='admin',
            **validated_data
        )
        
        # Create admin profile
        AdminProfile.objects.create(
            user=user,
            department=department,
            position=position,
            employee_id=employee_id,
            permissions_level=permissions_level
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account is disabled')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')


class UserProfileSerializer(serializers.ModelSerializer):
    citizen_profile = serializers.SerializerMethodField()
    organization_profile = serializers.SerializerMethodField()
    admin_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone', 'is_verified',
                 'created_at', 'citizen_profile', 'organization_profile', 'admin_profile']
        read_only_fields = ['id', 'created_at', 'user_type']
    
    def get_citizen_profile(self, obj):
        if obj.user_type == 'citizen' and hasattr(obj, 'citizen_profile'):
            return {
                'first_name': obj.citizen_profile.first_name,
                'last_name': obj.citizen_profile.last_name,
                'national_id': obj.citizen_profile.national_id,
                'address': obj.citizen_profile.address
            }
        return None
    
    def get_organization_profile(self, obj):
        if obj.user_type == 'organization' and hasattr(obj, 'organization_profile'):
            return {
                'organization_name': obj.organization_profile.organization_name,
                'organization_type': obj.organization_profile.organization_type,
                'registration_number': obj.organization_profile.registration_number,
                'contact_person': obj.organization_profile.contact_person,
                'address': obj.organization_profile.address,
                'website': obj.organization_profile.website
            }
        return None
    
    def get_admin_profile(self, obj):
        if obj.user_type == 'admin' and hasattr(obj, 'admin_profile'):
            return {
                'department': obj.admin_profile.department,
                'position': obj.admin_profile.position,
                'employee_id': obj.admin_profile.employee_id,
                'permissions_level': obj.admin_profile.permissions_level
            }
        return None



# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from django.contrib.auth.password_validation import validate_password
# from .models import User, CitizenProfile, OrganizationProfile, AdminProfile
# import random
# import string
# from datetime import datetime, timedelta
# from django.utils import timezone
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, validators=[validate_password])
#     password_confirm = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'phone_number', 'role', 'password', 'password_confirm')
    
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password_confirm']:
#             raise serializers.ValidationError("Passwords don't match")
#         return attrs
    
#     def validate_role(self, value):
#         if value not in ['citizen', 'organization']:
#             raise serializers.ValidationError("Invalid role. Only 'citizen' and 'organization' are allowed for registration.")
#         return value
    
#     def create(self, validated_data):
#         validated_data.pop('password_confirm')
#         password = validated_data.pop('password')
#         user = User.objects.create_user(password=password, **validated_data)
#         return user

# class CitizenProfileSerializer(serializers.ModelSerializer):
#     user = User()

#     class Meta:
#         model = CitizenProfile
#         fields = ['user', 'date_of_birth', 'address', 'gender', 'national_id_number', 'id_document']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_data['role'] = 'citizen'
#         user = User().create(user_data)
#         profile = CitizenProfile.objects.create(user=user, **validated_data)
#         return profile
    
#     def create(self, validated_data):
#         validated_data.pop('password_confirm')
#         password = validated_data.pop('password')
#         user = User.objects.create_user(password=password, **validated_data)
#         return user


# class OrganizationProfileSerializer(serializers.ModelSerializer):
#     user = UserRegistrationSerializer()

#     class Meta:
#         model = OrganizationProfile
#         fields = [
#             'user', 'company_name', 'cac_number', 'tax_id_number',
#             'company_address', 'industry_type',
#             'cac_certificate', 'tax_clearance_certificate'
#         ]

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_data['role'] = 'organization'
#         user = UserRegistrationSerializer().create(user_data)
#         profile = OrganizationProfile.objects.create(user=user, **validated_data)
#         return profile


# class AdminProfileSerializer(serializers.ModelSerializer):
#     user = UserRegistrationSerializer()

#     class Meta:
#         model = AdminProfile
#         fields = ['user', 'government_agency', 'designation', 'staff_id', 'official_id']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_data['role'] = 'admin'
#         user = UserRegistrationSerializer().create(user_data)
#         profile = AdminProfile.objects.create(user=user, **validated_data)
#         return profile





# class CitizenLoginSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         if self.user.role != 'citizen':
#             raise serializers.ValidationError("User is not a citizen.")
#         return data

# class OrganizationLoginSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         if self.user.role != 'organization':
#             raise serializers.ValidationError("User is not an organization.")
#         return data

# class AdminLoginSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         if self.user.role != 'admin':
#             raise serializers.ValidationError("User is not an admin.")
#         return data






# # serializers.py
# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         if email and password:
#             user = authenticate(request=self.context.get('request'), email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError(_("Invalid email or password."), code='authorization')
#         else:
#             raise serializers.ValidationError(_("Must include both email and password."), code='authorization')

#         data['user'] = user
#         return data

# class OTPRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=False)
#     phone_number = serializers.CharField(required=False)
#     verification_type = serializers.ChoiceField(choices=['email', 'phone'])
    
#     def validate(self, attrs):
#         verification_type = attrs.get('verification_type')
#         if verification_type == 'email' and not attrs.get('email'):
#             raise serializers.ValidationError('Email is required for email verification')
#         if verification_type == 'phone' and not attrs.get('phone_number'):
#             raise serializers.ValidationError('Phone number is required for phone verification')
#         return attrs

# class OTPVerifySerializer(serializers.Serializer):
#     email = serializers.EmailField(required=False)
#     phone_number = serializers.CharField(required=False)
#     code = serializers.CharField(max_length=6)
#     verification_type = serializers.ChoiceField(choices=['email', 'phone'])

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'username', 'phone_number', 'role', 'is_verified', 'created_at')
#         read_only_fields = ('id', 'email', 'role', 'created_at')