from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            _("users.additional_fields"),
            {
                "fields": ("faculty",),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
