from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password123"
        )

        self.mentor = User.objects.create_user(
            username="mentor", email="mentor@test.com", password="password123", is_mentor=True
        )

        self.student = User.objects.create_user(
            username="student", email="student@test.com", password="password123"
        )

    def auth(self, user):
        self.client.force_authenticate(user)

    def test_registration(self):
        url = reverse("v0:users:users-registration")

        data = {
            "username": "new_user",
            "email": "new@test.com",
            "password": "password123",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_retrieve_user(self):
        self.auth(self.user)

        url = reverse("v0:users:users-detail", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_partial_update(self):
        self.auth(self.user)

        url = reverse("v0:users:users-detail", args=[self.user.id])
        response = self.client.patch(url, {"first_name": "Updated"})

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_not_owner(self):
        other = User.objects.create_user(username="other", password="123456")
        self.auth(other)

        url = reverse("v0:users:users-detail", args=[self.user.id])
        response = self.client.patch(url, {"first_name": "Hack"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_student_success(self):
        self.auth(self.mentor)

        url = reverse("v0:users:users-add-student")
        response = self.client.post(url, {"student_id": self.student.id})

        self.student.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.student.mentor, self.mentor)

    def test_add_student_errors(self):
        self.auth(self.mentor)

        url = reverse("v0:users:users-add-student")

        # нет id
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

        # не найден
        response = self.client.post(url, {"student_id": 999})
        self.assertEqual(response.status_code, 404)

        # сам себя
        response = self.client.post(url, {"student_id": self.mentor.id})
        self.assertEqual(response.status_code, 400)

    def test_remove_student(self):
        self.auth(self.mentor)

        self.mentor.students.add(self.student)

        url = reverse("v0:users:users-remove-student")
        response = self.client.post(url, {"student_id": self.student.id})

        self.student.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.student.mentor)

    def test_remove_student_error(self):
        self.auth(self.mentor)

        url = reverse("v0:users:users-remove-student")
        response = self.client.post(url, {"student_id": self.student.id})

        self.assertEqual(response.status_code, 400)


class UserLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password123"
        )

    def auth(self, user):
        self.client.force_authenticate(user)

    def test_logout(self):
        self.auth(self.user)

        refresh = RefreshToken.for_user(self.user)

        url = reverse("v0:users:logout")
        response = self.client.post(url, {"refresh": str(refresh)})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_invalid(self):
        self.auth(self.user)

        url = reverse("v0:users:logout")
        response = self.client.post(url, {"refresh": "invalid"})

        self.assertEqual(response.status_code, 400)
