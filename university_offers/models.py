from tabnanny import verbose
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


# Факультет.
class Faculty(models.Model):
    full_name = models.CharField(
        max_length=255, unique=True, verbose_name=_("generic.full_name")
    )
    abbreviation = models.CharField(
        max_length=255, unique=True, verbose_name=_("generic.abbreviation")
    )
    cipher = models.IntegerField(
        validators=[MinValueValidator(1)], unique=True, verbose_name=_("generic.cipher")
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("faculty")
        verbose_name_plural = _("faculty.plural")


# Спеціальність.
class Speciality(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("generic.name"))
    code = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("generic.code")
    )
    specialization = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name=_("speciality.specialization"),
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, verbose_name=_("faculty")
    )
    end_of_accreditation = models.DateField(
        null=True, blank=True, verbose_name=_("speciality.end_of_accreditation")
    )  # TODO: ???
    educational_program_name = models.CharField(
        max_length=255, verbose_name=_("speciality.educational_program_name")
    )

    def __str__(self) -> str:
        code = str(self.code).zfill(3)
        if self.specialization:
            code += "." + str(self.specialization).zfill(3)

        return self.faculty.abbreviation + " - " + code + " " + self.name

    class Meta:
        verbose_name = _("speciality")
        verbose_name_plural = _("speciality.plural")


# Конкурсна пропозиція.
class UniversityOffer(models.Model):
    class Type(models.IntegerChoices):
        BUDGET = 1, _("university_offer.type.budget")
        CONTRACT = 2, _("university_offer.type.contract")

    class StudyForm(models.IntegerChoices):
        DAY = 1, _("university_offer.study_form.day")
        OVER_DISTANCE = 2, _("university_offer.study_form.over_distance")
        EVENING = 3, _("university_offer.study_form.evening")

    study_begin = models.DateField(verbose_name=_("university_offer.study_begin"))
    study_duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("university_offer.study_duration"),
    )
    speciality = models.ForeignKey(
        Speciality, on_delete=models.PROTECT, verbose_name=_("speciality")
    )
    type = models.PositiveIntegerField(
        choices=Type.choices, verbose_name=_("university_offer.type")
    )
    study_form = models.PositiveIntegerField(
        choices=StudyForm.choices, verbose_name=_("university_offer.study_form")
    )
    ects = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("university_offer.ects")
    )

    def __str__(self) -> str:
        return (
            str(self.speciality)
            + " - "
            + self.StudyForm(self.study_form).label
            + " - "
            + self.Type(self.type).label
        )

    class Meta:
        verbose_name = _("university_offer")
        verbose_name_plural = _("university_offer.plural")
