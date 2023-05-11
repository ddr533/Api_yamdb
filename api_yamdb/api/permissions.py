from rest_framework import permissions
from django.http import HttpResponseForbidden


class CastomAdminSuperUser(permissions.BasePermission):
    """
    Проверка что ты Администратор или Суперюзер.
    """
    
    def has_permission(self, request, view):
         if request.method in ['POST']:
            return True
         
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser or
            obj.role == 'admin'
        )
    
class CastomModerator(permissions.BasePermission):
    """
    Проверка что ты Модератор.
    """
    
    def has_permission(self, request, view):
         if request.method in ['POST']:
            return True
         
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser or
            obj.role == 'moderator'
        )
    
class UserUpdateRole(permissions.BasePermission):
    """
    Проверка что ты не можешь поменять роль.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method == ['PATCH'] and 'role' in request.data:
            new_role = request.data['role']
            if new_role != obj.role:
                return False
        return True


class IsAuthorOrStaffOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Изменять контент может только автор, администратор, модератор."""

    message = 'Изменять контент может только его автор, модератор или админ.'

    ALLOW_EDIT = ('moderator', 'admin')
    
    def has_object_permission(self, request, view, obj):

        return any((request.method in permissions.SAFE_METHODS,
                    request.user == obj.author,
                    request.user.is_superuser,
                    request.user.is_authenticated and
                    request.user.role in self.ALLOW_EDIT))


class AdminOrReadOnly(permissions.BasePermission):

    message = 'Изменять контент может только админ.'

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return any((request.method in permissions.SAFE_METHODS,
                    request.user.is_superuser,
                    request.user.is_authenticated and
                    request.user.role == 'admin'))

