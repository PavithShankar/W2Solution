from rest_framework import permissions


class IsEmployee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        breakpoint()
        return obj.employeeinfo == request.user
