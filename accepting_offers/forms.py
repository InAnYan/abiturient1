from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from persons.models import Person
from accepting_offers.models import AcceptedOffer
from university_offers.models import Speciality, UniversityOffer

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class AcceptedOfferForm(forms.ModelForm):
    class Meta:
        model = AcceptedOffer
        exclude = ("offer", "abiturient")
