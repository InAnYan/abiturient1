from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.db import transaction

from abiturients.forms import AbiturientForm, FamilyMemberFormSet, PhoneFormSet
from abiturients.models import Abiturient
from accepting_offers.forms import AcceptedOfferFormSet

from formtools.wizard.views import CookieWizardView


def done(request):
    return render(request, "done.html")


class AbiturientAndOffersWizard(CookieWizardView):
    form_list = [
        AbiturientForm,
        PhoneFormSet,
        FamilyMemberFormSet,
        AcceptedOfferFormSet,
    ]
    template_name = "wizard.html"

    def done(self, form_list, **kwargs):
        form, phone_set, family_member_set, accepted_offer_set = form_list

        with transaction.atomic():
            self.object = form.save()

            phone_set.instance = self.object
            phone_set.save()

            family_member_set.instance = self.object
            family_member_set.save()

            accepted_offer_set.instance = self.object
            accepted_offer_set.save()

        return HttpResponseRedirect(reverse("done"))
