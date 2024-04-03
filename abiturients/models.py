from django.db import models
from django.utils.translation import gettext_lazy as _


# Абітурієнт.
class Abiturient(models.Model):
    class Sex(models.IntegerChoices):
        MALE = 1, _("generic.sex.male")
        FEMALE = 2, _("generic.sex.female")

    last_name = models.CharField(max_length=255, verbose_name=_("generic.last_name"))
    first_name = models.CharField(max_length=255, verbose_name=_("generic.first_name"))
    patronymic = models.CharField(max_length=255, verbose_name=_("generic.patronymic"))

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
        max_length=255, verbose_name=_("generic.foreign_language")
    )
    nationality = models.CharField(
        max_length=255, verbose_name=_("generic.nationality"), null=True, blank=True
    )
    work = models.TextField(verbose_name=_("abiturient.work"))

    registered_address = models.TextField(
        verbose_name=_("abiturient.registered_address")
    )
    living_address = models.TextField(verbose_name=_("abiturient.living_address"))

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"

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

    last_name = models.CharField(max_length=255, verbose_name=_("generic.last_name"))
    first_name = models.CharField(max_length=255, verbose_name=_("generic.first_name"))
    patronymic = models.CharField(max_length=255, verbose_name=_("generic.patronymic"))

    telephone = models.CharField(max_length=255, verbose_name=_("generic.telephone"))

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
    number = models.CharField(max_length=255, verbose_name=_("phone.number"))
    abiturient = models.ForeignKey(
        Abiturient, on_delete=models.CASCADE, verbose_name=_("abiturient")
    )

    def __str__(self) -> str:
        return f"{self.abiturient} - {self.Type(self.type).label} - {self.number}"

    class Meta:
        verbose_name = _("phone")
        verbose_name_plural = _("phone.plural")
