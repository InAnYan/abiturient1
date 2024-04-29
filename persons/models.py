from signal import valid_signals
from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import date

from django.core.validators import MaxValueValidator

from django.core.validators import RegexValidator


class Person(models.Model):
    last_name = models.CharField(max_length=255, verbose_name=_("generic.last_name"))

    first_name = models.CharField(
        max_length=255,
        verbose_name=_("generic.first_name"),
    )

    patronymic = models.CharField(
        max_length=255,
        verbose_name=_("generic.patronymic"),
    )

    phone = models.CharField(
        verbose_name=_("generic.telephone"),
        validators=[
            RegexValidator(r"^\+\d{10,13}$", _("generic.only_numbers")),
        ],
        help_text=_("telephone.help"),
        max_length=13,
    )

    email = models.EmailField(verbose_name=_("generic.email"))

    living_address = models.TextField(verbose_name=_("abiturient.living_address"))

    passport = models.OneToOneField(
        "Passport",
        on_delete=models.PROTECT,
        verbose_name=_("persons.passport"),
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("persons.parent"),
    )

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    class Meta:
        verbose_name = _("abiturient")
        verbose_name_plural = _("abiturient.plural")


class Passport(models.Model):
    serie = models.CharField(
        verbose_name=_("persons.passport_serie"),
        max_length=2,
        null=True,
        blank=True,
        help_text=_("passport.serie.help"),
    )

    number = models.IntegerField(
        verbose_name=_("persons.passport_number"),
        validators=[MaxValueValidator(999999999)],
    )

    who_give = models.TextField(
        verbose_name=_("persons.passport_who_give"),
        help_text=_("passport.who_give.help"),
    )

    when_given = models.DateField(
        verbose_name=_("persons.passport_when_given"),
        validators=[MaxValueValidator(limit_value=date.today)],
    )

    inn = models.IntegerField(
        verbose_name=_("persons.inn"),
        validators=[MaxValueValidator(999999999999)],
        help_text=_("persons.inn.help"),
    )

    class Meta:
        verbose_name = _("persons.passport")
        verbose_name_plural = _("persons.passport.plural")
