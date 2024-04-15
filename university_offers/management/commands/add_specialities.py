from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from university_offers.models import Faculty, Speciality

specialities_data = [
    ("ІФ", {"code": "014.003", "name": "Середня освіта (Історія)"}),
    ("ІФ", {"code": "032", "name": "Історія та археологія"}),
    ("ММФ", {"code": "144", "name": "Теплоенергетика"}),
    ("ММФ", {"code": "112", "name": "Статистика"}),
    ("ММФ", {"code": "111", "name": "Математика"}),
    ("ФФЕКС", {"code": "105", "name": "Прикладна фізика та наноматеріали"}),
    ("ФФЕКС", {"code": "104", "name": "Фізика та астрономія"}),
    ("ФФЕКС", {"code": "014.008", "name": "Середня освіта (Фізика)"}),
    ("ФФЕКС", {"code": "123", "name": "Комп’ютерна інженерія"}),
]


class Command(BaseCommand):
    help = _("university_offers.add_specialities.help")

    def handle(self, *args, **options):
        for faculty_abbrev, speciality_info in specialities_data:
            faculty = Faculty.objects.get(abbreviation=faculty_abbrev)
            code_list = speciality_info["code"].split(".")
            code = code_list[0]
            specialization = code_list[1] if len(code_list) > 1 else None
            educational_program_name = speciality_info["name"]
            end_of_accreditation = None

            Speciality(
                faculty=faculty,
                name=speciality_info["name"],
                code=code,
                specialization=specialization,
                end_of_accreditation=end_of_accreditation,
                educational_program_name=educational_program_name,
            ).save()
