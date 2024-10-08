# Generated by Django 4.2.2 on 2024-09-29 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habit", "0003_alter_habit_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="complete_time",
            field=models.TimeField(
                blank=True, null=True, verbose_name="Время на выполнение"
            ),
        ),
        migrations.AlterField(
            model_name="habit",
            name="date",
            field=models.DateField(default="2024-01-01", verbose_name="дата привычки"),
        ),
    ]
