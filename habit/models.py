from django.db import models
from config.settings import NULLABLE, AUTH_USER_MODEL


class Habit(models.Model):
    """Модель привычки"""

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Обладатель привычки",
    )
    place = models.CharField(max_length=100, **NULLABLE, verbose_name="Место")
    time = models.TimeField(verbose_name="Время привычки")
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1, **NULLABLE, verbose_name="Периодичность привычки в днях"
    )
    award = models.CharField(max_length=255, **NULLABLE, verbose_name="Вознаграждение")
    complete_time = models.DurationField(**NULLABLE, verbose_name="Время на выполнение")
    is_published = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['action']
