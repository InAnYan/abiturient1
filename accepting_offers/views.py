from mmap import ACCESS_COPY
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction

from abiturients.forms import AbiturientForm, FamilyMemberFormSet, PhoneFormSet
from accepting_offers.forms import (
    AcceptedOfferForm,
)

from formtools.wizard.views import SessionWizardView


def done(request):
    from django.urls import get_resolver

    print(get_resolver().reverse_dict.keys())
    return render(request, "accepting_offers/done.html")


class AbiturientAndOffersWizard(SessionWizardView):
    form_list = [AbiturientForm, PhoneFormSet, FamilyMemberFormSet, AcceptedOfferForm]

    def get_template_names(self) -> list[str]:
        match self.steps.current:
            case "0":
                return ["accepting_offers/wizard_steps/step1.html"]
            case "1":
                return ["accepting_offers/wizard_steps/step2.html"]
            case "2":
                return ["accepting_offers/wizard_steps/step3.html"]
            case "3":
                # BUG: ON VALIDATION ERRORS FIELDS BECOME EMPTY.
                return ["accepting_offers/wizard_steps/step4.html"]
            case _:
                raise NotImplementedError()

    def done(self, form_list, **kwargs):
        form, phone_set, family_member_set, accepted_offer = form_list

        with transaction.atomic():
            abiturient = form.save()

            phone_set.instance = abiturient
            phone_set.save()

            family_member_set.instance = abiturient
            family_member_set.save()

            accepted_offer: AcceptedOfferForm
            accepted_offer.set_abiturient(abiturient)
            accepted_offer.save()

        return HttpResponseRedirect(reverse("done"))
