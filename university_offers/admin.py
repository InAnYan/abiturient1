from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from university_offers.models import Accreditation, EducationalProgram, Faculty, Speciality, UniversityOffer


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


@admin.register(Speciality)
class SpecialityAdmin(ImportExportModelAdmin):
    resource_classes = [SpecialityResource]


@admin.register(EducationalProgram)
class EducationalProgramAdmin(ImportExportModelAdmin):
    resource_classes = [EducationalProgramResource]

@admin.register(Accreditation)
class AccreditationAdmin(ImportExportModelAdmin):
    resource_classes = [AccreditationResource]

@admin.register(UniversityOffer)
class UniversityOfferAdmin(ImportExportModelAdmin):
    resource_classes = [UniversityOfferResource]

