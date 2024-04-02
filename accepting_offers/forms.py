from django import forms

from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer


class AcceptedOfferForm(forms.ModelForm):
    class Meta:
        model = AcceptedOffer
        exclude = ()


AcceptedOfferFormSet = forms.inlineformset_factory(
    Abiturient, AcceptedOffer, fields="__all__", min_num=1, extra=0, can_delete=False
)
