# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Citizen endpoints
    path('citizen/',
         views.CitizenDataRequestListCreateView.as_view(), 
         name='citizen-data-requests'),
    path('citizen/<int:pk>/',
         views.CitizenDataRequestDetailView.as_view(), 
         name='citizen-data-request-detail'),
    path('citizen/<int:pk>/download/',
         views.download_data,
         name='citizen-download-data'),
    path('citizen/companies/',
         views.AvailableCompaniesView.as_view(),
         name='available-companies'),
    
    # Company endpoints
    path('company/',
         views.CompanyDataRequestListView.as_view(), 
         name='company-data-requests'),
    path('company/<int:pk>/', 
         views.CompanyDataRequestDetailView.as_view(), 
         name='company-data-request-detail'),
    path('company/<int:pk>/approve-reject/', 
         views.approve_reject_request,
         name='approve-reject-request'),
    path('company/<int:pk>/fulfill/', 
         views.fulfill_request,
         name='fulfill-request'),
    
    # Shared endpoints
    path('requests/<int:pk>/logs/', 
         views.DataRequestLogsView.as_view(), 
         name='data-request-logs'),
    
    # Admin endpoints
    path('admin/', 
         views.AdminDataRequestListView.as_view(), 
         name='admin-data-requests'),
]