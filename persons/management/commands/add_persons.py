from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import random
from datetime import datetime, timedelta

from university_offers.models import UniversityOffer

ukrainian_first_names = [
    "Андрій",
    "Олександр",
    "Сергій",
    "Іван",
    "Михайло",
    "Олена",
    "Тетяна",
    "Наталія",
    "Оксана",
    "Ірина",
]

ukrainian_last_names = [
    "Петренко",
    "Іваненко",
    "Коваленко",
    "Бондаренко",
    "Шевченко",
    "Мельник",
    "Коваль",
    "Бойко",
    "Кравченко",
    "Ковалев",
]

ukrainian_patronymics = [
    "Андрійович",
    "Олександрович",
    "Сергійович",
    "Іванович",
    "Михайлович",
    "Олексіївна",
    "Тимофіївна",
    "Максимівна",
    "Дмитрівна",
    "Петрівна",
]


def generate_phone_number():
    return int(f"380{random.randint(50, 99)}{random.randint(1000000, 9999999)}")


def generate_email(first_name, last_name):
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "example.com"])
    return f"{first_name.lower()}.{last_name.lower()}@{domain}"


def generate_living_address():
    streets = [
        "вулиця Шевченка",
        "проспект Леніна",
        "вулиця Пушкіна",
        "вулиця Гоголя",
        "проспект Сталіна",
    ]
    cities = ["Київ", "Харків", "Львів", "Одеса", "Дніпро"]
    return f"{random.choice(streets)}, {random.randint(1, 100)}, м. {random.choice(cities)}"


def generate_passport_number():
    return int("".join(str(random.randint(0, 9)) for _ in range(8)))


def generate_passport_who_give():
    return random.randint(1000, 9999)


def generate_passport_when_given():
    start_date = datetime(2000, 1, 1)
    end_date = datetime.now()
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def generate_inn():
    return int("".join(str(random.randint(0, 9)) for _ in range(12)))


mockup_data = []


from persons.models import Passport, Person


class Command(BaseCommand):
    help = _("persons.add_persons.help")

    def handle(self, *args, **options):
        for i in range(UniversityOffer.objects.all().count()):
            first_name = random.choice(ukrainian_first_names)
            last_name = random.choice(ukrainian_last_names)
            patronymic = random.choice(ukrainian_patronymics)
            phone = generate_phone_number()
            email = generate_email(first_name, last_name)
            living_address = generate_living_address()
            passport_number = generate_passport_number()
            passport_who_give = generate_passport_who_give()
            passport_when_given = generate_passport_when_given()
            inn = generate_inn()

            passport = Passport.objects.create(
                number=passport_number,
                who_give=passport_who_give,
                when_given=passport_when_given,
                inn=inn,
            )

            Person.objects.create(
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                phone=phone,
                email=email,
                living_address=living_address,
                passport=passport,
            )
