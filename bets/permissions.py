from rest_framework import permissions


class UpdateOwnObjects(permissions.BasePermission):
    """allow users to edit their own objects"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id
