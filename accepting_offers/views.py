from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.db import transaction

from abiturients.models import Abiturient
from accepting_offers import forms
from accepting_offers.forms import AbiturientForm, AcceptedOfferFormSet

import logging

logger = logging.getLogger(__name__)


def form(request: HttpRequest):
    if request.method == "POST":
        form = MainForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("done"))
    else:
        form = AbiturientForm()

    context = {"form": form}

    return render(request, "form.html", context)


def done(request):
    return render(request, "done.html")


class CreateAbiturientView(CreateView):
    template_name = "form.html"
    model = Abiturient
    form_class = AbiturientForm
    success_url = "done"

    def get_context_data(self, **kwargs):
        context = super(CreateAbiturientView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = AcceptedOfferFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = AcceptedOfferFormSet(instance=self.object)
        return context

    def form_valid(self, form, formset: AcceptedOfferFormSet):
        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = AcceptedOfferFormSet(self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
