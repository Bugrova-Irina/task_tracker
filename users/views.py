from django.db.models import Count, Q
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from tasks.models import Task
from tasks.pagination import CustomPagination
from users.models import User
from users.permissions import IsOwner, IsOwnerOrManager
from users.serializers import UserSerializer, UserWithTasksSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # Доступно неавторизованным пользователям

    def perform_create(self, serializer):
        """Получение пользователя"""
        # Назначаем пользователя владельцем своего профиля
        user = serializer.save(is_active=True)
        user.owner = user  # Пользователь становится своим владельцем
        user.save()


class UserListAPIView(ListAPIView):
    """Получение списка пользователей с их задачами"""

    serializer_class = UserWithTasksSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        # Аннотируем количество активных задач и сортируем по убыванию
        queryset = User.objects.annotate(
            count_active_tasks=Count(
                "executor_tasks", filter=Q(executor_tasks__status=Task.ACTIVE)
            )
        ).order_by("-count_active_tasks")

        # Менеджер видит всех пользователей
        if self.request.user.groups.filter(name="managers").exists():
            return queryset
        # Обычный пользователь видит только себя
        return queryset.filter(id=self.request.user.id)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """Обновление и получение пользователя"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrManager)

    def get_object(self):
        # Менеджер может смотреть любого пользователя через ID в URL
        if (
            self.request.user.groups.filter(name="managers").exists()
            and "pk" in self.kwargs
        ):
            return User.objects.get(pk=self.kwargs["pk"])
        # Обычный пользователь может работать только со своим профилем
        return self.request.user

    def perform_update(self, serializer):
        # Менеджер не может менять пароль других пользователей
        if (
            self.request.user.groups.filter(name="managers").exists()
            and self.get_object() != self.request.user
        ):
            if "password" in serializer.validated_data:
                del serializer.validated_data["password"]
        super().perform_update(serializer)


class UserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner)  # Только владелец может удалять

    def get_object(self):
        # Пользователь может удалить только свой профиль
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
