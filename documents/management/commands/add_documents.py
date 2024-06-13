from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import os

from abiturient1.settings import BASE_DIR
from documents.models import Document


documents_path = BASE_DIR / "documents" / "documents_templates"


class Command(BaseCommand):
    help = _("Add document templates")

    def handle(self, *args, **options):
        for file in os.listdir(documents_path):
            with open(os.path.join(documents_path, file), "rb") as f:
                doc = Document()
                doc.name = file[:-5]

                if doc.name == "Контракт":
                    doc.only_for_contract = True

                if doc.name == "Анкета 2":
                    doc.only_for_full_time = True

                doc.file.save(doc.name, f)
                doc.save()
