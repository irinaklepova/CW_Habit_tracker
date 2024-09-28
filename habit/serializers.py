from rest_framework import serializers
from habit.models import Habit
from habit.validators import (
    RelatedHabitOrAwardValidator,
    TimeValidator,
    RelatedHabitIsPleasantValidator,
    PleasantHabitValidator,
    PeriodicityValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор модели привычки"""

    class Meta:
        model = Habit
        fields = "__all__"

        validators = [
            RelatedHabitOrAwardValidator(related_habit="related_habit", award="award"),
            TimeValidator(complete_time="complete_time"),
            RelatedHabitIsPleasantValidator(related_habit="related_habit"),
            PleasantHabitValidator(
                related_habit="related_habit",
                is_pleasant="is_pleasant",
                award="award",
            ),
            PeriodicityValidator(periodicity="periodicity"),
        ]
