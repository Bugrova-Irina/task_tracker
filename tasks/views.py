from django.core.serializers import serialize
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.pagination import CustomPagination
from tasks.serializers import TaskSerializer, ManagerTaskSerializer
from users.permissions import IsOwner, IsManager, IsOwnerOrManager


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
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        # Менеджер видит все задачи
        if self.request.user.groups.filter(name="managers").exists():
            return Task.objects.all()
        # Обычный пользователь видит только свои задачи
        return Task.objects.filter(owner=self.request.user)


class TaskRetrieveAPIView(RetrieveAPIView):
    """Вывод страницы задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrManager)


class TaskUpdateAPIView(UpdateAPIView):
    """Обновление задачи"""

    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrManager)

    def get_serializer_class(self):
        # Менеджер использует специальный сериализатор
        if self.request.user.groups.filter(name="managers").exists():
            return ManagerTaskSerializer
        return TaskSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        # Для менеджера дополнительно делаем поле executor необязательным при обновлении
        if self.request.user.groups.filter(name="managers").exists():
            serializer.fields["executor"].required = False
        return serializer


class TaskDestroyAPIView(DestroyAPIView):
    """Удаление задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)  # Только владелец может удалить
