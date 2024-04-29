from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import random

from accepting_offers.models import AcceptedOffer
from persons.models import Person
from university_offers.admin import UniversityOfferResource
from university_offers.models import UniversityOffer

offers_data = []

for i in range(UniversityOffer.objects.all().count()):
    abiturient = i + 1
    offer = i + 1
    offer = UniversityOffer.objects.get(id=offer)
    if offer.type == UniversityOffer.Type.CONTRACT:
        payment_type = random.randint(1, 4)
        payment_frequency = random.randint(1, 4)
    else:
        payment_frequency = None
        payment_type = None
    accepted_year = random.randint(1, 4)

    offers_data.append(
        {
            "abiturient": Person.objects.get(id=abiturient),
            "offer": offer,
            "payment_type": payment_type,
            "payment_frequency": payment_frequency,
            "accepted_year": accepted_year,
        }
    )


class Command(BaseCommand):
    help = _("accepting_offers.add_accepted_offers.help")

    def handle(self, *args, **options):
        for data in offers_data:
            AcceptedOffer.objects.create(**data)
