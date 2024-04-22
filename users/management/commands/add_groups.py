from django.core.management.base import BaseCommand

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = _("users.add_groups.help")

    def handle(self, *args, **options):
        Group.objects.create(name="pk")
