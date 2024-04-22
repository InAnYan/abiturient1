from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

capitalize_lazy = lazy(lambda s: s.capitalize(), str)


class LoginForm(forms.Form):
    username = forms.CharField(label=capitalize_lazy(_("users_login.username")))
    password = forms.CharField(
        widget=forms.PasswordInput, label=capitalize_lazy(_("users_login.password"))
    )
