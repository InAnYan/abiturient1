from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AcceptingOffersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accepting_offers"
    verbose_name = _("accepting_offers")
