# Generated by Django 4.2.2 on 2024-09-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="users/", verbose_name="Аватар"
            ),
        ),
    ]
