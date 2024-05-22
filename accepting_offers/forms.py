from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from abiturients.models import ContactInformation, SensitiveInformation
from accepting_offers.models import AcceptedOffer
from university_offers.models import UniversityOffer


class AbiturientBasicInformationForm(forms.Form):
    last_name = forms.CharField(max_length=255, label=_("Last name"))
    first_name = forms.CharField(max_length=255, label=_("First name"))
    patronymic = forms.CharField(max_length=255, label=_("Patronymic"), required=False)

    phone_number = forms.CharField(
        label=_("Phone number"),
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        max_length=13,
    )

    email = forms.EmailField(label=_("Email"))


class AbiturientBirthInformationForm(forms.Form):
    birth_country = forms.CharField(max_length=255, label=_("Birth country"))
    birth_town = forms.CharField(max_length=255, label=_("Birth town"))

    birth_date = forms.DateField(label=_("Date of birth"))

    nationality = forms.CharField(
        max_length=255, label=_("Nationality"), required=False
    )

    foreign_language = forms.CharField(
        max_length=255, label=_("What foreign language do you know?"), required=False
    )


class AbiturientEducationForm(forms.Form):
    education_institution = forms.CharField(
        max_length=255, label=_("Educational institution")
    )
    education_place = forms.TextInput(label=_("Education place"))
    education_end = forms.DateField(label=_("Education end date"))


class AbiturientMiscInformationForm(forms.Form):
    work = forms.CharField(label=_("Work"), required=False)
    martial_status = forms.ChoiceField(
        label=_("Martial status"),
        choices=AcceptedOffer.MartialStatus.choices,
    )
    living_address = forms.CharField(label=_("Living address"))
    registered_address = forms.CharField(label=_("Registered address"))


# University offer search form.


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


class AbiturientParentsForm(forms.Form):
    father_last_name = forms.CharField(max_length=255, label=_("Father last name"))
    father_first_name = forms.CharField(max_length=255, label=_("Father first name"))
    father_patronymic = forms.CharField(
        max_length=255, label=_("Father patronymic"), required=False
    )

    # NOO! Code duplication...
    father_phone = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        label=_("Father phone number"),
    )

    mother_last_name = forms.CharField(max_length=255, label=_("Mother last name"))
    mother_first_name = forms.CharField(max_length=255, label=_("Mother first name"))
    mother_patronymic = forms.CharField(
        max_length=255, label=_("Mother patronymic"), required=False
    )

    mother_phone = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        label=_("Mother phone number"),
    )


class AbiturientSensitiveInformationForm(forms.ModelForm):
    class Meta:
        model = SensitiveInformation
        exclude = []


class RepresentativeContactForm(forms.ModelForm):
    living_address = forms.CharField(label=_("Living address"))

    class Meta:
        model = ContactInformation
        exclude = []

    field_order = [
        "last_name",
        "first_name",
        "patronymic",
        "phone_number",
        "living_address",
    ]


class RepresentativeSensitiveInformationForm(forms.ModelForm):
    class Meta:
        model = SensitiveInformation
        exclude = []


class EmptyForm(forms.Form):
    pass
