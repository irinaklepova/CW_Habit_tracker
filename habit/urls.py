from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitListAPIView,
    HabitPersonAPIView,
    HabitCreateAPIView,
    HabitUpdateAPIView,
    HabitDeleteAPIView,
    HabitRetrieveAPIView,
)

app_name = HabitConfig.name

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="list_public"),
    path("habit/list_person/", HabitPersonAPIView.as_view(), name="list_person"),
    path("habit/create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path(
        "habit/retrieve/<int:pk>/",
        HabitRetrieveAPIView.as_view(),
        name="habit_retrieve",
    ),
    path("habit/update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("habit/delete/<int:pk>/", HabitDeleteAPIView.as_view(), name="habit_delete"),
]
