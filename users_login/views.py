from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import LoginForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
from django.shortcuts import redirect


def user_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("pk_panel"))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect(reverse("pk_panel"))
            else:
                form.add_error("password", _("auth.login.failed"))
    else:
        form = LoginForm()
    return render(request, "users_login/login.html", {"form": form})


def user_logout(request: HttpRequest):
    logout(request)
    return redirect(reverse("login"))
