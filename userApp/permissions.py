from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin" or request.user.is_superuser
