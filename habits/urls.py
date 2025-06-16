from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    PublicHabitListAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habits_list"),
    path("create/", HabitCreateAPIView.as_view(), name="habits_create"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habits_update"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habits_retrieve"),
    path(
        "<int:pk>/delete/",
        HabitDestroyAPIView.as_view(),
        name="habits_delete",
    ),
    path("public/", PublicHabitListAPIView.as_view(), name="public_habits"),
]
