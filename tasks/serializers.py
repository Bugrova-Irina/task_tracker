from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class UserTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения задач пользователя"""
    class Meta:
        model = Task
        fields = ("title", "time", "status")


class ManagerTaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор задач для менеджера - может менять только исполнителя
    """
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["title", "parent_task", "time", "status", "owner"]

    def to_internal_value(self, data):
        # Получаем список read-only полей
        read_only_fields = getattr(self.Meta, "read_only_fields", [])

        # Проверяем попытку пользователя изменить read-only поля
        for field_name in read_only_fields:
            if field_name in data:
                raise serializers.ValidationError({
                    field_name: f"Поле '{field_name}' не может быть изменено менеджером"
                })

        return super().to_internal_value(data)
