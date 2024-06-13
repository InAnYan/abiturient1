from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from university_offers.models import (
    Accreditation,
    EducationalProgram,
    Faculty,
    Speciality,
    UniversityOffer,
)


class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty


class SpecialityResource(resources.ModelResource):
    faculty_abbrev = fields.Field(
        column_name="faculty_abbrev",
        attribute="faculty",
        widget=widgets.ForeignKeyWidget(Faculty, "abbreviation"),
    )

    class Meta:
        model = Speciality


class EducationalProgramResource(resources.ModelResource):
    class Meta:
        model = EducationalProgram


class AccreditationResource(resources.ModelResource):
    class Meta:
        model = Accreditation


class UniversityOfferResource(resources.ModelResource):
    class Meta:
        model = UniversityOffer


@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    resource_classes = [FacultyResource]
    list_per_page = 15


@admin.register(Speciality)
class SpecialityAdmin(ImportExportModelAdmin):
    resource_classes = [SpecialityResource]
    list_per_page = 15


@admin.register(EducationalProgram)
class EducationalProgramAdmin(ImportExportModelAdmin):
    resource_classes = [EducationalProgramResource]
    list_per_page = 15


@admin.register(Accreditation)
class AccreditationAdmin(ImportExportModelAdmin):
    resource_classes = [AccreditationResource]
    list_per_page = 15


@admin.register(UniversityOffer)
class UniversityOfferAdmin(ImportExportModelAdmin):
    resource_classes = [UniversityOfferResource]
    list_per_page = 15
