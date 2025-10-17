from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from users.models import User


class TaskTestCase(APITestCase):
    """Тестирование CRUD задач"""

    def setUp(self):
        # Экземпляр пользователя
        self.user = User.objects.create(
            email="admin@example.com",
            first_name="Admin",
            last_name="Adminov"
        )
        # Экземпляр задачи
        self.task = Task.objects.create(
            title="to do task1",
            time="2025-10-25T15:15:00Z",
            status="active",
            parent_task=None,
            executor=self.user,
            owner=self.user,
        )
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_task_create(self):
        # Проверяем создание задачи
        url = reverse("tasks:task-create")
        data = {
            "title": "write code",
            "time": "2025-10-25T10:05:00Z",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_retrieve(self):
        # Проверяем вывод информации о задаче
        url = reverse("tasks:task-retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task.title)

    def test_task_update(self):
        # Проверяем обновление информации о задаче
        url = reverse("tasks:task-update", args=(self.task.pk,))
        data = {"title": "write good code"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "write good code")

    def test_task_delete(self):
        # Проверяем удаление задачи
        url = reverse("tasks:task-delete", args=(self.task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_task_list(self):
        # Проверяем вывод списка задач
        url = reverse("tasks:tasks-list")
        response = self.client.get(url)
        data = response.json()

        # Используем динамические ID вместо хардкода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

        task_data = data["results"][0]
        self.assertEqual(task_data["title"], self.task.title)
        self.assertEqual(task_data["time"], self.task.time)
        self.assertEqual(task_data["status"], self.task.status)
        self.assertEqual(task_data["parent_task"], self.task.parent_task)
        self.assertEqual(task_data["executor"], self.user.id)
        self.assertEqual(task_data["owner"], self.user.id)

    def test_task_without_executor(self):
        # Проверяет вывод списка задач без исполнителя,
        # от которых зависят другие задачи, взятые в работу
        url = reverse("tasks:tasks-without-executor")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(data["results"], [])


class ImportantTaskTestCase(APITestCase):
    """Тестирование важных задач с кандидатами"""

    def setUp(self):
        # создаем пользователей
        self.user1 = User.objects.create(
            email="user1@example.com",
            first_name="User1",
            last_name="Testov",
            position_at_work="Developer"
        )
        self.user2 = User.objects.create(
            email="user2@example.com",
            first_name="User2",
            last_name="Testov",
            position_at_work="Developer"
        )

        # Создаем важную задачу
        self.important_task = Task.objects.create(
            title="Important task",
            time="2025-10-25T15:15:00Z",
            status="active",
            parent_task=None,
            executor=None,
            owner=self.user1,
        )

        # Создаем подзадачу, которая зависит от важной задачи и имеет исполнителя
        self.subtask_with_executor = Task.objects.create(
            title="Subtask with executor",
            time="2025-10-26T15:15:00Z",
            status="active",
            parent_task=self.important_task,
            executor=self.user2,
            owner=self.user1
        )

        # Аутентификация первого пользователя
        self.client.force_authenticate(user=self.user1)

    def test_important_task_with_candidates(self):
        # Проверяет вывод списка важных задач с кандидатами
        url = reverse("tasks:important-tasks-candidates")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(len(data["results"]), 1)

        result_item = data["results"][0]
        self.assertEqual(result_item["task"]["title"], self.important_task.title)
        self.assertEqual(result_item["task"]["time"], self.important_task.time)
        self.assertEqual(result_item["deadline"], self.important_task.time)

        # Проверяем, что кандидаты есть в списке
        self.assertIsInstance(result_item["candidates"], list)
        # Проверяем, что в списке кандидатов есть пользователи
        self.assertGreater(len(result_item["candidates"]), 0)
