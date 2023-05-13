from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class UserPermissions(permissions.IsAuthenticated):
    """Управление правами доступа к модели User."""

    message = 'У вас недостаточно прав.'

    def has_permission(self, request, view):
        if view.action in ('list', 'destroy'):
            return request.user.is_authenticated and request.user.is_admin
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):

        return any((request.user.username == obj.username
                    and request.method != 'PATCH',
                    request.user.is_admin))


class IsAuthorOrStaffOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Изменять контент может только автор, администратор, модератор."""

    message = 'Изменять контент может только его автор, модератор или админ.'

    ALLOW_EDIT = ('moderator', 'admin')

    def has_object_permission(self, request, view, obj):

        return any((request.method in permissions.SAFE_METHODS,
                    request.user == obj.author,
                    request.user.is_superuser,
                    request.user.is_authenticated
                    and request.user.role in self.ALLOW_EDIT))


class AdminOrReadOnly(permissions.IsAuthenticated):

    message = 'Изменять контент может только админ.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return any((request.method in permissions.SAFE_METHODS,
                    request.user.is_authenticated and request.user.is_admin))
