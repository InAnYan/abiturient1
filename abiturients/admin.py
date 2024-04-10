from datetime import datetime
from django.contrib import admin

from abiturient1.settings import MEDIA_ROOT
from abiturients.models import Abiturient, FamilyMember, Phone

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.utils import formats

from docxtpl import DocxTemplate

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

abiturient_full_name = fields.Field(
    column_name="abiturient_full_name",
    attribute="abiturient",
    widget=widgets.ForeignKeyWidget(Abiturient, "full_name"),
)


class AbiturientResource(resources.ModelResource):
    class Meta:
        model = Abiturient


class FamilyMemberResource(resources.ModelResource):
    abiturient_id = abiturient_full_name

    class Meta:
        model = FamilyMember


class PhoneResource(resources.ModelResource):
    abiturient_id = abiturient_full_name

    class Meta:
        model = Phone


class FamilyMemberInline(admin.StackedInline):
    model = FamilyMember
    extra = 0


class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 0


@admin.register(Abiturient)
class AbiturientAdmin(ImportExportModelAdmin):
    @admin.action(
        description=_("Make abiturient info")
    )  # NOTE: Yep, the translation key is not in the project style. That's a mistake.
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
        context = {"abiturients": list(queryset)}
        doc.render(context)
        doc.save(response)
        return response

    actions = [make_abiturient_info]
    resource_classes = [AbiturientResource]
    inlines = [FamilyMemberInline, PhoneInline]
    search_fields = ["last_name", "first_name", "patronymic", "email"]


@admin.register(FamilyMember)
class FamilyMemberAdmin(ImportExportModelAdmin):
    resource_classes = [FamilyMemberResource]


@admin.register(Phone)
class PhoneAdmin(ImportExportModelAdmin):
    resource_classes = [PhoneResource]
