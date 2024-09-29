from datetime import time
from rest_framework.serializers import ValidationError


class HabitAwardValidator:
    """
    Валидатор проверяет условия:
    - В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки.
    Можно заполнить только одно из двух полей.
    - У приятной привычки не может быть вознаграждения.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        award = value.get(self.field)
        related_habit = value.get("related_habit")
        is_pleasant = value.get("is_pleasant")
        if award and is_pleasant:
            raise ValidationError("У приятной привычки не может быть вознаграждения")
        elif award and related_habit:
            raise ValidationError(
                "У привычки может быть либо вознаграждение, либо приятная привычка"
            )


class RelatedHabitValidator:
    """
    Валидатор проверяет условия:
    - У приятной привычки не может быть связанной привычки.
    - В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = value.get(self.field)
        is_pleasant = value.get("is_pleasant")
        if related_habit and is_pleasant:
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки."
            )

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")


class TimeValidator:
    """Валидатор проверяет время выполнения (не более 120 секунд)"""

    def __init__(self, complete_time):
        self.complete_time = complete_time

    def __call__(self, value):
        time_to_complete = time(hour=0, minute=2, second=0)
        tmp_complete_time = value.get(self.complete_time)
        if tmp_complete_time is not None:
            if tmp_complete_time > time_to_complete:
                raise ValidationError("Время выполнения не может быть более 2 минут")


class PeriodicityValidator:
    """Валидатор проверяет, что привычку нельзя выполнять реже, чем 1 раз в 7 дней"""

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, value):
        tmp_periodicity = value.get(self.periodicity)
        if not (0 < tmp_periodicity <= 7):
            raise ValidationError(
                "Поле не может быть пустым. Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )
