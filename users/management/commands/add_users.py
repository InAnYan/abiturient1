from django.core.management.base import BaseCommand

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from university_offers.models import Faculty
from users.models import User

names = [
    "monika",
    "eleonora",
    "alisa",
    "anzhelika",
    "violetta",
    "veronika",
    "karina",
    "margarita",
    "natali",
    "roza",
    "stella",
    "zlata",
    "snezhana",
    "ulyana",
    "larisa",
    "anastasia",
]


class Command(BaseCommand):
    help = _("Add users for testing (for different faculties of DNU)")

    def handle(self, *args, **options):
        pk_group = Group.objects.get(name="pk")

        for id, faculty in enumerate(Faculty.objects.all()):
            user = User.objects.create_user(
                username=names[id], faculty=faculty, password="12345"
            )

            print("{0: <10} | {1: <10} | {2}".format(names[id], "12345", str(faculty)))

            pk_group.user_set.add(user)
