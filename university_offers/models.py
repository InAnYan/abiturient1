from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator
from dateutil.relativedelta import relativedelta
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Faculty(models.Model):
    full_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("generic.full_name"),
    )

    abbreviation = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("generic.abbreviation"),
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("faculty")
        verbose_name_plural = _("faculty.plural")


class Speciality(models.Model):
    code = models.IntegerField(verbose_name=_("generic.code"))

    name = models.CharField(
        max_length=255,
        verbose_name=_("generic.name"),
    )

    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, verbose_name=_("faculty")
    )

    specialization_code = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("speciality.specialization_code"),
    )

    def __str__(self) -> str:
        return self.faculty.abbreviation + " - " + self.code_and_name

    @property
    def code_and_name(self) -> str:
        code = str(self.code).zfill(3)
        if self.specialization_code:
            code += "." + str(self.specialization_code).zfill(3)

        return code + " " + self.name

    class Meta:
        verbose_name = _("speciality")
        verbose_name_plural = _("speciality.plural")


class EducationalProgram(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("generic.name"),
    )

    speciality = models.ForeignKey(
        Speciality, on_delete=models.PROTECT, verbose_name=_("speciality")
    )

    """
    @property
    def has_accreditation(self) -> str:
        if (
            self.end_of_accreditation
            and self.end_of_accreditation > datetime.now().date()
        ):
            return _("educational_program.has_accreditation")
        else:
            return _("educational_program.not_has_accreditation")
    """

    def __str__(self) -> str:
        return f"{self.speciality} - {self.name}"


class EducationalLevel(models.IntegerChoices):
    BACHELOR = 1, _("university_offer.level.bachelor")
    MASTER = 2, _("university_offer.level.master")
    PHD = 3, _("university_offer.level.aspirant")


class Accreditation(models.Model):
    class Type(models.IntegerChoices):
        SPECIALITY = 1, _("accreditation.type.speciality")
        EDUCATIONAL_PROGRAM = 2, _("accreditation.type.educational_program")

    educational_program = models.ForeignKey(
        EducationalProgram, on_delete=models.PROTECT, verbose_name=_("educational_program")
    )

    level = models.IntegerField(
        choices=EducationalLevel.choices,
        verbose_name=_("educational_level"),
    )

    end_date = models.DateField(verbose_name=_("accreditation.end_date"))

    number = models.PositiveIntegerField(verbose_name=_("accreditation.number"))

    serie = models.CharField(max_length=2, null=True, blank=True, verbose_name=_("accreditation.serie"))

    type = models.PositiveIntegerField(
        choices=Type.choices,
        verbose_name=_("accreditation.type"), 
    )

    def __str__(self) -> str:
        return f"{self.serie + " " if self.serie else " "}{self.number} - {self.educational_program}"

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
        verbose_name = _("accreditation")
        verbose_name_plural = _("accreditation.plural")


class UniversityOffer(models.Model):
    class Type(models.IntegerChoices):
        BUDGET = 1, _("university_offer.type.budget")
        CONTRACT = 2, _("university_offer.type.contract")

    class StudyForm(models.IntegerChoices):
        DAY = 1, _("university_offer.study_form.day")
        OVER_DISTANCE = 2, _("university_offer.study_form.over_distance")
        DISTANCE = 3, _("university_offer.study_form.distance")

    class Basis(models.IntegerChoices):
        PZSO = 1, _("university_offer.basis.pzso")
        NRK_5 = 2, _("university_offer.basis.nrk_5")
        NRK_6_7 = 3, _("university_offer.basis.nrk_6_7")

    study_begin = models.DateField(verbose_name=_("university_offer.study_begin"))

    study_duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("university_offer.study_duration"),
    )

    @property
    def study_end(self):
        return self.study_begin + relativedelta(months=self.study_duration)

    @property
    def study_duration_years(self) -> int:
        return self.study_duration // 12

    @property
    def study_duration_months(self) -> int:
        return self.study_duration % 12

    educational_program = models.ForeignKey(
        EducationalProgram, on_delete=models.PROTECT, verbose_name=_("speciality")
    )

    level = models.PositiveIntegerField(
        choices=EducationalLevel.choices, verbose_name=_("university_offer.level")
    )

    basis = models.PositiveIntegerField(
        choices=Basis.choices,
        verbose_name=_("university_offers.basis"),
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

    year1_cost = models.PositiveIntegerField(
        verbose_name=_("university_offer.year1_cost"), default=0
    )

    year2_cost = models.PositiveIntegerField(
        verbose_name=_("university_offer.year2_cost"), default=0
    )

    year3_cost = models.PositiveIntegerField(
        verbose_name=_("university_offer.year3_cost"), default=0
    )

    year4_cost = models.PositiveIntegerField(
        verbose_name=_("university_offer.year4_cost"), default=0
    )

    @property
    def year1_cost_words(self) -> str:
        from num2words import num2words

        return num2words(self.year1_cost, lang="uk")

    @property
    def year2_cost_words(self) -> str:
        from num2words import num2words

        return num2words(self.year2_cost, lang="uk")

    @property
    def year3_cost_words(self) -> str:
        from num2words import num2words

        return num2words(self.year3_cost, lang="uk")

    @property
    def year4_cost_words(self) -> str:
        from num2words import num2words

        return num2words(self.year4_cost, lang="uk")

    @property
    def full_cost(self) -> int:
        return self.year1_cost + self.year2_cost + self.year3_cost + self.year4_cost

    @property
    def full_cost_words(self) -> str:
        from num2words import num2words

        return num2words(self.full_cost, lang="uk")

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

    class Meta:
        verbose_name = _("university_offer")
        verbose_name_plural = _("university_offer.plural")
