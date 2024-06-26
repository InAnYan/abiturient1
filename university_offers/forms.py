from logging import captureWarnings
from typing import Iterable
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from university_offers.models import (
    EducationalLevel,
    Faculty,
    Speciality,
    UniversityOffer,
)


capitalize_lazy = lazy(lambda s: s.capitalize(), str)


def make_speciality_choices():
    # Shitty algroithm.
    choices = [
        (speciality.id, speciality.code_and_name)
        for speciality in Speciality.objects.all()
    ]
    unique_choices = []
    names = []
    for id, name in choices:
        if name in names:
            continue
        names.append(name)
        unique_choices.append((id, name))
    return sorted(unique_choices, key=lambda t: t[1])


class UniversityOfferSearchForm(forms.Form):
    speciality = forms.ChoiceField(
        choices=lambda: make_speciality_choices(),
        required=False,
        label=_("Speciality"),
    )
    offer_type = forms.ChoiceField(
        choices=UniversityOffer.Type.choices,
        label=_("Offer type"),
        help_text=_("Budget or contract"),
    )

    study_form = forms.ChoiceField(
        choices=UniversityOffer.StudyForm.choices,
        label=_("Study form"),
    )

    level = forms.ChoiceField(
        choices=EducationalLevel.choices,
        label=_("Educational level"),
    )

    basis = forms.ChoiceField(
        choices=UniversityOffer.Basis.choices,
        label=_("Basis"),
    )

    # It will be a hidden field, so we can't leave it required because the error message won't be shown.
    result_offer = forms.ModelChoiceField(
        queryset=UniversityOffer.objects.all(),
        required=False,
        label=_("Result offer (you are not supposed to see this)"),
    )

    def clean_result_offer(self):
        if not self.cleaned_data["result_offer"]:
            self.add_error(None, _("Please, choose an offer"))
        return self.cleaned_data["result_offer"]
