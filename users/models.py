from django.contrib.auth.models import AbstractUser

from django.db import models

from university_offers.models import Faculty

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
