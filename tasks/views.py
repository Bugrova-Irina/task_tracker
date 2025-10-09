from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.pagination import CustomPagination
from tasks.serializers import TaskSerializer
from users.permissions import IsOwner


class TaskCreateAPIView(CreateAPIView):
    """Создание задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Назначение пользователя владельцем задачи
        serializer.save(owner = self.request.user)


class TaskListAPIView(ListAPIView):
    """Вывод списка задач"""

    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = CustomPagination

    def get_queryset(self):
        # Возвращаем задачи только текущего пользователя
        return Task.objects.filter(owner=self.request.user)


class TaskRetrieveAPIView(RetrieveAPIView):
    """Вывод страницы задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class TaskUpdateAPIView(UpdateAPIView):
    """Обновление задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class TaskDestroyAPIView(DestroyAPIView):
    """Удаление задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)
