from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}  # Пароль только для записи
        }

    def update(self, instance, validated_data):
        """Обновление пользователя с хешированием пароля"""
        password = validated_data.pop("password", None)

        # Обновляем остальные поля
        instance = super().update(instance, validated_data)

        # Если передан пароль, хешируем его
        if password:
            instance.set_password(password)
            instance.save()

        return instance
