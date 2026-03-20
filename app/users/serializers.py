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
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_mentor",
        )


class RetrieveUserSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField(read_only=True)
    students = serializers.SerializerMethodField(read_only=True)
    mentor = serializers.CharField(source="mentor.username", read_only=True)

    def get_password(self, obj):
        request = self.context.get("request")
        if not obj.raw_password or request.user != obj:
            return ""
        return obj.raw_password

    def get_students(self, obj: User):
        if obj.is_mentor:
            return [student.username for student in obj.students.all()]
        return []

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone",
            "mentor",
            "students",
            "is_mentor",
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone",
        )


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class AddStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
