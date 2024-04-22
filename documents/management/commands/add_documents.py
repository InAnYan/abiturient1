from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import os

from abiturient1.settings import BASE_DIR
from documents.models import Document


documents_path = BASE_DIR / "documents" / "documents_templates"


class Command(BaseCommand):
    help = _("documents.add_documents.help")

    def handle(self, *args, **options):
        for file in os.listdir(documents_path):
            with open(os.path.join(documents_path, file), "rb") as f:
                doc = Document()
                doc.name = file[:-5]
                doc.file.save(doc.name, f)
                doc.save()
