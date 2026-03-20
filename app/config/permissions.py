from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = _("Вы не являетесь владельцем этого аккаунта")

    def has_object_permission(self, request, view, obj):
        return request.user and obj == request.user


class IsMentor(BasePermission):
    message = _("Вы не являетесь ментором")

    def has_permission(self, request, view):
        return request.user and request.user.is_mentor
