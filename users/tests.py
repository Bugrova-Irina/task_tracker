from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тестирование CRUD пользователя"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(
            email="admin@example.com",
            first_name="Admin",
            last_name="Adminov",
            position_at_work="Superuser"
        )
        self.user.set_password("12345")
        self.user.save()

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        # Проверяем вывод информации о пользователе
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):
        # Проверяем создание пользователя
        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "position_at_work": "programmer",
            "password": "12345"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        # Проверяем обновление информации о пользователе
        url = reverse("users:user-update", args=(self.user.pk,))
        data = {"first_name": "Petr"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("first_name"), "Petr")

    def test_user_delete(self):
        # Проверяем удаление пользователя
        url = reverse("users:delete")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
