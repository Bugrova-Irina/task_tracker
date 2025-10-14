from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView, UserDestroyAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("profile/", UserUpdateAPIView.as_view(), name="profile"),
    path("profile/<int:pk>/", UserUpdateAPIView.as_view(), name="user-detail"),
    path("profile/delete/", UserDestroyAPIView.as_view(), name="delete"),
    path("profile/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("", UserListAPIView.as_view(), name="users-list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token-refresh",
    ),
]
