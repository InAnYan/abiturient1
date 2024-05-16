from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UniversityOffersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "university_offers"
    verbose_name = _("University offers")
