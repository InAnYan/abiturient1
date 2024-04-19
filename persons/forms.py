from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from persons.models import Person

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class DateInput(forms.DateInput):
    input_type = "date"


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ["parent"]
        widgets = {"passport_when_given": DateInput()}


class AbiturientForm(PersonForm):
    has_18_years = forms.BooleanField(
        label=capitalize_lazy(_("persons.has_18_years")), required=False
    )
