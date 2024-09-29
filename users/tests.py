from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тест для модели пользователя"""

    def setUp(self):
        pass

    def test_user_create_login(self):
        """Тест создания и регистрации пользователя"""
        url = reverse("users:register")
        data = {
            "email": "test@test.ru",
            "password": "12345678",
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(data.get("email"), "test@test.ru")
