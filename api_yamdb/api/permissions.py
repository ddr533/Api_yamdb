from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    ALLOW_EDIT = ('admin', )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_superuser
                or request.user.role in self.ALLOW_EDIT
                )
