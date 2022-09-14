from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Пермишн для чтения, либо для админа"""
    message = 'Для редактирования Вы должны иметь права администратора '

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin))


class ReviewAndComment(permissions.BasePermission):
    """Пермишн отзывов и комментариев"""
    message = ('Для редактирования Вы должны  быть автором контента '
               'и/или иметь права администратора либо модератора.')

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    """Пермишн для админа"""
    message = 'Вы должны иметь права администратора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
