from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "action",
        "time",
        "date",
        "place",
        "is_pleasant",
        "related_habit",
        "periodicity",
        "complete_time",
        "is_published",
    )
