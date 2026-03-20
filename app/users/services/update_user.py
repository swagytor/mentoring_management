from django.contrib.auth.hashers import make_password

from users.models import User


class UpdateUserService:
    def __call__(self, user: User, data: dict) -> User:
        data = self._validate_data(data)
        user = self._update_user(user, data)
        return user

    def _update_user(self, user, data):
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.save(
            update_fields=["first_name", "last_name", "email", "password", "raw_password", "phone"]
        )

        return user

    def _validate_data(self, data: dict) -> dict:
        raw_password = data["password"]
        data["raw_password"] = raw_password
        data["password"] = make_password(raw_password)

        return data
