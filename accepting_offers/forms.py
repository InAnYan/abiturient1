from mimetypes import init
from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from persons.models import Person
from accepting_offers.models import AcceptedOffer
from university_offers.models import Speciality, UniversityOffer

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class AcceptedOfferForm(forms.ModelForm):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        if self.initial["offer"].type == UniversityOffer.Type.CONTRACT:
            if (
                "payment_type" not in cleaned_data
                or cleaned_data["payment_type"] is None
            ):
                self.add_error(
                    None,
                    _("accepting_offers.payment_type_required_for_contract"),
                )
            if (
                "payment_frequency" not in cleaned_data
                or cleaned_data["payment_frequency"] is None
            ):
                self.add_error(
                    None,
                    _("accepting_offers.payment_frequency_required_for_contract"),
                )
        elif self.initial["offer"].type == UniversityOffer.Type.BUDGET:
            if (
                "payment_type" in cleaned_data
                and cleaned_data["payment_type"] is not None
            ):
                self.add_error(
                    None,
                    _("accepting_offers.payment_type_not_required_for_budget"),
                )
            if (
                "payment_frequency" in cleaned_data
                and cleaned_data["payment_frequency"] is not None
            ):
                self.add_error(
                    None,
                    _("accepting_offers.payment_frequency_not_required_for_budget"),
                )
        else:
            raise NotImplementedError()

    class Meta:
        model = AcceptedOffer
        exclude = ("offer", "abiturient")
