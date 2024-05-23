from datetime import date
from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from abiturients.models import (
    PASSPORT_AUTHORITY_HELP,
    PASSPORT_SERIE_HELP,
    Abiturient,
    ContactInformation,
    SensitiveInformation,
)
from accepting_offers.models import AcceptedOffer
from university_offers.models import UniversityOffer

from django.core.validators import MaxValueValidator


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

    birth_date = forms.DateField(
        label=_("Date of birth"), widget=forms.TextInput(attrs={"type": "date"})
    )

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
    education_place = forms.CharField(label=_("Education place"))
    education_end = forms.DateField(
        label=_("Education end date"), widget=forms.TextInput(attrs={"type": "date"})
    )


class AbiturientMiscInformationForm(forms.Form):
    work = forms.CharField(label=_("Work"), required=False)
    martial_status = forms.ChoiceField(
        label=_("Martial status"),
        choices=Abiturient.MartialStatus.choices,
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


class RepresentativeForm(forms.Form):
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

    living_address = forms.CharField(label=_("Living address"))

    passport_serie = forms.CharField(
        max_length=2,
        label=_("Passport serie"),
        required=False,
        help_text=_(PASSPORT_SERIE_HELP),
    )

    passport_number = forms.IntegerField(
        label=_("Passport number"),
        validators=[MaxValueValidator(999999999)],
        required=False,
    )

    passport_authority = forms.CharField(
        label=_("Authority"),
        required=False,
        help_text=_(PASSPORT_AUTHORITY_HELP),
    )

    passport_issue_date = forms.DateField(
        label=_("Date of issue"),
        validators=[MaxValueValidator(limit_value=date.today)],
        required=False,
    )

    rntrc = forms.IntegerField(
        label=_("RNTRC"),
        validators=[MaxValueValidator(999999999999)],
        required=False,
        help_text=_(
            "Registration number of the taxpayer's account card (a local equivalent of the taxpayer's identification number)"
        ),
    )


class EmptyForm(forms.Form):
    pass
