from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import (TaskListAPIView, TaskRetrieveAPIView,
                         TaskUpdateAPIView, TaskCreateAPIView,
                         TaskDestroyAPIView, TasksWithoutExecutorListAPIView)

app_name = TasksConfig.name

urlpatterns = [
    path("", TaskListAPIView.as_view(), name="tasks-list"),
    path("<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-retrieve"),
    path("<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task-delete"),
    path("no-executor/", TasksWithoutExecutorListAPIView.as_view(), name="tasks-without-executor"),
]
