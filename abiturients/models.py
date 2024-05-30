from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator


class ContactInformation(models.Model):
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))
    first_name = models.CharField(max_length=255, verbose_name=_("First name"))
    patronymic = models.CharField(
        max_length=255, verbose_name=_("Patronymic"), blank=True, null=True
    )

    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        max_length=13,
    )

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}" + (
            f" {self.patronymic}" if self.patronymic else ""
        )

    def __str__(self) -> str:
        return self.full_name + " - " + self.phone_number

    class Meta:
        verbose_name = _("Contact information")
        verbose_name_plural = _("Contact informations")


class SensitiveInformation(models.Model):
    passport_serie = models.CharField(
        verbose_name=_("Passport serie"),
        max_length=2,
        null=True,
        blank=True,
        help_text=_(
            "If you have an ID card, leave this field empty. If you have a book-passport, then fill this field."
        ),
    )

    passport_number = models.IntegerField(
        verbose_name=_("Passport number"),
        validators=[MaxValueValidator(999999999)],
        null=True,
        blank=True,
    )

    passport_authority = models.TextField(
        verbose_name=_("Authority"),
        help_text=_(
            "If you have an ID card, this field should contain numbers. If you have a book-passport, this field should contain a text (description)."
        ),
        null=True,
        blank=True,
    )

    passport_issue_date = models.DateField(
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


class AbiturientRepresentative(models.Model):
    contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Contact information"),
    )

    living_address = models.TextField(verbose_name=_("Living address"))

    sensitive_information = models.OneToOneField(
        SensitiveInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Sensitive information"),
    )

    class Meta:
        verbose_name = _("Abiturient representative")
        verbose_name_plural = _("Abiturient representatives")


class Abiturient(models.Model):
    contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Contact information"),
        related_name="abiturient",
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

    work = models.TextField(verbose_name=_("Work"), blank=True, null=True)

    class MartialStatus(models.IntegerChoices):
        SINGLE = 1, _("Single")
        MARRIED = 2, _("Married")

    martial_status = models.IntegerField(
        verbose_name=_("Marital status"), choices=MartialStatus.choices
    )

    foreign_language = models.CharField(
        max_length=255, verbose_name=_("Foreign language"), blank=True, null=True
    )

    email = models.EmailField(verbose_name=_("Email"))

    living_address = models.TextField(verbose_name=_("Living address"))
    registered_address = models.TextField(verbose_name=_("Registered address"))

    mother_contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Mother's contact information"),
        blank=True,
        null=True,
        related_name="mother",
    )

    father_contact_information = models.OneToOneField(
        ContactInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Father's contact information"),
        blank=True,
        null=True,
        related_name="father",
    )

    sensitive_information = models.OneToOneField(
        SensitiveInformation,
        on_delete=models.CASCADE,
        verbose_name=_("Sensitive information"),
    )

    representative = models.OneToOneField(
        AbiturientRepresentative,
        on_delete=models.CASCADE,
        verbose_name=_("Representative"),
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.contact_information.full_name

    class Meta:
        verbose_name = _("Abiturient")
        verbose_name_plural = _("Abiturients")
