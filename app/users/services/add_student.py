from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, NotFound

from users.models import User


class AddStudentService:
    def __call__(self, mentor: User, data: dict) -> User:
        student = self._get_student(data)
        mentor = self._add_student(mentor, student)

        return mentor

    def _get_student(self, data: dict) -> User:
        student_id = data.get("student_id")

        if student_id is None:
            raise ValidationError({"error": _("Не передан ID студента")})
        student = (
            User.objects.prefetch_related("students")
            .select_related("mentor")
            .filter(id=student_id)
            .first()
        )

        if not student:
            raise NotFound({"error": _("Студент не найден")})

        return student

    def _add_student(self, mentor: User, student: User) -> User:
        if mentor == student:
            raise ValidationError(
                {"error": _("Нельзя добавлять себя в качестве студента")}
            )

        if student.mentor:
            if student.mentor != mentor:
                raise ValidationError(
                    {"error": _("У студента уже есть ментор")}
                )
            else:
                raise ValidationError(
                    {"error": _("Студент уже числится у вас")}
                )

        mentor.students.add(student)

        return mentor
