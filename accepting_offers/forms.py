from typing import Any
from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer
from university_offers.models import Faculty, Speciality, UniversityOffer

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class AcceptedOfferForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        Faculty.objects.all(), label=capitalize_lazy(_("faculty"))
    )

    speciality = forms.CharField(
        widget=forms.Select(choices=[]), label=capitalize_lazy(_("speciality"))
    )

    study_form = forms.CharField(
        widget=forms.Select(choices=[]),
        label=capitalize_lazy(_("university_offer.study_form")),
    )

    type = forms.CharField(
        widget=forms.Select(choices=[]),
        label=capitalize_lazy(_("university_offer.type")),
    )

    # Dummy field
    info_div = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=capitalize_lazy(_("accepted_offers.info_about_offer")),
    )

    def clean(self) -> dict[str, Any]:
        self.construct_university_offer()
        return super().clean()

    def set_abiturient(self, abiturient: Abiturient):
        self.instance.abiturient = abiturient

    def construct_university_offer(self):
        if (
            "speciality" in self.cleaned_data
            and "study_form" in self.cleaned_data
            and "type" in self.cleaned_data
        ):
            self.instance.offer = UniversityOffer.objects.filter(
                speciality__id=self.cleaned_data["speciality"],
                study_form=self.cleaned_data["study_form"],
                type=self.cleaned_data["type"],
            ).get()

    class Meta:
        model = AcceptedOffer
        exclude = ("offer", "abiturient")

    field_order = [
        "faculty",
        "speciality",
        "study_form",
        "type",
        "info_div",
        "payment_type",
        "payment_frequency",
        "accepted_year",
    ]
