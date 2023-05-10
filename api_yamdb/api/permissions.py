from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, \
    AllowAny


class IsAuthorOrStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    """Изменять контент может только автор, администратор, модератор."""

    message = 'Изменять контент может только его автор, модератор или админ.'
    
    def has_object_permission(self, request, view, obj):
        success_roles = ('moderator', 'admin')

        return any((request.method in SAFE_METHODS,
                    request.user == obj.author,
                    request.user.is_superuser,
                    request.user.is_authenticated and
                    request.user.role in success_roles))
