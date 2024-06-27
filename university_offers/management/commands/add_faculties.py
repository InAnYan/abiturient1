from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from university_offers.models import Faculty


faculties_data = [
    {
        "full_name": "Факультет української й іноземної філології та мистецтвознавства",
        "abbreviation": "ФУІФМ",
        "cipher": 1,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Факультет суспільних наук і міжнародних відносин",
        "abbreviation": "ФСНМВ",
        "cipher": 2,
        "email": "ruslanpopov1512@gmail.com",
    },
    {"full_name": "Історичний факультет", "abbreviation": "ІФ", "cipher": 3},
    {
        "full_name": "Факультет психології та спеціальної освіти",
        "abbreviation": "ФПСО",
        "cipher": 4,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Факультет прикладної математики",
        "abbreviation": "ФПМ",
        "cipher": 5,
        "email": "ruslanpopov1512@gmail.com",
    },
    {"full_name": "Факультет економіки", "abbreviation": "ФЕ", "cipher": 6},
    {
        "full_name": "Факультет систем і засобів масової комунікації",
        "abbreviation": "ФСЗМК",
        "cipher": 7,
        "email": "ruslanpopov1512@gmail.com",
    },
    {"full_name": "Юридичний факультет", "abbreviation": "ЮФ", "cipher": 8},
    {
        "full_name": "Факультет фізики, електроніки та комп'ютерних систем",
        "abbreviation": "ФФЕКС",
        "cipher": 9,
        "email": "ruslanpopov1512@gmail.com",
    },
    {"full_name": "Фізико-технічний факультет", "abbreviation": "ФТФ", "cipher": 10},
    {
        "full_name": "Механіко-математичний факультет",
        "abbreviation": "ММФ",
        "cipher": 11,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Хімічний факультет",
        "abbreviation": "ХФ",
        "cipher": 12,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Біолого-екологічний факультет",
        "abbreviation": "БЕФ",
        "cipher": 13,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Факультет медичних технологій діагностики та реабілітації",
        "abbreviation": "ФМТДР",
        "cipher": 14,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Навчально-методичний центр заочної та вечірньої форм навчання",
        "abbreviation": "НМЦЗВФН",
        "cipher": 0000,
        "email": "ruslanpopov1512@gmail.com",
    },
    {
        "full_name": "Навчально-методичний центр післядипломної освіти",
        "abbreviation": "НМЦПДО",
        "cipher": 0000,
        "email": "ruslanpopov1512@gmail.com",
    },
]


class Command(BaseCommand):
    help = _("add DNU faculties (2024)")

    def handle(self, *args, **options):
        for faculty_data in faculties_data:
            del faculty_data["cipher"]
            Faculty(**faculty_data).save()
