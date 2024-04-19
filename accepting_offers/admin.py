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
from documents.generation import (
    add_content_disposition_header,
    generate_document,
    generate_document_filename,
    generate_document_response,
)
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

        return generate_document_response(offer, doc)

    make_document.short_description = (
        _("accepting_offers.admin.make_document") + " " + doc.name
    )
    make_document.__name__ = "make_document_" + str(doc.pk)

    return make_document
