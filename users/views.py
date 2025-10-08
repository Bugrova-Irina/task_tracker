from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # Доступно неавторизованным пользователям

    def perform_create(self, serializer):
        """Получение пользователя"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # Хеширование пароля
        user.save()


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """Обновление и получение пользователя"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
