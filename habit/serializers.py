from rest_framework import serializers
from habit.models import Habit
from habit.validators import (
    TimeValidator,
    PeriodicityValidator,
    HabitAwardValidator,
    RelatedHabitValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор модели привычки"""

    class Meta:
        model = Habit
        fields = "__all__"

        validators = [
            HabitAwardValidator(field="award"),
            RelatedHabitValidator(field="related_habit"),
            PeriodicityValidator(periodicity="periodicity"),
            TimeValidator(complete_time="complete_time"),
        ]
