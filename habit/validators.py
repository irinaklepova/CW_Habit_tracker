from datetime import time
from rest_framework.serializers import ValidationError


class RelatedHabitOrAwardValidator:
    """Валидатор проверяет одновременный выбор связанной привычки и указания вознаграждения"""

    def __init__(self, related_habit, award):
        self.related_habit = related_habit
        self.award = award

    def __call__(self, value):
        tmp_related_habit = dict(value).get(self.related_habit)
        tmp_award = dict(value).get(self.award)
        if tmp_related_habit is not None and tmp_award is not None:
            raise ValidationError(
                "Не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки."
            )


class PleasantHabitValidator:
    """Валидатор проверяет отсутствие У приятной привычки вознаграждения или связанной привычки"""

    def __init__(self, related_habit, is_pleasant, award):
        self.related_habit = related_habit
        self.is_pleasant = is_pleasant
        self.award = award

    def __call__(self, value):
        tmp_related_habit = value.get(self.related_habit)
        tmp_is_pleasant = value.get(self.is_pleasant)
        tmp_award = value.get(self.award)
        if tmp_is_pleasant and (tmp_related_habit or tmp_award):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class TimeValidator:
    """Волидатор проверяет время выполнения (не более 120 секунд)"""

    def __init__(self, complete_time):
        self.complete_time = complete_time

    def __call__(self, value):
        time_to_complete = time(hour=0, minute=2, second=0)
        tmp_complete_time = value.get(self.complete_time)
        if tmp_complete_time is not None:
            if tmp_complete_time > time_to_complete:
                raise ValidationError("Время выполнения не может быть более 2 минут")


class RelatedHabitIsPleasantValidator:
    """Валидатор проверяет у связанной привычки признак приятной привычки"""

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, value):
        tmp_related_habit = value.get(self.related_habit)

        if tmp_related_habit:
            if not tmp_related_habit.is_pleasant:
                raise ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки."
                )


class PeriodicityValidator:
    """Валидатор проверяет, что привычку нельзя выполнять реже, чем 1 раз в 7 дней"""

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, value):
        tmp_periodicity = value.get(self.periodicity)
        if tmp_periodicity is None or tmp_periodicity > 7:
            raise ValidationError(
                "Поле не может быть пустым. Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )
