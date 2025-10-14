from isort.wrap_modes import vertical_hanging_indent
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        # Для задач проверяем владельца задачи
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        # Для пользователей проверяем, что это тот же пользователь
        elif hasattr(obj, "owner") and obj.owner == request.user:
            return True
        return False


class IsManager(permissions.BasePermission):
    """
    Проверяет, является ли пользователь менеджером
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="managers").exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrManager(permissions.BasePermission):
    """
    Проверяет, является пользователь владельцем или менеджером
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Менеджер имеет доступ ко всем объектам
        if request.user.groups.filter(name="managers").exists():
            return True
        # Обычный пользователь имеет доступ только к своим объектам
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        return False
