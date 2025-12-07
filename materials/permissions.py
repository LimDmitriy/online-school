from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Permission для проверки группы модератор,
    Модератор может смотреть и редактировать
    """

    message = "Модератору нельзя создавать или удалять!!!"

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True

        is_moderator = user.groups.filter(name="Moderator").exists()

        if is_moderator:
            if view.action in ("list", "retrieve", "update", "partial_update"):
                return True

            if view.action in ("create", "destroy"):
                return False

        return True


class IsOwnerOrModerator(BasePermission):
    """Permission для проверки владельца"""

    message = "Доступно только для владельца!!!"

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True

        is_moderator = user.groups.filter(name="Moderator").exists()

        if is_moderator:
            return True
        return obj.owner == user
