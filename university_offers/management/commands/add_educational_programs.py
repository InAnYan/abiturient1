from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from university_offers.models import EducationalProgram, Speciality


class Command(BaseCommand):
    help = _("university_offers.add_educational_programs.help")

    def handle(self, *args, **options):
        for speciality in Speciality.objects.all():
            EducationalProgram.objects.create(
                name=speciality.name,
                speciality=speciality,
                end_of_accreditation=datetime.now(),
            )
