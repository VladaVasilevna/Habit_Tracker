from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="test@gmail.com", password="password"
        )
        cls.habit = Habit.objects.create(
            location="Парк",
            time="19:00",
            owner=cls.user,
            action="Бег",
            execution_time=30,
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse("habits:habits_create")
        data = {
            "location": "Спортзал",
            "time": "18:00",
            "action": "Тренировка",
            "execution_time": "60",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.count(), 1)

    def test_update_habit(self):
        url = reverse("habits:habits_update", args=(self.habit.pk,))
        data = {
            "location": "Басейн",
            "time": "8:00",
            "action": "Плавание",
            "execution_time": "120",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Плавание")

    def test_retrieve_habit(self):
        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Бег")

    def test_delete_habit(self):
        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
