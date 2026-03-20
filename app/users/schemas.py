from drf_spectacular.utils import extend_schema

from users.serializers import UserLogoutSerializer

user_logout_schema_view: dict = {
    "post": extend_schema(
        methods=["POST"],
        summary="Выход из авторизации",
        request=UserLogoutSerializer,
    )
}
