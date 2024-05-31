from django.contrib import admin

from abiturients.models import (
    Abiturient,
    AbiturientRepresentative,
)

admin.site.register(Abiturient)
admin.site.register(AbiturientRepresentative)
