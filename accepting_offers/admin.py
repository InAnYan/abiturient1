from datetime import datetime
from typing import Any
from django.contrib import admin
from django.db.models import QuerySet
from django.contrib import messages
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from django.http import HttpRequest, HttpResponse
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from abiturient1.settings import MEDIA_ROOT
from persons.models import Person
from accepting_offers.models import AcceptedOffer
from documents.models import Document
from university_offers.models import UniversityOffer

from docxtpl import DocxTemplate


class AcceptedOfferResource(resources.ModelResource):
    abiturient_full_name = fields.Field(
        column_name="abiturient_full_name",
        attribute="abiturient",
        widget=widgets.ForeignKeyWidget(Person, "full_name"),
    )

    offer_str = fields.Field(
        column_name="offer_str",
        attribute="offer",
        widget=widgets.ForeignKeyWidget(UniversityOffer, "str_property"),
    )

    class Meta:
        model = AcceptedOffer


@admin.register(AcceptedOffer)
class AcceptedOfferAdmin(ImportExportModelAdmin):
    resource_classes = [AcceptedOfferResource]
    search_fields = [
        "abiturient__last_name",
        "abiturient__first_name",
        "abiturient__patronymic",
        "abiturient__email",
    ]

    def get_actions(self, request: HttpRequest) -> resources.OrderedDict[Any, Any]:
        actions = super(AcceptedOfferAdmin, self).get_actions(request)

        for document in Document.objects.all():
            action = make_document_action(document)
            actions[action.__name__] = (
                action,
                action.__name__,
                action.short_description,
            )

        return actions


# Source: https://medium.com/@JeremyLaine/non-ascii-content-disposition-header-in-django-3a20acc05f0d
from urllib.parse import quote


def add_content_disposition_header(response, filename):
    """
    Add an RFC5987 / RFC6266 compliant Content-Disposition header to an
    HttpResponse to tell the browser to save the HTTP response to a file.
    """
    try:
        filename.encode("ascii")
        file_expr = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(filename))
    response["Content-Disposition"] = "attachment; {}".format(file_expr)
    return response


# --------------------------------------------------------------------------------------------------


def make_document_action(doc: Document):
    def make_document(
        modeladmin: AcceptedOfferAdmin,
        request: HttpRequest,
        queryset: QuerySet[AcceptedOffer],
    ):
        if len(queryset) != 1:
            modeladmin.message_user(
                request,
                _("accepting_offers.admin.only_one_offer"),
                level=messages.ERROR,
            )
            return

        offer: AcceptedOffer = queryset.get()
        offer.offer.study_form = UniversityOffer.StudyForm(offer.offer.study_form).label
        offer.offer.type = UniversityOffer.Type(offer.offer.type).label

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                if doc.file.name.endswith(".docx")
                else "application/msword"
            )
        )

        now = datetime.now()
        formatted_now = formats.date_format(now, "SHORT_DATETIME_FORMAT")

        add_content_disposition_header(
            response,
            doc.name + "_" + offer.abiturient.full_name + "_" + formatted_now + ".docx",
        )

        doc_templ = DocxTemplate(doc.file.path)
        context = {"offer": offer}
        doc_templ.render(context)
        doc_templ.save(response)
        return response

    make_document.short_description = (
        _("accepting_offers.admin.make_document") + " " + doc.name
    )
    make_document.__name__ = "make_document_" + str(doc.pk)

    return make_document
