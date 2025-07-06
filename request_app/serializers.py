# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DataRequest, DataRequestLog

class CitizenDataRequestSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    request_type_display = serializers.CharField(source='get_request_type_display', read_only=True)
    
    class Meta:
        model = DataRequest
        fields = [
            'id', 'company', 'company_name', 'request_type', 'request_type_display',
            'reason', 'status', 'status_display', 'created_at', 'updated_at',
            'approved_at', 'fulfilled_at', 'approval_notes', 'rejection_reason',
            'download_expires_at', 'downloaded_at'
        ]
        read_only_fields = [
            'id', 'status', 'created_at', 'updated_at', 'approved_at', 
            'fulfilled_at', 'approval_notes', 'rejection_reason',
            'download_expires_at', 'downloaded_at'
        ]
    
    def create(self, validated_data):
        # Set the citizen to the current user
        validated_data['citizen'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_company(self, value):
        # Ensure the selected company is actually a company user
        if not value.groups.filter(name='company').exists():
            raise serializers.ValidationError("Selected user is not a company.")
        return value


class CompanyDataRequestSerializer(serializers.ModelSerializer):
    citizen_name = serializers.CharField(source='citizen.username', read_only=True)
    citizen_email = serializers.CharField(source='citizen.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    request_type_display = serializers.CharField(source='get_request_type_display', read_only=True)
    
    class Meta:
        model = DataRequest
        fields = [
            'id', 'citizen', 'citizen_name', 'citizen_email', 'request_type', 
            'request_type_display', 'reason', 'status', 'status_display',
            'created_at', 'updated_at', 'approved_at', 'fulfilled_at',
            'approval_notes', 'rejection_reason'
        ]
        read_only_fields = [
            'id', 'citizen', 'citizen_name', 'citizen_email', 'request_type',
            'reason', 'created_at', 'updated_at', 'approved_at', 'fulfilled_at'
        ]


class DataRequestApprovalSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    notes = serializers.CharField(required=False, allow_blank=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if data['action'] == 'reject' and not data.get('rejection_reason'):
            raise serializers.ValidationError(
                "Rejection reason is required when rejecting a request."
            )
        return data


class DataRequestLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)
    
    class Meta:
        model = DataRequestLog
        fields = ['action', 'performed_by_name', 'timestamp', 'details']


class CompanyListSerializer(serializers.ModelSerializer):
    """Serializer for listing available companies"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']