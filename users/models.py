from django.contrib.auth.models import AbstractUser

from django.db import models

from university_offers.models import Faculty


class User(AbstractUser):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, null=True, blank=True
    )
