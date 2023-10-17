"""
Model that holds custom permission classes fro app 'permissions'
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission class to check if the user is the owner
    of the restaurant.
    """
    def has_object_permission(self, request, view, obj):
        # Allow HEAD or OPTIONS requests.
        if request.method in ('HEAD', 'OPTIONS'):
            return True

        return obj.owner == request.user
