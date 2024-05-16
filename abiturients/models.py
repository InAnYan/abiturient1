from datetime import date
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator


TELEPHONE_HELP = "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"


class ContactInformation(models.Model):
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))
    first_name = models.CharField(max_length=255, verbose_name=_("First name"))
    patronymic = models.CharField(max_length=255, verbose_name=_("Patronymic"))

    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(TELEPHONE_HELP),
        max_length=13,
    )

    class Meta:
        verbose_name = _("Contact information")
        verbose_name_plural = _("Contact informations")


PASSPORT_SERIE_HELP = "If you have an ID card, leave this field empty. If you have a book-passport, then fill this field."
PASSPORT_AUTHORITY_HELP = "If you have an ID card, this field should contain numbers. If you have a book-passport, this field should contain a text (description)."


class SensitiveInformation(models.Model):
    serie = models.CharField(
        verbose_name=_("Passport serie"),
        max_length=2,
        null=True,
        blank=True,
        help_text=_(PASSPORT_SERIE_HELP),
    )

    number = models.IntegerField(
        verbose_name=_("Passport number"),
        validators=[MaxValueValidator(999999999)],
        null=True,
        blank=True,
    )

    authority = models.TextField(
        verbose_name=_("Authority"),
        help_text=_(PASSPORT_AUTHORITY_HELP),
        null=True,
        blank=True,
    )

    issue_date = models.DateField(
        verbose_name=_("Date of issue"),
        validators=[MaxValueValidator(limit_value=date.today)],
        null=True,
        blank=True,
    )

    rntrc = models.IntegerField(
        verbose_name=_("RNTRC"),
        validators=[MaxValueValidator(999999999999)],
        help_text=_(
            "Registration number of the taxpayer's account card (a local equivalent of the taxpayer's identification number)"
        ),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Sensitive information")
        verbose_name_plural = _("Sensitive informations")


class Abiturient(models.Model):
    contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Contact information"),
    )

    birth_date = models.DateField(verbose_name=_("Date of birth"))
    birth_country = models.CharField(max_length=255, verbose_name=_("Birth country"))
    birth_town = models.CharField(max_length=255, verbose_name=_("Birth town"))

    nationality = models.CharField(
        max_length=255, verbose_name=_("Nationality"), blank=True, null=True
    )

    education_institution = models.CharField(
        max_length=255, verbose_name=_("Educational institution")
    )

    education_place = models.CharField(
        max_length=255, verbose_name=_("Education place")
    )

    education_end = models.DateField(verbose_name=_("Education end date"))

    job = models.TextField(verbose_name=_("Job"), blank=True, null=True)

    class MartialStatus(models.IntegerChoices):
        SINGLE = 1, _("Single")
        MARRIED = 2, _("Married")

    marital_status = models.IntegerField(
        verbose_name=_("Marital status"), choices=MartialStatus.choices
    )

    foreign_language = models.CharField(
        max_length=255, verbose_name=_("Foreign language"), blank=True, null=True
    )

    email = models.EmailField(verbose_name=_("Email"))

    home_address = models.TextField(verbose_name=_("Home address"))
    living_address = models.TextField(verbose_name=_("Living address"))

    mother_contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Mother's contact information"),
        blank=True,
        null=True,
    )

    father_contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Father's contact information"),
        blank=True,
        null=True,
    )

    sensitive_information = models.OneToOneField(
        SensitiveInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Sensitive information"),
        blank=True,
        null=True,
    )
