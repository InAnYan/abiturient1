from django import forms

from abiturients.models import Abiturient, FamilyMember, Phone


class DateInput(forms.DateInput):
    input_type = "date"


class AbiturientForm(forms.ModelForm):
    class Meta:
        model = Abiturient
        exclude = ()
        widgets = {"birth_date": DateInput()}


FamilyMemberFormSet = forms.inlineformset_factory(
    Abiturient, FamilyMember, fields="__all__", min_num=1, extra=0, can_delete=False
)

PhoneFormSet = forms.inlineformset_factory(
    Abiturient, Phone, fields="__all__", min_num=1, extra=0, can_delete=False
)
