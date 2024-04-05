from django.contrib import admin

from abiturient1.settings import MEDIA_ROOT
from abiturients.models import Abiturient, FamilyMember, Phone

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from docxtpl import DocxTemplate


class AbiturientAdmin(admin.ModelAdmin):
    @admin.action(description=_("Make abiturient info"))
    def make_abiturient_info(self, request: HttpRequest, queryset: QuerySet):
        print(dir(queryset.first()))
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        doc = DocxTemplate(MEDIA_ROOT / "abiturient_info.docx")
        context = {"abiturients": list(queryset)}
        doc.render(context)
        doc.save(response)
        return response

    actions = [make_abiturient_info]


admin.site.register(Abiturient, AbiturientAdmin)
admin.site.register(FamilyMember)
admin.site.register(Phone)
