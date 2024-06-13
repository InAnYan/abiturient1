from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

ukrainian_validator = RegexValidator(
    r"^[А-Яа-яЄєІіЇїҐґ\'’` ]*$", _("Only Ukrainian letters allowed")
)
