from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from abiturients.models import Abiturient
from university_offers.models import UniversityOffer


# Заява.
class AcceptedOffer(models.Model):
    # Періодичність оплати.
    class PaymentFrequency(models.IntegerChoices):
        EVERY_SEMESTER = 1, "Щосеместрово"
        EVERY_YEAR = 2, "Щорічно"
        EVERY_MONTH = 3, "Щомісячно"
        FULL = 4, "Повна за весь період навчання"

    # Тип фінансування.
    class PaymentType(models.IntegerChoices):
        GOVERNMENTAL = 1, "Державне замовлення"
        TOWN = 2, "Місцевого замовлення"
        PRIVATE = 3, "Кошти юридичних та/або фізичних осіб"
        PRIVILEGED = 4, "Пільгове"

    abiturient = models.ForeignKey(Abiturient, on_delete=models.PROTECT)
    offer = models.ForeignKey(UniversityOffer, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    payment_type = models.IntegerField(choices=PaymentType.choices)
    payment_frequency = models.IntegerField(choices=PaymentFrequency.choices)

    accepted_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
