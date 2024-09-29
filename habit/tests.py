from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тесты для модели привычки"""

    def setUp(self):
        """Создание в базу записей пользователя и привычки"""
        self.user = User.objects.create(email="test1@test.ru")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            owner=self.user,
            place="test",
            time="21:00",
            action="test",
            periodicity=1,
            complete_time="00:01:30",
            is_pleasant=False,
            award="test",
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        url = reverse("habit:habit_create")
        data = {
            "owner": self.user.pk,
            "place": "test2",
            "time": "22:00",
            "action": "test2",
            "periodicity": 1,
            "complete_time": "00:01:30",
            "is_published": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_update(self):
        """Тест редактирования привычки"""
        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {
            "place": "test3",
            "owner": self.user.pk,
            "periodicity": 1,
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "test3")

    def test_habit_award_validator(self):
        """Тест валидации при создании привычки"""
        url = reverse("habit:habit_create")
        data = {
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 2,
            "complete_time": "00:01:30",
            "is_published": True,
            "award": "test4",
            "is_pleasant": False,
            "related_habit": self.habit.pk,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            [
                "У привычки может быть либо вознаграждение, либо приятная привычка",
                "Связанная привычка должна быть приятной",
            ],
        )

        # Проверка валидации при редактировании привычки
        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 2,
            "complete_time": "00:01:30",
            "is_published": True,
            "award": "test4",
            "is_pleasant": False,
            "related_habit": self.habit.pk,
        }
        response = self.client.put(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            [
                "У привычки может быть либо вознаграждение, либо приятная привычка",
                "Связанная привычка должна быть приятной",
            ],
        )

    def test_related_habit_validator(self):
        """Тест валидации при создании приятной привычки"""
        url = reverse("habit:habit_create")
        data = {
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 1,
            "complete_time": "00:01:30",
            "is_published": True,
            "award": "test4",
            "is_pleasant": True,
            "related_habit": self.habit.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            [
                "У приятной привычки не может быть вознаграждения",
                "У приятной привычки не может быть связанной привычки.",
            ],
        )

        # Проверка валидации при редактировании приятной привычки
        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 1,
            "complete_time": "00:01:30",
            "is_published": True,
            "award": "test4",
            "is_pleasant": True,
            "related_habit": self.habit.pk,
        }
        response = self.client.put(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            [
                "У приятной привычки не может быть вознаграждения",
                "У приятной привычки не может быть связанной привычки.",
            ],
        )

    def test_time_validator(self):
        """Тест валидации времени выполнения при создании привычки"""
        url = reverse("habit:habit_create")
        data = {
            "owner": self.user.pk,
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 1,
            "complete_time": "00:02:30",
            "is_published": True,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            ["Время выполнения не может быть более 2 минут"],
        )

        # Проверка валидации времени выполнения при редактировании привычки
        url = reverse("habit:habit_update", args=[self.habit.pk])
        data = {
            "owner": self.user.pk,
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 1,
            "complete_time": "00:02:30",
            "is_published": True,
        }
        response = self.client.put(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            ["Время выполнения не может быть более 2 минут"],
        )

    def test_periodicity_validator(self):
        """Тест валидации периодичности при создании привычки"""
        url = reverse("habit:habit_create")
        data = {
            "owner": self.user.pk,
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 8,
            "is_published": True,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            [
                "Поле не может быть пустым. Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            ],
        )

        # Проверка валидации периодичности при редактировании привычки
        url = reverse("habit:habit_update", args=[self.habit.pk])
        data = {
            "owner": self.user.pk,
            "place": "test4",
            "time": "22:00",
            "action": "test4",
            "periodicity": 0,
            "is_published": True,
        }
        response = self.client.put(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            [
                "Поле не может быть пустым. Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            ],
        )

    def test_list_habit_public(self):
        """Тест вывода списка публичных привычек"""
        url = reverse("habit:list_public")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_retrieve(self):
        """Тест вывода привычки пользователя"""
        url = reverse("habit:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_person(self):
        """Тест вывода привычек пользователя"""
        url = reverse("habit:list_person")
        response = self.client.get(url)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": "test",
                    "time": "21:00:00",
                    "date": "2024-01-01",
                    "action": "test",
                    "is_pleasant": False,
                    "periodicity": 1,
                    "award": "test",
                    "complete_time": "00:01:30",
                    "is_published": False,
                    "owner": self.user.pk,
                    "related_habit": None,
                }
            ],
        }
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
        self.assertEqual(len(response.data), 4)

    def test_delete_habit(self):
        """Тест удаления привычки"""
        url = reverse("habit:habit_delete", args=[self.habit.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
