from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
