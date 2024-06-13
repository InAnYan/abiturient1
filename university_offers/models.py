from typing import Optional
from django.db import models
from django.core.validators import MinValueValidator
from dateutil.relativedelta import relativedelta
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from abiturient1.settings import UKRAINIAN_DATE_FORMAT


class Faculty(models.Model):
    full_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Full name"),
    )

    abbreviation = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Abbreviation"),
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")


class Speciality(models.Model):
    code = models.IntegerField(verbose_name=_("Code"))

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    specialization_code = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Specialization code"),
    )

    specialization_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Specialization name"),
    )

    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, verbose_name=_("Faculty")
    )

    def __str__(self) -> str:
        return (
            self.faculty.abbreviation
            + " - "
            + self.code_and_name
            + (f"({self.code_and_name_s})" if self.specialization_code else "")
        )

    @property
    def code_and_name(self) -> str:
        return str(self.code).zfill(3) + " " + self.name

    @property
    def code_and_name_s(self) -> str:
        return f"{self.code_with_specialization} {self.specialization_name}"

    @property
    def code_with_specialization(self) -> str:
        code = str(self.code).zfill(3)
        if self.specialization_code:
            code += "." + str(self.specialization_code).zfill(3)

        return code

    def clean(self) -> None:
        super().clean()

        if not (self.specialization_code and self.specialization_name):
            raise ValidationError("Both specialization code and name must be set")

    class Meta:
        verbose_name = _("Speciality")
        verbose_name_plural = _("Specialities")


class EducationalProgram(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    speciality = models.ForeignKey(
        Speciality, on_delete=models.PROTECT, verbose_name=_("Speciality")
    )

    def __str__(self) -> str:
        return f"{self.speciality} - {self.name}"

    class Meta:
        verbose_name = _("Educational program")
        verbose_name_plural = _("Educational programs")


class EducationalLevel(models.IntegerChoices):
    BACHELOR = 1, _("Bachelor")
    MASTER = 2, _("Master")
    PHD = 3, _("PhD")


class Accreditation(models.Model):
    class Type(models.IntegerChoices):
        SPECIALITY = 1, _("Speciality")
        EDUCATIONAL_PROGRAM = 2, _("Educational program")

    educational_program = models.ForeignKey(
        EducationalProgram,
        on_delete=models.PROTECT,
        verbose_name=_("Educational program"),
    )

    level = models.IntegerField(
        choices=EducationalLevel.choices,
        verbose_name=_("Educational level"),
    )

    end_date = models.DateField(verbose_name=_("End of accreditation"))

    number = models.PositiveIntegerField(verbose_name=_("Accreditation number"))

    serie = models.CharField(
        max_length=2, null=True, blank=True, verbose_name=_("Accreditation serie")
    )

    type = models.PositiveIntegerField(
        choices=Type.choices,
        verbose_name=_("Accreditation type"),
    )

    def __str__(self) -> str:
        return f"{self.serie + ' ' if self.serie else ' '}{self.number} - {self.educational_program}"

    @property
    def ukr_sentence(self) -> str:
        work = "Сертифікат про акредитацію"
        work += " "
        match self.type:
            case self.Type.EDUCATIONAL_PROGRAM:
                work += "освітньої програми"
            case self.Type.SPECIALITY:
                work += "спеціальності"
            case _:
                raise Exception("It can't be: " + self.Type(self.type).label)
        work += " "
        if self.serie:
            work += self.serie
            work += " "
        work += str(self.number)
        work += ", "
        work += "дійсний до"
        work += " "
        work += self.end_date.strftime("%d.%m.%Y")
        return work

    class Meta:
        verbose_name = _("Accreditation")
        verbose_name_plural = _("Accreditations")


class UniversityOffer(models.Model):
    class Type(models.IntegerChoices):
        BUDGET = 1, _("Budget")
        CONTRACT = 2, _("Contract")

    class StudyForm(models.IntegerChoices):
        DAY = 1, _("Full-time")
        OVER_DISTANCE = 2, _("Part-time")
        DISTANCE = 3, _("Distance")

    class Basis(models.IntegerChoices):
        PZSO = 1, _("CGSE")
        NRK_5 = 2, _("NFQ5")
        NRK_6_7 = 3, _("NFQ6 or NFQ7")

    study_begin = models.DateField(verbose_name=_("Beginning of study"))

    @property
    def study_begin_str(self) -> str:
        return self.study_begin.strftime(UKRAINIAN_DATE_FORMAT)

    study_duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Study duration"),
        help_text=_("In months"),
    )

    @property
    def study_end(self):
        return self.study_begin + relativedelta(months=self.study_duration)

    @property
    def study_end_str(self) -> str:
        return self.study_end.strftime(UKRAINIAN_DATE_FORMAT)

    @property
    def study_duration_years(self) -> int:
        return self.study_duration // 12

    @property
    def study_duration_months(self) -> int:
        return self.study_duration % 12

    educational_program = models.ForeignKey(
        EducationalProgram,
        on_delete=models.PROTECT,
        verbose_name=_("Educational program"),
    )

    level = models.PositiveIntegerField(
        choices=EducationalLevel.choices, verbose_name=_("Educational level")
    )

    basis = models.PositiveIntegerField(
        choices=Basis.choices,
        verbose_name=_("Basis"),
    )

    type = models.PositiveIntegerField(
        choices=Type.choices,
        verbose_name=_("Offer type"),
        help_text=_("Budget or contract"),
    )

    study_form = models.PositiveIntegerField(
        choices=StudyForm.choices, verbose_name=_("Study form")
    )

    @property
    def get_study_form_label(self) -> str:
        return self.StudyForm(self.study_form).label

    @property
    def study_form_o(self) -> str:
        match self.study_form:
            case self.StudyForm.DAY:
                return "денної"
            case self.StudyForm.OVER_DISTANCE:
                return "заочної"
            case self.StudyForm.DISTANCE:
                return "дистанційної"
            case _:
                raise Exception("It can't be: " + self.StudyForm(self.study_form).label)

    ects = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("ECTS")
    )

    year1_cost = models.PositiveIntegerField(verbose_name=_("Year 1 cost"), default=0)

    year2_cost = models.PositiveIntegerField(verbose_name=_("Year 2 cost"), default=0)

    year3_cost = models.PositiveIntegerField(verbose_name=_("Year 3 cost"), default=0)

    year4_cost = models.PositiveIntegerField(verbose_name=_("Year 4 cost"), default=0)

    @property
    def year1_cost_words(self) -> str:
        return generate_currency_str(self.year1_cost)

    @property
    def year2_cost_words(self) -> str:
        return generate_currency_str(self.year2_cost)

    @property
    def year3_cost_words(self) -> str:
        return generate_currency_str(self.year3_cost)

    @property
    def year4_cost_words(self) -> str:
        return generate_currency_str(self.year4_cost)

    @property
    def full_cost(self) -> int:
        return self.year1_cost + self.year2_cost + self.year3_cost + self.year4_cost

    @property
    def full_cost_words(self) -> str:
        return generate_currency_str(self.full_cost)

    def __str__(self) -> str:
        return self.str_property

    @property
    def str_property(self) -> str:
        return (
            str(self.educational_program)
            + " - "
            + self.StudyForm(self.study_form).label
            + " - "
            + self.Type(self.type).label
        )

    @property
    def get_accreditation(self) -> Optional["Accreditation"]:
        return self.educational_program.accreditation_set.filter(
            level=self.level
        ).first()

    @property
    def has_accreditation_s(self) -> str:
        if self.get_accreditation:
            return "акредитованою"

        return "не акредитованою"

    @property
    def money_source(self) -> str:
        if self.type == UniversityOffer.Type.BUDGET:
            return "за державним замовленням"
        else:
            return "навчання за кошти фізичних або юридичних осіб"

    @property
    def get_level_label(self) -> str:
        return EducationalLevel(self.level).label

    class Meta:
        verbose_name = _("University offer")
        verbose_name_plural = _("University offers")


def generate_currency_str(num: int) -> str:
    from num2words import num2words

    return num2words(num, lang="uk", to="currency", currency="UAH").split(",")[1]
