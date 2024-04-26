from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from persons.models import Person
from university_offers.models import UniversityOffer


class AcceptedOffer(models.Model):
    class PaymentFrequency(models.IntegerChoices):
        EVERY_SEMESTER = 1, _("accepting_offers.payment_frequency.every_semester")
        EVERY_YEAR = 2, _("accepting_offers.payment_frequency.every_year")
        EVERY_MONTH = 3, _("accepting_offers.payment_frequency.every_month")
        FULL = 4, _("accepting_offers.payment_frequency.full")

    class PaymentType(models.IntegerChoices):
        TOWN = 2, _("accepting_offers.payment_type.town")
        PRIVATE = 3, _("accepting_offers.payment_type.private")
        PRIVILEGED = 4, _("accepting_offers.payment_type.privileged")

    abiturient = models.ForeignKey(
        Person, on_delete=models.PROTECT, verbose_name=_("abiturient")
    )

    offer = models.ForeignKey(
        UniversityOffer, on_delete=models.PROTECT, verbose_name=_("university_offer")
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("generic.created_at")
    )

    payment_type = models.IntegerField(
        choices=PaymentType.choices,
        verbose_name=_("accepting_offers.payment_type"),
        blank=True,
        null=True,
    )

    payment_frequency = models.IntegerField(
        choices=PaymentFrequency.choices,
        verbose_name=_("accepting_offers.payment_frequency"),
        blank=True,
        null=True,
    )

    accepted_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name=_("accepting_offers.accepted_year"),
    )

    def __str__(self) -> str:
        return f"{self.abiturient} - {self.offer}"

    # This requires offer to be. But in the wizard form I cannot pass it.
    """
    def clean(self) -> None:
        super().clean()
        if self.offer.type == UniversityOffer.Type.CONTRACT:
            if self.payment_type is None:
                raise ValidationError(
                    _("accepting_offers.payment_type_required_for_contract")
                )
            if self.payment_frequency is None:
                raise ValidationError(
                    _("accepting_offers.payment_frequency_required_for_contract")
                )
        elif self.offer.type == UniversityOffer.Type.BUDGET:
            if self.payment_type is not None:
                raise ValidationError(
                    _("accepting_offers.payment_type_not_required_for_budget")
                )
            if self.payment_frequency is not None:
                raise ValidationError(
                    _("accepting_offers.payment_frequency_not_required_for_budget")
                )
        else:
            raise NotImplementedError()
    """

    class Meta:
        verbose_name = _("accepted_offer")
        verbose_name_plural = _("accepted_offer.plural")
