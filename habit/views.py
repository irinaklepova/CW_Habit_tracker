from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from habit.models import Habit
from habit.paginators import HabitPagination
from users.permissions import IsOwner
from habit.serializers import HabitSerializer


class HabitListAPIView(ListAPIView):
    """Generic-класс для вывода списка опубликованных привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_published=True)
    pagination_class = HabitPagination


class HabitRetrieveAPIView(RetrieveAPIView):
    """Generic-класс для просмотра привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitPersonAPIView(ListAPIView):
    """Generic-класс для вывода списка привычек, принадлежащих пользователю"""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = (IsOwner,)

    def get_queryset(self):
        queryset = Habit.objects.filter(owner=self.request.user)
        return queryset


class HabitCreateAPIView(CreateAPIView):
    """Generic-класс для создания привычки, принадлежащей пользователю"""

    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateAPIView(UpdateAPIView):
    """Generic-класс для редактирования привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDeleteAPIView(DestroyAPIView):
    """Generic-класс для удаления привычки"""

    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
