from datetime import date
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from university_offers.models import EducationalProgram, Speciality, UniversityOffer


class Command(BaseCommand):
    help = _("university_offers.add_offers.help")

    def handle(self, *args, **options):
        for speciality in Speciality.objects.all():
            for type, _ in UniversityOffer.Type.choices:
                for study_form, _ in UniversityOffer.StudyForm.choices:
                    for level, _ in UniversityOffer.Level.choices:
                        UniversityOffer.objects.create(
                            study_begin=date.today(),
                            study_duration=12,
                            educational_program=EducationalProgram.objects.get(
                                name=speciality.name
                            ),
                            type=type,
                            study_form=study_form,
                            ects=60,
                            level=level,
                        )
