from django import forms

from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer


class DateInput(forms.DateInput):
    input_type = "date"


class AbiturientForm(forms.ModelForm):
    class Meta:
        model = Abiturient
        exclude = ()
        widgets = {"birth_date": DateInput()}


class AcceptedOfferForm(forms.ModelForm):
    class Meta:
        model = AcceptedOffer
        exclude = ()


AcceptedOfferFormSet = forms.inlineformset_factory(
    Abiturient, AcceptedOffer, fields="__all__", min_num=1, extra=0, can_delete=False
)
