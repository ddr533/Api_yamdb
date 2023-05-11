from rest_framework import permissions

class CastomAdminSuperUser(permissions.BasePermission):
    """
    Проверка что ты Администратор или Суперюзер
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
    Проверка что ты Модератор
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
    Проверка что ты не можешь поменять роль
    """
    def has_object_permission(self, request, view, obj):
        if request.method == ['PATCH'] and 'role' in request.data:
            new_role = request.data['role']
            if new_role != obj.role:
                return False
        return True