from datetime import date
from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from abiturients.models import (
    Abiturient,
)
from accepting_offers.models import AcceptedOffer
from university_offers.models import UniversityOffer

from django.core.validators import MaxValueValidator

from abiturient1.validators import ukrainian_validator


class AbiturientBasicInformationForm(forms.Form):
    last_name = forms.CharField(
        max_length=255, label=_("Last name"), validators=[ukrainian_validator]
    )

    first_name = forms.CharField(
        max_length=255, label=_("First name"), validators=[ukrainian_validator]
    )

    patronymic = forms.CharField(
        max_length=255,
        label=_("Patronymic"),
        required=False,
        validators=[ukrainian_validator],
    )

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
        label=_("Date of birth"),
        widget=forms.TextInput(attrs={"type": "date"}),
        validators=[
            MaxValueValidator(date.today, _("Date of birth cannot be in the future"))
        ],
    )

    nationality = forms.CharField(
        max_length=255, label=_("Nationality"), required=False
    )

    gender = forms.ChoiceField(
        label=_("Gender"),
        choices=Abiturient.Gender.choices,
    )

    foreign_language = forms.CharField(
        max_length=255,
        label=_("What foreign language do you know?"),
        required=False,
        help_text=_("Use nominative case"),
    )


class AbiturientEducationForm(forms.Form):
    education_institution = forms.CharField(
        max_length=255, label=_("Full name of educational institution that you ended")
    )
    education_place = forms.CharField(label=_("Education place"))
    education_end = forms.DateField(
        label=_("Education end date"),
        widget=forms.TextInput(attrs={"type": "date"}),
        validators=[
            MaxValueValidator(
                date.today, _("Education end date cannot be in the future")
            )
        ],
    )

    hidden_birth_date = forms.DateField(required=False)

    def clean_education_end(self) -> date:
        res = self.cleaned_data["education_end"]

        if res < self.initial["hidden_birth_date"]:
            raise forms.ValidationError(
                _("Education end date cannot be before birth date")
            )

        return res


class AbiturientMiscInformationForm(forms.Form):
    work = forms.CharField(
        label=_("Work experience"),
        required=False,
        help_text=_(
            "You can leave this field empty. You can tell us were and how you worked before entering out university"
        ),
    )
    martial_status = forms.ChoiceField(
        label=_("Martial status"),
        choices=Abiturient.MartialStatus.choices,
    )
    living_address = forms.CharField(label=_("Living address"))
    registered_address = forms.CharField(label=_("Registered address"))


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

        return cleaned_data

    @property
    def get_payment_frequency_label(self) -> str:
        return AcceptedOffer.PaymentFrequency(self.payment_frequency).label

    class Meta:
        model = AcceptedOffer
        exclude = ("offer", "abiturient")


class AbiturientParentsForm(forms.Form):
    father_last_name = forms.CharField(
        max_length=255, label=_("Father last name"), required=False
    )
    father_first_name = forms.CharField(
        max_length=255, label=_("Father first name"), required=False
    )
    father_patronymic = forms.CharField(
        max_length=255, label=_("Father patronymic"), required=False
    )

    father_phone = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        label=_("Father phone number"),
        required=False,
    )

    mother_last_name = forms.CharField(
        max_length=255, label=_("Mother last name"), required=False
    )
    mother_first_name = forms.CharField(
        max_length=255, label=_("Mother first name"), required=False
    )
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
        required=False,
    )


class AbiturientSensitiveInformationForm(forms.Form):
    hidden_birth_date = forms.DateField(required=False)

    passport_serie = forms.CharField(
        label=_("Passport serie"),
        max_length=2,
        required=False,
        help_text=_(
            "If you have an ID card, leave this field empty. If you have a book-passport, then fill this field."
        ),
        validators=[ukrainian_validator],
    )

    passport_number = forms.IntegerField(
        label=_("Passport number"),
        validators=[MaxValueValidator(999999999)],
        required=False,
    )

    passport_authority = forms.CharField(
        label=_("Authority"),
        help_text=_(
            "If you have an ID card, this field should contain numbers. If you have a book-passport, this field should contain a text (description)."
        ),
        required=False,
        validators=[
            RegexValidator(
                r"^[А-Яа-яЄєІіЇїҐґ\'’`0-9 ]*$",
                _("Only Ukrainian letters or numbers allowed"),
            )
        ],
    )

    passport_issue_date = forms.DateField(
        label=_("Date of issue"),
        validators=[
            MaxValueValidator(
                limit_value=date.today,
                message=_("Passport issue date cannot be in the future"),
            )
        ],
        widget=forms.TextInput(attrs={"type": "date"}),
        required=False,
    )

    def clean_passport_issue_date(self) -> date | None:
        res = self.cleaned_data["passport_issue_date"]

        if res:
            if res < self.initial["hidden_birth_date"]:
                raise forms.ValidationError(
                    _("Passport issue date cannot be before birth date")
                )

        return res

    passport_expiry_date = forms.DateField(
        label=_("Date of expiry"),
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
        help_text=_("Only for ID-card"),
    )

    def clean_passport_expiry_date(self) -> date | None:
        if (
            "passport_expiry_date" not in self.cleaned_data
            or not self.cleaned_data["passport_expiry_date"]
            or "passport_issue_date" not in self.cleaned_data
            or not self.cleaned_data["passport_issue_date"]
        ):
            return None

        res = self.cleaned_data["passport_expiry_date"]

        if res < self.cleaned_data["passport_issue_date"]:
            raise forms.ValidationError(
                _("Passport expiry date cannot be before passport issue date")
            )

        return res

    rntrc = forms.IntegerField(
        label=_("RNTRC"),
        validators=[MaxValueValidator(999999999999)],
        help_text=_(
            "Registration number of the taxpayer's account card (a local equivalent of the taxpayer's identification number)"
        ),
        required=False,
    )


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

    email = forms.EmailField(label=_("Email"))

    living_address = forms.CharField(label=_("Living address"))

    passport_serie = forms.CharField(
        max_length=2,
        label=_("Passport serie"),
        required=False,
        help_text=_(
            "If you have an ID card, leave this field empty. If you have a book-passport, then fill this field."
        ),
    )

    passport_number = forms.IntegerField(
        label=_("Passport number"),
        validators=[MaxValueValidator(999999999)],
        required=False,
    )

    passport_authority = forms.CharField(
        label=_("Authority"),
        required=False,
        help_text=_(
            "If you have an ID card, this field should contain numbers. If you have a book-passport, this field should contain a text (description)."
        ),
    )

    passport_issue_date = forms.DateField(
        label=_("Date of issue"),
        validators=[
            MaxValueValidator(
                limit_value=date.today,
                message=_("Passport issue date cannot be in the future"),
            )
        ],
        widget=forms.TextInput(attrs={"type": "date"}),
        required=False,
    )

    passport_expiry_date = forms.DateField(
        label=_("Date of expiry"),
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
        help_text=_("Only for ID-card"),
    )

    def clean_passport_expiry_date(self) -> date | None:
        if (
            "passport_expiry_date" not in self.cleaned_data
            or not self.cleaned_data["passport_expiry_date"]
            or "passport_issue_date" not in self.cleaned_data
            or not self.cleaned_data["passport_issue_date"]
        ):
            return None

        res = self.cleaned_data["passport_expiry_date"]

        if res < self.cleaned_data["passport_issue_date"]:
            raise forms.ValidationError(
                _("Passport expiry date cannot be before passport issue date")
            )

        return res

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
