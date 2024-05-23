from django.contrib import admin

from abiturients.models import (
    Abiturient,
    AbiturientRepresentative,
    ContactInformation,
    SensitiveInformation,
)

admin.site.register(Abiturient)
admin.site.register(ContactInformation)
admin.site.register(SensitiveInformation)
admin.site.register(AbiturientRepresentative)
