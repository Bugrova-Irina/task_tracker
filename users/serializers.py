from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.serializers import ModelSerializer

from tasks.serializers import UserTaskSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "position_at_work",
            "avatar",
            "password"
        )
        extra_kwargs = {
            "password": {"write_only": True}  # Пароль только для записи
        }

    def create(self, validated_data):
        """Обновление пользователя с хешированием пароля"""
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        return user


class UserWithTasksSerializer(ModelSerializer):
    """Сериализатор списка пользователей с задачами"""
    tasks = SerializerMethodField()
    count_active_tasks = IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "position_at_work",
            "tasks",
            "count_active_tasks",
        )

    def get_tasks(self, obj):
        # Получаем задачи, где пользователь является исполнителем
        tasks = obj.executor_tasks.all()
        return UserTaskSerializer(tasks, many=True).data
