from django import forms
from django.urls import reverse

from abiturients.models import Abiturient, FamilyMember, Phone


class DateInput(forms.DateInput):
    input_type = "date"


class AbiturientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbiturientForm, self).__init__(*args, **kwargs)
        autocomplete_fields = [
            "birth_country",
            "birth_town",
            "nationality",
            "foreign_language",
        ]
        for field_name in autocomplete_fields:
            self.fields[field_name].widget.attrs["class"] = "autocomplete"
            self.fields[field_name].widget.attrs["data-url"] = reverse(
                "ajax_" + field_name
            )

    class Meta:
        model = Abiturient
        exclude = ()
        widgets = {
            "birth_date": DateInput(),
        }


FamilyMemberFormSet = forms.inlineformset_factory(
    Abiturient, FamilyMember, fields="__all__", min_num=1, extra=0, can_delete=False
)

PhoneFormSet = forms.inlineformset_factory(
    Abiturient, Phone, fields="__all__", min_num=1, extra=0, can_delete=False
)
