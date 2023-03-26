from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """Проверка является ли пользователь автором
    или администратором при изменении контента."""
    message: str = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj) -> bool:
        """Установка разрешения на уровне объекта изменять
        контент только с правами автора или администратора"""
        return (request.method in permissions.SAFE_METHODS
                or (request.user == obj.author or request.user.is_staff))
