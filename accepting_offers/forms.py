from mimetypes import init
from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from accepting_offers.models import AcceptedOffer
from university_offers.models import Speciality, UniversityOffer

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class AcceptedOfferForm(forms.ModelForm):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        if self.initial["offer"].type == UniversityOffer.Type.CONTRACT:
            if (
                "payment_frequency" not in cleaned_data
                or cleaned_data["payment_frequency"] is None
            ):
                self.add_error(
                    None,
                    _(
                        "Please, set payment frequency because you chose a contract offer"
                    ),
                )
        elif self.initial["offer"].type == UniversityOffer.Type.BUDGET:
            if (
                "payment_frequency" in cleaned_data
                and cleaned_data["payment_frequency"] is not None
            ):
                self.add_error(
                    None,
                    _(
                        "Please, leave the payment frequency blank because you chose a budget offer"
                    ),
                )
        else:
            raise NotImplementedError()

    class Meta:
        model = AcceptedOffer
        exclude = ("offer", "abiturient")


class EmptyForm(forms.Form):
    pass
