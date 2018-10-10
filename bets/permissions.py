from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class UpdateOwnObjects(permissions.BasePermission):
    """allow users to edit their own objects"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST" and request.user.id != obj.user.id:
            raise PermissionDenied("Not Allowed")
        return obj.user.id == request.user.id


class UserPrivateData(permissions.BasePermission):
    """ allows only user to manipulate with data - PRIVATE CRUD"""

    def has_object_permission(self, request, view, obj):
        if request.method == "POST" and request.user.id != obj.user.id:
            raise PermissionDenied("Not Allowed")
        return obj.user.id == request.user.id


class OnlySafeMethods(permissions.BasePermission):
    """for SAFE only methods"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class RegisterUserPostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return True
        return False
