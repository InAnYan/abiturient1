from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from abiturients.models import Abiturient
from university_offers.models import UniversityOffer


class AcceptedOffer(models.Model):
    class PaymentFrequency(models.IntegerChoices):
        EACH_SEMESTER = 1, _("Each semester")
        EACH_YEAR = 2, _("Each year")
        FULL = 3, _("Full payment")

    abiturient = models.ForeignKey(
        Abiturient, on_delete=models.PROTECT, verbose_name=_("Abiturient")
    )

    offer = models.ForeignKey(
        UniversityOffer, on_delete=models.PROTECT, verbose_name=_("University offer")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    payment_frequency = models.IntegerField(
        choices=PaymentFrequency.choices,
        verbose_name=_("Payment frequency"),
        blank=True,
        null=True,
    )

    @property
    def get_payment_frequency_label(self) -> str:
        return AcceptedOffer.PaymentFrequency(self.payment_frequency).label

    accepted_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name=_("Accepted year"),
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
        verbose_name = _("Accepted offer")
        verbose_name_plural = _("Accepted offers")
