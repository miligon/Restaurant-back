from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow HEAD or OPTIONS requests.
        if request.method in ('HEAD', 'OPTIONS'):
            return True

        return obj.owner == request.user