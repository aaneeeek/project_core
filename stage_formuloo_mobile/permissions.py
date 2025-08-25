from rest_framework.permissions import BasePermission


class ScrumMasterPerm(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role =='scrum_master')