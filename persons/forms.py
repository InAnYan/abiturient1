from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from persons.models import Passport, Person

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class DateInput(forms.DateInput):
    input_type = "date"


class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["living_address"].widget.attrs = {"rows": 3}

    class Meta:
        model = Person
        exclude = ["parent", "passport"]
        error_messages = {"email": {"invalid": _("persons.form.invalid_email")}}


class PassportForm(forms.ModelForm):
    class Meta:
        model = Passport
        exclude = []
        widgets = {"when_given": DateInput()}


class AbiturientForm(PersonForm):
    has_18_years = forms.BooleanField(
        label=capitalize_lazy(_("persons.has_18_years")), required=False
    )
