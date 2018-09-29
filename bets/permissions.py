from rest_framework import permissions


class UpdateOwnObjects(permissions.BasePermission):
    """allow users to edit their own objects"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # TODO - BETTER
        if request.method == "POST" and request.user.id != obj.user.id:
            raise PermissionError("Not Allowed")
        return obj.user.id == request.user.id


class UserPrivateData(permissions.BasePermission):
    """ allows only user to manipulate with data - PRIVATE CRUD"""

    def has_object_permission(self, request, view, obj):
        # TODO BETTER
        # Not working from POSTMAN
        if request.method == "POST" and request.user.id != obj.user.id:
            raise PermissionError("Not Allowed")
        return obj.user.id == request.user.id
