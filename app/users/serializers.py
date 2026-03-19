from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=False, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = PhoneNumberField(required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "phone")


class RetrieveUserSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField(read_only=True)

    def get_password(self, obj):
        request = self.context.get("request")
        if not obj.raw_password or request.user != obj:
            return ""
        return obj.raw_password

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "phone")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "phone")
