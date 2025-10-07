from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None  # Авторизация по email

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Укажите почту",
    )
    name = models.CharField(
        max_length=150,
        verbose_name="ФИО",
        help_text="Укажите ФИО"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    position_at_work = models.CharField(
        max_length=250,
        verbose_name="Должность",
        help_text="Укажите должность",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Добавьте аватар",
    )

    # Авторизация по email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return f"{self.name} - {self.position_at_work}"
