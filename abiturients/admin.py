from django.contrib import admin

from abiturients.models import (
    Abiturient,
    AbiturientRepresentative,
)


@admin.register(Abiturient)
class AbiturientAdmin(admin.ModelAdmin):
    model = Abiturient
    list_per_page = 15


@admin.register(AbiturientRepresentative)
class AbiturientRepresentativeAdmin(admin.ModelAdmin):
    model = AbiturientRepresentative
    list_per_page = 15
