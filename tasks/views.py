from pydoc import pager

from django.core.serializers import serialize
from django.db.models import Q, Count
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.models import Task
from tasks.pagination import CustomPagination
from tasks.serializers import TaskSerializer, ManagerTaskSerializer, TaskWithCandidatesSerializer
from users.models import User
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


class ImportantTaskWithCandidatesAPIView(ListAPIView):
    """
    Вывод списка важных задач (без исполнителя, но с зависимостями)
    с рекомендованными исполнителями
    """
    serializer_class = TaskWithCandidatesSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrManager | IsSuperuser)
    pagination_class = CustomPagination

    def get_queryset(self):
        # Получаем важные задачи - активные, без исполнителя
        # от которых зависят другие задачи
        important_tasks = Task.objects.filter(
            status=Task.ACTIVE,
            executor__isnull=True
        ).filter(
            Q(task__status=Task.ACTIVE, task__executor__isnull=False) |
            Q(parent_task__status=Task.ACTIVE, parent_task__executor__isnull=False)
        ).distinct()

        # Аннотируем пользователей с количеством активных задач
        users_with_counts = User.objects.annotate(
            active_tasks_count=Count(
                "executor_tasks",
                filter=Q(executor_tasks__status=Task.ACTIVE)
            )
        )

        # Создаем словарь для быстрого доступа к количеству задач по ID пользователя
        user_tasks_count = {
            user.id: user.active_tasks_count
            for user in users_with_counts
        }

        # Находим минимальное количество задач
        if users_with_counts.exists():
            min_tasks_count = min(user_tasks_count.values())
        else:
            min_tasks_count = 0

        # Получаем наименее загруженных пользователей
        least_loaded_users = [
            user for user in users_with_counts
            if user.active_tasks_count == min_tasks_count
        ]

        # Собираем результат
        result = []
        for task in important_tasks:
            candidates = list(least_loaded_users)

            # Добавляем исполнителя родительской задачи, если он не сильно загружен
            if task.parent_task and task.parent_task.executor:
                parent_executor_id = task.parent_task.executor.id
                if parent_executor_id in user_tasks_count:
                    parent_executor_count = user_tasks_count[parent_executor_id]

                    if parent_executor_count <= min_tasks_count + 2:
                        # Находим полный объект пользователя
                        parent_executor = next(
                            (user for user in users_with_counts if user.id == parent_executor_id),
                            None
                        )
                        if parent_executor and parent_executor not in candidates:
                            candidates.append(parent_executor)

            # Создаем объект результата
            result.append({
                "task": task,
                "candidates": candidates
            })

        return result

    def list(self, request, *args, **kwargs):
        # Переопределяем list для обработки не-Queryset
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
