from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="ivklepova2307@gmail.com",
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
        )
        user.set_password("123qwe456rty")
        user.save()
