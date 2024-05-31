from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator


class AbiturientRepresentative(models.Model):
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

    living_address = models.TextField(verbose_name=_("Living address"))

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

    passport_expiry_date = models.DateField(
        verbose_name=_("Date of expiry"),
        validators=[MinValueValidator(limit_value=date.today)],
        null=True,
        blank=True,
        help_text=_("Only for ID-card"),
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

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}" + (
            f" {self.patronymic}" if self.patronymic else ""
        )

    class Meta:
        verbose_name = _("Abiturient representative")
        verbose_name_plural = _("Abiturient representatives")


class Abiturient(models.Model):
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

    birth_date = models.DateField(
        verbose_name=_("Date of birth"), validators=[MaxValueValidator(date.today)]
    )
    birth_country = models.CharField(max_length=255, verbose_name=_("Birth country"))
    birth_town = models.CharField(max_length=255, verbose_name=_("Birth town"))

    nationality = models.CharField(
        max_length=255, verbose_name=_("Nationality"), blank=True, null=True
    )

    class Gender(models.IntegerChoices):
        MALE = 1, _("Male")
        FEMALE = 2, _("Female")

    gender = models.IntegerField(verbose_name=_("Gender"), choices=Gender.choices)

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

    mother_last_name = models.CharField(
        max_length=255, verbose_name=_("Mother's last name"), blank=True, null=True
    )
    mother_first_name = models.CharField(
        max_length=255, verbose_name=_("Mother's first name"), blank=True, null=True
    )
    mother_patronymic = models.CharField(
        max_length=255, verbose_name=_("Mother's patronymic"), blank=True, null=True
    )

    @property
    def mother_full_name(self) -> str:
        return f"{self.mother_last_name} {self.mother_first_name}" + (
            f" {self.mother_patronymic}" if self.mother_patronymic else ""
        )

    mother_phone_number = models.CharField(
        verbose_name=_("Mother's phone number"),
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        max_length=13,
        blank=True,
        null=True,
    )

    father_last_name = models.CharField(
        max_length=255, verbose_name=_("Father's last name"), blank=True, null=True
    )
    father_first_name = models.CharField(
        max_length=255, verbose_name=_("Father's first name"), blank=True, null=True
    )
    father_patronymic = models.CharField(
        max_length=255, verbose_name=_("Father's patronymic"), blank=True, null=True
    )

    @property
    def father_full_name(self) -> str:
        return f"{self.father_last_name} {self.father_first_name}" + (
            f" {self.father_patronymic}" if self.father_patronymic else ""
        )

    father_phone_number = models.CharField(
        verbose_name=_("Father's phone number"),
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("Wrong phone number format")),
        ],
        help_text=_(
            "Write the phone number in the following form: +380123456789 (start with +, then area code, then the rest of the number)"
        ),
        max_length=13,
        blank=True,
        null=True,
    )

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

    passport_expiry_date = models.DateField(
        verbose_name=_("Date of expiry"),
        validators=[MinValueValidator(limit_value=date.today)],
        null=True,
        blank=True,
        help_text=_("Only for ID-card"),
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
