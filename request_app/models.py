# from django.db import models

# # Create your models here.
# # models.py
# from django.db import models
# from accounts.models import User
# from django.utils import timezone
# from accounts.models import CitizenProfile, OrganizationProfile, AdminProfile


# class DataRequest(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#         ('fulfilled', 'Fulfilled'),
#     ]
    
#     REQUEST_TYPES = [
#         ('personal_data', 'Personal Data'),
#         ('transaction_history', 'Transaction History'),
#         ('account_details', 'Account Details'),
#         ('all_data', 'All Data'),
#     ]
    
#     citizen = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE, 
#         related_name='data_requests',
#         limit_choices_to={'groups__name': 'citizen'}
#     )
#     company = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE, 
#         related_name='received_requests',
#         limit_choices_to={'groups__name': 'company'}
#     )
#     request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
#     reason = models.TextField(help_text="Reason for data request")
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     approved_at = models.DateTimeField(null=True, blank=True)
#     fulfilled_at = models.DateTimeField(null=True, blank=True)
    
#     # Approval details
#     approved_by = models.ForeignKey(
#         User, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True,
#         related_name='approved_requests'
#     )
#     approval_notes = models.TextField(blank=True)
#     rejection_reason = models.TextField(blank=True)
    
#     # Data delivery
#     data_file = models.FileField(upload_to='data_exports/', null=True, blank=True)
#     download_expires_at = models.DateTimeField(null=True, blank=True)
#     downloaded_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         ordering = ['-created_at']
        
#     def __str__(self):
#         return f"{self.citizen.username} - {self.request_type} - {self.status}"
    
#     def mark_as_approved(self, approved_by, notes=""):
#         self.status = 'approved'
#         self.approved_by = approved_by
#         self.approved_at = timezone.now()
#         self.approval_notes = notes
#         self.save()
    
#     def mark_as_rejected(self, rejected_by, reason):
#         self.status = 'rejected'
#         self.approved_by = rejected_by
#         self.rejection_reason = reason
#         self.updated_at = timezone.now()
#         self.save()
    
#     def mark_as_fulfilled(self, data_file=None):
#         self.status = 'fulfilled'
#         self.fulfilled_at = timezone.now()
#         if data_file:
#             self.data_file = data_file
#             # Set download expiry (e.g., 30 days)
#             self.download_expires_at = timezone.now() + timezone.timedelta(days=30)
#         self.save()


# class DataRequestLog(models.Model):
#     """Track all actions on data requests for audit purposes"""
#     request = models.ForeignKey(DataRequest, on_delete=models.CASCADE, related_name='logs')
#     action = models.CharField(max_length=50)  # created, approved, rejected, fulfilled, downloaded
#     performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     details = models.JSONField(default=dict)
    
#     class Meta:
#         ordering = ['-timestamp']

# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class DataRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    ]
    
    REQUEST_TYPES = [
        ('personal_data', 'Personal Data'),
        ('transaction_history', 'Transaction History'),
        ('account_details', 'Account Details'),
        ('all_data', 'All Data'),
    ]
    
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='data_requests',
        limit_choices_to={'user_type': 'citizen'}
    )
    organization = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_requests',
        limit_choices_to={'user_type': 'organization'}
    )
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    reason = models.TextField(help_text="Reason for data request")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    
    # Approval details
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_requests'
    )
    approval_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Data delivery
    data_file = models.FileField(upload_to='data_exports/', null=True, blank=True)
    download_expires_at = models.DateTimeField(null=True, blank=True)
    downloaded_at = models.DateTimeField(null=True, blank=True)
    
    # Regulator monitoring
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(blank=True)
    flagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flagged_requests'
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.citizen.email} - {self.request_type} - {self.status}"
    
    def mark_as_approved(self, approved_by, notes=""):
        self.status = 'approved'
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.approval_notes = notes
        self.save()
    
    def mark_as_rejected(self, rejected_by, reason):
        self.status = 'rejected'
        self.approved_by = rejected_by
        self.rejection_reason = reason
        self.updated_at = timezone.now()
        self.save()
    
    def mark_as_fulfilled(self, data_file=None):
        self.status = 'fulfilled'
        self.fulfilled_at = timezone.now()
        if data_file:
            self.data_file = data_file
            # Set download expiry (e.g., 30 days)
            self.download_expires_at = timezone.now() + timezone.timedelta(days=30)
        self.save()


class DataRequestLog(models.Model):
    """Track all actions on data requests for audit purposes"""
    request = models.ForeignKey(DataRequest, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50)  # created, approved, rejected, fulfilled, downloaded, flagged
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-timestamp']

