# permissions.py
from rest_framework import permissions

class IsCitizen(permissions.BasePermission):
    """
    Custom permission to only allow citizens to access citizen endpoints.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='citizen').exists()


class IsCompany(permissions.BasePermission):
    """
    Custom permission to only allow companies to access company endpoints.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='company').exists()


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins/regulators to access admin endpoints.
    """
    def has_permission(self, request, view):
        return (request.user.groups.filter(name='admin').exists() or 
                request.user.groups.filter(name='regulator').exists() or
                request.user.is_superuser)