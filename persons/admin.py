from datetime import datetime
from django.contrib import admin

from abiturient1.settings import MEDIA_ROOT
from persons.models import Person

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.utils import formats

from docxtpl import DocxTemplate


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    @admin.action(description=_("persons.admin.make_info"))
    def make_abiturient_info(self, request: HttpRequest, queryset: QuerySet):
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        now = datetime.now()
        formatted_now = formats.date_format(now, "SHORT_DATETIME_FORMAT")

        response["Content-Disposition"] = (
            'attachment; filename="'
            + _("abiturient.report")
            + "_"
            + formatted_now
            + '.docx"'
        )

        doc = DocxTemplate(MEDIA_ROOT / "abiturient_info.docx")
        context = {"persons": list(queryset)}
        doc.render(context)
        doc.save(response)
        return response

    actions = [make_abiturient_info]
    search_fields = ["last_name", "first_name", "patronymic", "email"]
