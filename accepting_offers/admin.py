from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from accepting_offers.models import AcceptedOffer


class AcceptedOfferResource(resources.ModelResource):
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

    list_per_page = 15
