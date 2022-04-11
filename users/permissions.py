from rest_framework import permissions
from .models import Users


class IsOwner(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user == Users.objects.get(pk=view.kwargs['id'])
