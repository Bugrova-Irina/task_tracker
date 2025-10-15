from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.pagination import CustomPagination
from tasks.serializers import TaskSerializer, ManagerTaskSerializer
from users.permissions import IsOwner, IsOwnerOrManager, IsSuperuser


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
        if self.request.user.is_superuser or self.request.user.groups.filter(name="managers").exists():
            return Task.objects.all()
        # Обычный пользователь видит только свои задачи
        return Task.objects.filter(owner=self.request.user)


class TasksWithoutExecutorListAPIView(ListAPIView):
    """
    Вывод списка задач без исполнителя, от
    которых зависят другие задачи, взятые в работу
    """
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        # Базовый queryset - активные задачи без исполнителя
        base_queryset = Task.objects.filter(
            status=Task.ACTIVE,
            executor__isnull=True
        )

        # Подзапрос для поиска зависимых активных задач с исполнителем
        # Ищем как родительские, так и дочерние зависимости
        dependent_tasks_filter = Q(
            # Эта задача является родителем для активных задач с исполнителем
            Q(task__status=Task.ACTIVE, task__executor__isnull=False) |
            # Эта задача является дочерней у активных задач с исполнителем
            Q(parent_task__status=Task.ACTIVE, parent_task__executor__isnull=False)
        )

        # Применяем фильтр зависимых задач
        queryset = base_queryset.filter(dependent_tasks_filter).distinct()

        # Фильтрация по владельцу для обычных пользователей
        if not (self.request.user.is_superuser or self.request.user.groups.filter(name="managers").exists()):
            queryset = queryset.filter(owner=self.request.user)

        return queryset


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
        # Суперпользователь использует обычный сериализатор (полные права)
        if self.request.user.is_superuser:
            return TaskSerializer
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
    # Суперпользователь и владелец могут удалить задачи
    permission_classes = (IsAuthenticated, IsOwnerOrManager)
