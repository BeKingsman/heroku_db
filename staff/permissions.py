from rest_framework import permissions
from django.http import HttpResponse





class IsStaffOrAdmin(permissions.BasePermission):
    message = "you are not authorised"

    def has_object_permission(self,request,view,object):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
                return True
        if request.user.is_superuser:
                return True
