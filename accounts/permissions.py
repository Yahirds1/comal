from rest_framework.permissions import BasePermission, SAFE_METHODS

class UserRecordPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if view.action == "list":
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.pk == request.user.pk
