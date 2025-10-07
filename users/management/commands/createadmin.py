from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(email="admin@example.com")
        user.set_password("12345")
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
