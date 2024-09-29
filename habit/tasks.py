from datetime import timedelta
from django.utils import timezone
from celery import shared_task

from habit.models import Habit
from habit.services import send_tg_message


@shared_task
def reminder():
    """Отложенная задача Celery для напоминания о выполнении привычки"""

    now = timezone.now().today()
    habits = Habit.objects.filter(time__gte=now.time())
    for habit in habits:
        owner = habit.owner.chat_id
        date = habit.date + timedelta(days=habit.periodicity)
        if date == now.date():
            if owner:
                text = (
                    f"Привет, друг, наступило время для {habit.action}"
                    f" в {habit.place}."
                    f"Тебе потребуется на это всего {habit.complete_time} минут."
                )
                send_tg_message(text, owner)
