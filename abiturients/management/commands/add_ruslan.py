import datetime
from typing import Any, Dict
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import json


from abiturient1.settings import BASE_DIR
from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer
from university_offers.models import (
    Accreditation,
    EducationalLevel,
    EducationalProgram,
    Faculty,
    Speciality,
    UniversityOffer,
)


class Command(BaseCommand):
    help = _("Add Popov Ruslan Oleksandrovich to database")

    def handle(self, *args, **options):
        abiturient = Abiturient(
            last_name="Попов",
            first_name="Руслан",
            patronymic="Олександрович",
            phone_number="+380123456789",
            birth_date=datetime.date(2005, 12, 15),
            birth_country="Україна",
            birth_town="Дніпро",
            nationality="українець",
            gender=Abiturient.Gender.MALE,
            education_institution="Слобожанський ліцей Слобожанської селищної ради",
            education_place="смт. Слобожанське, вул. Теплична 1",
            education_end=datetime.date(2023, 5, 31),
            work="",
            martial_status=Abiturient.MartialStatus.SINGLE,
            foreign_language="англійська",
            email="ruslanpopov1512@gmail.com",
            living_address="смт. Слобожанське",
            registered_address="смт. Слобожанське",
            mother_last_name="Іванова",
            mother_first_name="Анна",
            mother_patronymic="Олександрівна",
            mother_phone_number="+380123456789",
            father_last_name="Петров",
            father_first_name="Олександр",
            father_patronymic="Іванович",
            father_phone_number="+380123456789",
            passport_number="1234567890",
            passport_authority="1234",
            passport_issue_date=datetime.date(2000, 5, 31),
            passport_expiry_date=datetime.date(3000, 5, 31),
            rntrc="123123123123",
        )

        abiturient.save()

        offer = UniversityOffer.objects.get(
            level=EducationalLevel.BACHELOR,
            basis=UniversityOffer.Basis.PZSO,
            type=UniversityOffer.Type.BUDGET,
            study_form=UniversityOffer.StudyForm.DAY,
            educational_program__name="Комп'ютерна інженерія",
        )

        accepted_offer = AcceptedOffer(
            abiturient=abiturient,
            offer=offer,
            created_at=datetime.datetime.now(),
            accepted_year=1,
        )

        accepted_offer.save()
