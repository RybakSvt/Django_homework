from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только владельцу объекта.
    Для задач и подзадач.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем, запись только администраторам.
    Используется для категорий.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAuthenticatedForModification(permissions.BasePermission):
    """
    Чтение для всех, создание/изменение только для аутентифицированных.
    Используется для задач.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated