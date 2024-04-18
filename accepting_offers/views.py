from typing import Optional
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction

from accepting_offers.forms import AcceptedOfferForm
from persons.forms import AbiturientForm, PersonForm

from formtools.wizard.views import CookieWizardView


def done(request):
    from django.urls import get_resolver

    print(get_resolver().reverse_dict.keys())
    return render(request, "accepting_offers/done.html")


class AbiturientAndOffersWizard(CookieWizardView):
    form_list = [
        ("abiturient", AbiturientForm),
        ("parent", PersonForm),
        ("offer", AcceptedOfferForm),
    ]

    def should_be_parent(self) -> bool:
        abiturient: dict | None = self.get_cleaned_data_for_step("abiturient")
        if not abiturient:
            return True

        return not abiturient["has_18_years"]

    condition_dict = {
        "abiturient": lambda _: True,
        "parent": should_be_parent,
        "offer": lambda _: True,
    }

    def get_template_names(self) -> list[str]:
        match self.steps.current:
            case "abiturient":
                return ["accepting_offers/wizard_steps/step1.html"]
            case "parent":
                return ["accepting_offers/wizard_steps/step2.html"]
            case "offer":
                return ["accepting_offers/wizard_steps/step3.html"]
            case _:
                raise NotImplementedError()

    def done(self, form_list, **kwargs):
        if len(form_list) == 3:
            abiturient_form, parent_form, accepted_offer = form_list
        else:
            abiturient_form, accepted_offer = form_list
            parent_form = None

        abiturient_form: AbiturientForm
        parent_form: Optional[PersonForm]
        accepted_offer: AcceptedOfferForm

        with transaction.atomic():
            if parent_form:
                parent = parent_form.save()
                abiturient_form.instance.parent = parent

            abiturient = abiturient_form.save()

            accepted_offer.set_abiturient(abiturient)
            accepted_offer.save()

        return HttpResponseRedirect(reverse("done"))
