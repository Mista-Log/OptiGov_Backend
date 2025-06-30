from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, CitizenProfile, OrganizationProfile, AdminProfile
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'phone_number', 'role', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def validate_role(self, value):
        if value not in ['citizen', 'organization']:
            raise serializers.ValidationError("Invalid role. Only 'citizen' and 'organization' are allowed for registration.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class CitizenProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = CitizenProfile
        fields = ['user', 'date_of_birth', 'address', 'gender', 'national_id_number', 'id_document']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'citizen'
        user = UserRegistrationSerializer().create(user_data)
        profile = CitizenProfile.objects.create(user=user, **validated_data)
        return profile
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class OrganizationProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = OrganizationProfile
        fields = [
            'user', 'company_name', 'cac_number', 'tax_id_number',
            'company_address', 'industry_type',
            'cac_certificate', 'tax_clearance_certificate'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'organization'
        user = UserRegistrationSerializer().create(user_data)
        profile = OrganizationProfile.objects.create(user=user, **validated_data)
        return profile


class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = AdminProfile
        fields = ['user', 'government_agency', 'designation', 'staff_id', 'official_id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'admin'
        user = UserRegistrationSerializer().create(user_data)
        profile = AdminProfile.objects.create(user=user, **validated_data)
        return profile




# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError(_("Invalid email or password."), code='authorization')
        else:
            raise serializers.ValidationError(_("Must include both email and password."), code='authorization')

        data['user'] = user
        return data

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    verification_type = serializers.ChoiceField(choices=['email', 'phone'])
    
    def validate(self, attrs):
        verification_type = attrs.get('verification_type')
        if verification_type == 'email' and not attrs.get('email'):
            raise serializers.ValidationError('Email is required for email verification')
        if verification_type == 'phone' and not attrs.get('phone_number'):
            raise serializers.ValidationError('Phone number is required for phone verification')
        return attrs

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    code = serializers.CharField(max_length=6)
    verification_type = serializers.ChoiceField(choices=['email', 'phone'])

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone_number', 'role', 'is_verified', 'created_at')
        read_only_fields = ('id', 'email', 'role', 'created_at')