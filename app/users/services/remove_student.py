from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, NotFound

from users.models import User


class RemoveStudentService:
    def __call__(self, mentor: User, data: dict) -> User:
        student = self._get_student(data)
        mentor = self._remove_student(mentor, student)

        return mentor

    def _get_student(self, data: dict) -> User:
        student_id = data.get("student_id")

        if student_id is None:
            raise ValidationError({"error": _("Не передан ID студента")})
        student = (
            User.objects.prefetch_related("students").select_related("mentor").filter(id=student_id)
        ).first()

        if not student:
            raise NotFound({"error": _("Студент не найден")})

        return student

    def _remove_student(self, mentor: User, student: User) -> User:
        if student.mentor is None:
            raise ValidationError({"error": _("У студента отсутствует ментор")})
        elif student.mentor != mentor:
            raise ValidationError({"error": _("Пользователь не является вашим студентом")})

        mentor.students.remove(student)

        return mentor
