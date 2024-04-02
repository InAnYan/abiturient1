from django.contrib import admin

from abiturients.models import Abiturient, FamilyMember, Phone


admin.site.register(Abiturient)
admin.site.register(FamilyMember)
admin.site.register(Phone)
