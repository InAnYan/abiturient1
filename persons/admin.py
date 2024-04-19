from datetime import datetime
from django.contrib import admin

from abiturient1.settings import MEDIA_ROOT
from persons.models import Person

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.utils import formats

from docxtpl import DocxTemplate


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["last_name", "first_name", "patronymic", "email"]
