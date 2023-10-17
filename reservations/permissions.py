"""
Model that holds custom permission classes fro app 'reservations'
"""
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission class to check if the requesting user is the owner
    of the associated restaurant.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('HEAD', 'OPTIONS'):
            return True

        return obj.restaurant.owner == request.user
