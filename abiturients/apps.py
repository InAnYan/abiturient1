from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AbiturientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "abiturients"
    verbose_name = _("abiturients")
