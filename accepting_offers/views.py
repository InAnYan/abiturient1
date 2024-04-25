from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction

from accepting_offers.forms import AcceptedOfferForm
from persons.forms import AbiturientForm, PassportForm, PersonForm

from formtools.wizard.views import CookieWizardView

from university_offers.forms import UniversityOfferSearchForm


def done(request):
    from django.urls import get_resolver

    print(get_resolver().reverse_dict.keys())
    return render(request, "abiturient_form/done.html")


class AbiturientAndOffersWizard(CookieWizardView):
    form_list = [
        ("abiturient", AbiturientForm),
        ("abiturient_passport", PassportForm),
        ("parent", PersonForm),
        ("parent_passport", PassportForm),
        ("offer", UniversityOfferSearchForm),
        ("accepted_offer", AcceptedOfferForm),
    ]

    def should_be_parent(self) -> bool:
        abiturient: dict | None = self.get_cleaned_data_for_step("abiturient")
        if not abiturient:
            return True

        return not abiturient["has_18_years"]

    condition_dict = {
        "abiturient": lambda _: True,
        "abiturient_passport": lambda _: True,
        "parent": should_be_parent,
        "parent_passport": should_be_parent,
        "offer": lambda _: True,
        "accepted_offer": lambda _: True,
    }

    def get_template_names(self) -> list[str]:
        match self.steps.current:
            case "abiturient":
                return ["abiturient_form/wizard_steps/abiturient.html"]
            case "abiturient_passport":
                return ["abiturient_form/wizard_steps/abiturient_passport.html"]
            case "parent":
                return ["abiturient_form/wizard_steps/parent.html"]
            case "parent_passport":
                return ["abiturient_form/wizard_steps/parent_passport.html"]
            case "offer":
                return ["abiturient_form/wizard_steps/offer.html"]
            case "accepted_offer":
                return ["abiturient_form/wizard_steps/accepted_offer.html"]
            case _:
                raise NotImplementedError()

    def done(self, form_list, **kwargs):
        # That's easier.
        if len(form_list) == 4:
            abiturient_form: AbiturientForm = form_list[0]
            abiturient_passport_form: PassportForm = form_list[1]
            offer_form: UniversityOfferSearchForm = form_list[2]
            accepted_offer_form: AcceptedOfferForm = form_list[3]

            with transaction.atomic():
                abiturient_form.instance.passport = abiturient_passport_form.save()
                abiturient = abiturient_form.save()

                accepted_offer_form.instance.abiturient = abiturient
                accepted_offer_form.instance.offer = offer_form.cleaned_data[
                    "result_offer"
                ]
                accepted_offer_form.save()
        else:
            abiturient_form: AbiturientForm = form_list[0]
            abiturient_passport_form: PassportForm = form_list[1]
            parent_form: PersonForm = form_list[2]
            parent_passport_form: PassportForm = form_list[3]
            offer_form: UniversityOfferSearchForm = form_list[4]
            accepted_offer_form: AcceptedOfferForm = form_list[5]

            with transaction.atomic():
                parent_form.instance.passport = parent_passport_form.save()

                abiturient_form.instance.passport = abiturient_passport_form.save()
                abiturient_form.instance.parent = parent_form.save()
                abiturient = abiturient_form.save()

                accepted_offer_form.instance.abiturient = abiturient
                accepted_offer_form.instance.offer = offer_form.cleaned_data[
                    "result_offer"
                ]
                accepted_offer_form.save()

        return HttpResponseRedirect(reverse("done"))
