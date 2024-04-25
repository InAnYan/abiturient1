from datetime import date
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from university_offers.models import EducationalProgram, Speciality, UniversityOffer

offers_data = [
    (
        "Теплоенергетика",
        UniversityOffer.StudyForm.EVENING,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Математика",
        UniversityOffer.StudyForm.OVER_DISTANCE,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Комп’ютерна інженерія",
        UniversityOffer.StudyForm.OVER_DISTANCE,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Середня освіта (Історія)",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Середня освіта (Історія)",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Історія та археологія",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Історія та археологія",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Теплоенергетика",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Теплоенергетика",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Статистика",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Статистика",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Математика",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Математика",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Прикладна фізика та наноматеріали",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Прикладна фізика та наноматеріали",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Фізика та астрономія",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Фізика та астрономія",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Середня освіта (Фізика)",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Середня освіта (Фізика)",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
    (
        "Комп’ютерна інженерія",
        UniversityOffer.StudyForm.OVER_DISTANCE,
        UniversityOffer.Type.CONTRACT,
    ),
    (
        "Комп’ютерна інженерія",
        UniversityOffer.StudyForm.DAY,
        UniversityOffer.Type.BUDGET,
    ),
]


class Command(BaseCommand):
    help = _("university_offers.add_offers.help")

    def handle(self, *args, **options):
        for speciality_name, study_form, type in offers_data:
            UniversityOffer.objects.create(
                study_begin=date.today(),
                study_duration=12,
                educational_program=EducationalProgram.objects.get(
                    name=speciality_name
                ),
                type=type,
                study_form=study_form,
                ects=60,
                level=UniversityOffer.Level.BACHELOR,
            )
