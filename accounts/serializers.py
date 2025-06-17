from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, OTPVerification
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

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs

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