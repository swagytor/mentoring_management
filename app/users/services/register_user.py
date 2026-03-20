from users.models import User


class RegisterUserService:
    def __call__(self, data: dict) -> User:
        data = self._validate_data(data)
        user = self._create_user(data)

        return user

    def _validate_data(self, data: dict) -> dict:
        data["raw_password"] = data["password"]

        return data

    def _create_user(self, data: dict) -> User:
        return User.objects.create_user(**data)
