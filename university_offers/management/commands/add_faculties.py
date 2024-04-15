from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from university_offers.models import Faculty


faculties_data = [
    {
        "full_name": "Факультет української й іноземної філології та мистецтвознавства",
        "abbreviation": "ФУІФМ",
        "cipher": 1,
    },
    {
        "full_name": "Факультет суспільних наук і міжнародних відносин",
        "abbreviation": "ФСНМВ",
        "cipher": 2,
    },
    {"full_name": "Історичний факультет", "abbreviation": "ІФ", "cipher": 3},
    {
        "full_name": "Факультет психології та спеціальної освіти",
        "abbreviation": "ФПСО",
        "cipher": 4,
    },
    {
        "full_name": "Факультет прикладної математики",
        "abbreviation": "ФПМ",
        "cipher": 5,
    },
    {"full_name": "Факультет економіки", "abbreviation": "ФЕ", "cipher": 6},
    {
        "full_name": "Факультет систем і засобів масової комунікації",
        "abbreviation": "ФСЗМК",
        "cipher": 7,
    },
    {"full_name": "Юридичний факультет", "abbreviation": "ЮФ", "cipher": 8},
    {
        "full_name": "Факультет фізики, електроніки та комп'ютерних систем",
        "abbreviation": "ФФЕКС",
        "cipher": 9,
    },
    {"full_name": "Фізико-технічний факультет", "abbreviation": "ФТФ", "cipher": 10},
    {
        "full_name": "Механіко-математичний факультет",
        "abbreviation": "ММФ",
        "cipher": 11,
    },
    {"full_name": "Хімічний факультет", "abbreviation": "ХФ", "cipher": 12},
    {"full_name": "Біолого-екологічний факультет", "abbreviation": "БЕФ", "cipher": 13},
    {
        "full_name": "Факультет медичних технологій діагностики та реабілітації",
        "abbreviation": "ФМТДР",
        "cipher": 14,
    },
]


class Command(BaseCommand):
    help = _("university_offers.add_faculties.help")

    def handle(self, *args, **options):
        for faculty_data in faculties_data:
            Faculty(**faculty_data).save()
