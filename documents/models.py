from django.db import models
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("document.plural")
