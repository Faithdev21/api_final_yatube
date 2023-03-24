from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author or request.user.is_staff


class IfUserNotFollowing(permissions.BasePermission):
    message = 'Нельзя подписаться на самого себя'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user != obj.following:
            return True
