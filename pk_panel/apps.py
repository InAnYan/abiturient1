from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PkPanelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pk_panel"
    verbose_name = _("Addmision office panel")
