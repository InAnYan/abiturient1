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
    from django.urls import get_resolver

    print(get_resolver().reverse_dict.keys())
    return render(request, "accepting_offers/done.html")


class AbiturientAndOffersWizard(CookieWizardView):
    form_list = [
        AbiturientForm,
        PhoneFormSet,
        FamilyMemberFormSet,
        AcceptedOfferFormSet,
    ]

    def get_template_names(self) -> list[str]:
        match self.steps.current:
            case "0":
                return ["accepting_offers/wizard_steps/step1.html"]
            case "1":
                return ["accepting_offers/wizard_steps/step2.html"]
            case "2":
                return ["accepting_offers/wizard_steps/step3.html"]
            case "3":
                return ["accepting_offers/wizard_steps/step4.html"]
            case _:
                raise NotImplementedError()

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
