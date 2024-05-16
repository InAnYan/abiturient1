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
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        required=False,
        label=_("Faculty"),
    )

    speciality = forms.ChoiceField(
        choices=lambda: make_speciality_choices(),
        required=False,
        label=_("Speciality"),
    )

    educational_program_name = forms.CharField(
        required=False,
        label=_("Name of educational program"),
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

    """
    def find_university_offers(self) -> Iterable[UniversityOffer]:
        q = UniversityOffer.objects.filter(
            basis=self.cleaned_data["basis"],
            level=self.cleaned_data["level"],
            study_form=self.cleaned_data["study_form"],
            offer_type=self.cleaned_data["offer_type"],
        )

        if faculty := self.cleaned_data["faculty"]:
            q = q.filter(faculty=faculty)

        if speciality := self.cleaned_data["speciality"]:
            q = q.filter(speciality=speciality)

        if educational_program_name := self.cleaned_data["educational_program_name"]:

            def rank(offer: UniversityOffer) -> int:
                from thefuzz import fuzz

                return fuzz.partial_ratio(
                    educational_program_name, offer.educational_program.name
                )

            q = sorted(q, key=rank, reverse=True)

        return q
    """
