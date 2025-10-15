from django.db import models


class Task(models.Model):
    """Модель задачи"""

    # Статусы задачи
    ACTIVE = "active"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (ACTIVE, "В работе"),
        (COMPLETED, "Завершена"),
    ]

    title = models.CharField(
        max_length=250,
        verbose_name="Название задачи",
        help_text="укажите название задачи",
    )
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Родительская задача",
        help_text="Укажите родительскую задачу",
    )
    executor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Исполнитель",
        help_text="Укажите исполнителя",
        related_name="executor_tasks",
    )
    time = models.DateTimeField(
        verbose_name="Когда должно быть готово",
        help_text="Укажите дату и время, когда должно быть готово",
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=ACTIVE,
        verbose_name="Статус задачи",
        help_text="Укажите статус задачи",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Владелец задачи",
        help_text="Укажите владельца задачи",
        related_name="owned_tasks",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
