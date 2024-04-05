from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


name_validator = RegexValidator("([^\W\d]| )+", _("abiturients.invalid_name_part"))
only_alpha_validator = RegexValidator("[^\W\d]+", _("generic.only_alpha"))
number_validator = RegexValidator("\d+", _("generic.only_numbers"))


telephone_validators = [number_validator]
telephone_verbose_name = _("generic.telephone")
telephone_max_length = 12


# Абітурієнт.
class Abiturient(models.Model):
    class Sex(models.IntegerChoices):
        MALE = 1, _("generic.sex.male")
        FEMALE = 2, _("generic.sex.female")

    last_name = models.CharField(
        max_length=255, verbose_name=_("generic.last_name"), validators=[name_validator]
    )

    first_name = models.CharField(
        max_length=255,
        verbose_name=_("generic.first_name"),
        validators=[name_validator],
    )

    patronymic = models.CharField(
        max_length=255,
        verbose_name=_("generic.patronymic"),
        validators=[name_validator],
    )

    sex = models.PositiveIntegerField(
        choices=Sex.choices, verbose_name=_("generic.sex")
    )

    birth_date = models.DateField(verbose_name=_("abiturient.birth_date"))

    birth_country = models.CharField(
        max_length=255, verbose_name=_("abiturient.birth_country")
    )

    birth_town = models.CharField(
        max_length=255, verbose_name=_("abiturient.birth_town")
    )

    education = models.TextField(verbose_name=_("abiturient.education"))

    email = models.EmailField(verbose_name=_("generic.email"))

    foreign_language = models.CharField(
        max_length=255,
        verbose_name=_("generic.foreign_language"),
        validators=[only_alpha_validator],
    )

    nationality = models.CharField(
        max_length=255,
        verbose_name=_("generic.nationality"),
        null=True,
        blank=True,
        validators=[only_alpha_validator],
    )

    work = models.TextField(verbose_name=_("abiturient.work"))

    registered_address = models.TextField(
        verbose_name=_("abiturient.registered_address")
    )

    living_address = models.TextField(verbose_name=_("abiturient.living_address"))

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    @property
    def sex_label(self) -> str:
        return self.Sex(self.sex).label

    class Meta:
        verbose_name = _("abiturient")
        verbose_name_plural = _("abiturient.plural")


# Член сім'ї.
class FamilyMember(models.Model):
    class Type(models.IntegerChoices):
        MOTHER = 1, _("family_member.type.mother")
        FATHER = 2, _("family_member.type.father")
        OTHER = 3, _("family_member.type.other")

    type = models.IntegerField(
        choices=Type.choices, verbose_name=_("family_member.type")
    )

    last_name = models.CharField(
        max_length=255, verbose_name=_("generic.last_name"), validators=[name_validator]
    )

    first_name = models.CharField(
        max_length=255,
        verbose_name=_("generic.first_name"),
        validators=[name_validator],
    )

    patronymic = models.CharField(
        max_length=255,
        verbose_name=_("generic.patronymic"),
        validators=[name_validator],
    )

    telephone = models.CharField(
        max_length=telephone_max_length,
        validators=telephone_validators,
        verbose_name=telephone_verbose_name,
    )

    abiturient = models.ForeignKey(
        Abiturient, on_delete=models.CASCADE, verbose_name=_("abiturient")
    )

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic} - {self.Type(self.type).label} - {_('abiturient')} {self.abiturient}"

    class Meta:
        verbose_name = _("family_member")
        verbose_name_plural = _("family_member.plural")


# Телефон.
class Phone(models.Model):
    class Type(models.IntegerChoices):
        HOME = 1, _("phone.type.home")
        MOBILE = 2, _("phone.type.mobile")
        WORK = 3, _("phone.type.work")

    type = models.IntegerField(choices=Type.choices, verbose_name=_("phone.type"))

    telephone = models.CharField(
        max_length=telephone_max_length,
        validators=telephone_validators,
        verbose_name=telephone_verbose_name,
    )

    abiturient = models.ForeignKey(
        Abiturient, on_delete=models.CASCADE, verbose_name=_("abiturient")
    )

    def __str__(self) -> str:
        return f"{self.abiturient} - {self.Type(self.type).label} - {self.telephone}"

    class Meta:
        verbose_name = _("phone")
        verbose_name_plural = _("phone.plural")

    field_order = ["type", "number"]
