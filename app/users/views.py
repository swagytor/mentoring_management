from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from config.permissions import IsOwner
from users.models import User
from users.serializers import (
    UserSerializer,
    RegisterUserSerializer,
    UpdateUserSerializer,
    RetrieveUserSerializer,
)
from users.services import RegisterUserService


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "registration":
            return RegisterUserSerializer
        elif self.action == "retrieve":
            return RetrieveUserSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateUserSerializer

        return UserSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == "registration":
            return [AllowAny()]

        return super().get_permissions()

    @action(detail=False, methods=["post"])
    def registration(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        RegisterUserService()(serializer.validated_data)

        return Response({"detail": "Регистрация прошла успешно"}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
