from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer
from university_offers.models import UniversityOffer


class AcceptedOfferResource(resources.ModelResource):
    abiturient_full_name = fields.Field(
        column_name="abiturient_full_name",
        attribute="abiturient",
        widget=widgets.ForeignKeyWidget(Abiturient, "full_name"),
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
