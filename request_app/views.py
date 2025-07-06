from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.utils import timezone
from .models import DataRequest, DataRequestLog
from .serializers import (
    CitizenDataRequestSerializer, CompanyDataRequestSerializer,
    DataRequestApprovalSerializer, CompanyListSerializer, DataRequestLogSerializer
)
from .permissions import IsCitizen, IsCompany, IsAdmin


class CitizenDataRequestListCreateView(generics.ListCreateAPIView):
    """
    Citizen endpoint to:
    - GET: List their own data requests
    - POST: Create new data requests
    """
    serializer_class = CitizenDataRequestSerializer
    permission_classes = [IsAuthenticated, IsCitizen]
    
    def get_queryset(self):
        return DataRequest.objects.filter(citizen=self.request.user)
    
    def perform_create(self, serializer):
        request_obj = serializer.save()
        # Log the creation
        DataRequestLog.objects.create(
            request=request_obj,
            action='created',
            performed_by=self.request.user,
            details={'request_type': request_obj.request_type}
        )


class CitizenDataRequestDetailView(generics.RetrieveAPIView):
    """
    Citizen endpoint to view details of their specific data request
    """
    serializer_class = CitizenDataRequestSerializer
    permission_classes = [IsAuthenticated, IsCitizen]
    
    def get_queryset(self):
        return DataRequest.objects.filter(citizen=self.request.user)


class CompanyDataRequestListView(generics.ListAPIView):
    """
    Company endpoint to list data requests sent to them
    """
    serializer_class = CompanyDataRequestSerializer
    permission_classes = [IsAuthenticated, IsCompany]
    
    def get_queryset(self):
        return DataRequest.objects.filter(company=self.request.user)


class CompanyDataRequestDetailView(generics.RetrieveAPIView):
    """
    Company endpoint to view details of a specific data request
    """
    serializer_class = CompanyDataRequestSerializer
    permission_classes = [IsAuthenticated, IsCompany]
    
    def get_queryset(self):
        return DataRequest.objects.filter(company=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCompany])
def approve_reject_request(request, pk):
    """
    Company endpoint to approve or reject a data request
    """
    data_request = get_object_or_404(
        DataRequest, 
        pk=pk, 
        company=request.user,
        status='pending'
    )
    
    serializer = DataRequestApprovalSerializer(data=request.data)
    if serializer.is_valid():
        action = serializer.validated_data['action']
        notes = serializer.validated_data.get('notes', '')
        rejection_reason = serializer.validated_data.get('rejection_reason', '')
        
        if action == 'approve':
            data_request.mark_as_approved(request.user, notes)
            log_action = 'approved'
            log_details = {'notes': notes}
        else:
            data_request.mark_as_rejected(request.user, rejection_reason)
            log_action = 'rejected'
            log_details = {'rejection_reason': rejection_reason}
        
        # Log the action
        DataRequestLog.objects.create(
            request=data_request,
            action=log_action,
            performed_by=request.user,
            details=log_details
        )
        
        return Response({
            'message': f'Request {action}d successfully',
            'status': data_request.status
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCompany])
def fulfill_request(request, pk):
    """
    Company endpoint to fulfill an approved data request by uploading data
    """
    data_request = get_object_or_404(
        DataRequest,
        pk=pk,
        company=request.user,
        status='approved'
    )
    
    if 'data_file' not in request.FILES:
        return Response(
            {'error': 'Data file is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data_file = request.FILES['data_file']
    data_request.mark_as_fulfilled(data_file)
    
    # Log the fulfillment
    DataRequestLog.objects.create(
        request=data_request,
        action='fulfilled',
        performed_by=request.user,
        details={'filename': data_file.name}
    )
    
    return Response({
        'message': 'Request fulfilled successfully',
        'download_expires_at': data_request.download_expires_at
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCitizen])
def download_data(request, pk):
    """
    Citizen endpoint to download their fulfilled data request
    """
    data_request = get_object_or_404(
        DataRequest,
        pk=pk,
        citizen=request.user,
        status='fulfilled'
    )
    
    # Check if download has expired
    if data_request.download_expires_at and timezone.now() > data_request.download_expires_at:
        raise Http404("Download link has expired")
    
    if not data_request.data_file:
        raise Http404("Data file not available")
    
    # Update downloaded timestamp
    data_request.downloaded_at = timezone.now()
    data_request.save()
    
    # Log the download
    DataRequestLog.objects.create(
        request=data_request,
        action='downloaded',
        performed_by=request.user,
        details={}
    )
    
    # Return file response
    return FileResponse(
        data_request.data_file.open('rb'),
        as_attachment=True,
        filename=f"data_export_{data_request.id}.zip"
    )


class AvailableCompaniesView(generics.ListAPIView):
    """
    Citizen endpoint to get list of available companies
    """
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated, IsCitizen]
    
    def get_queryset(self):
        company_group = Group.objects.get(name='company')
        return User.objects.filter(groups=company_group, is_active=True)


class DataRequestLogsView(generics.ListAPIView):
    """
    View logs for a specific data request (available to citizen and company)
    """
    serializer_class = DataRequestLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        request_id = self.kwargs['pk']
        data_request = get_object_or_404(DataRequest, pk=request_id)
        
        # Check permissions
        if (self.request.user != data_request.citizen and 
            self.request.user != data_request.company):
            return DataRequestLog.objects.none()
        
        return DataRequestLog.objects.filter(request=data_request)


# Admin views (optional)
class AdminDataRequestListView(generics.ListAPIView):
    """
    Admin endpoint to view all data requests
    """
    serializer_class = CompanyDataRequestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = DataRequest.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add filtering options
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset