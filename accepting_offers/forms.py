from random import choices
from django import forms
from django.urls import reverse, reverse_lazy

from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer
from university_offers.models import Faculty, Speciality, UniversityOffer


class AcceptedOfferForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        Faculty.objects.all(),
        widget=forms.Select(
            attrs={
                "hx-get": reverse_lazy("ajax_specialities"),
                "hx-trigger": "change",
                "hx-target": "next .select",
            }
        ),
    )

    speciality = forms.ModelChoiceField(
        Speciality.objects.all(),
        widget=forms.Select(
            attrs={
                "hx-get": reverse_lazy("ajax_study_forms"),
                "hx-trigger": "change",
                "hx-target": "next .select",
            }
        ),
    )

    study_form = forms.ChoiceField(
        choices=UniversityOffer.StudyForm.choices,
        widget=forms.Select(
            attrs={
                "hx-get": reverse_lazy("ajax_offer_types"),
                "hx-trigger": "change",
                "hx-target": "next .select",
            }
        ),
    )

    type = forms.ChoiceField(choices=UniversityOffer.Type.choices)

    class Meta:
        model = AcceptedOffer
        exclude = ("offer",)

    field_order = [
        "faculty",
        "speciality",
        "study_form",
        "type",
        "payment_type",
        "payment_frequency",
        "accepted_year",
    ]


AcceptedOfferFormSet = forms.inlineformset_factory(
    Abiturient,
    AcceptedOffer,
    AcceptedOfferForm,
    fields="__all__",
    min_num=1,
    extra=0,
    can_delete=False,
)
