from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction

from abiturients.models import (
    Abiturient,
    AbiturientRepresentative,
    ContactInformation,
    SensitiveInformation,
)
from accepting_offers.forms import (
    AbiturientBasicInformationForm,
    AbiturientBirthInformationForm,
    AbiturientEducationForm,
    AbiturientMiscInformationForm,
    AbiturientParentsForm,
    AbiturientSensitiveInformationForm,
    AcceptedOfferForm,
    EmptyForm,
    RepresentativeContactForm,
    RepresentativeSensitiveInformationForm,
)

from formtools.wizard.views import CookieWizardView

from accepting_offers.models import AcceptedOffer
from university_offers.forms import UniversityOfferSearchForm
from university_offers.models import UniversityOffer


def done(request):
    from django.urls import get_resolver

    print(get_resolver().reverse_dict.keys())
    return render(request, "abiturient_form/done.html")


form_list_str = [
    "abiturient_basic",
    "abiturient_birth",
    "abiturient_education",
    "abiturient_misc",
    "offer",
    "accepted_offer",
    "abiturient_parents",
    "abiturient_sensitive",
    "representative_contact",
    "representative_sensitive",
    "check",
]


class AbiturientAndOffersWizard(CookieWizardView):
    form_list = [
        ("abiturient_basic", AbiturientBasicInformationForm),
        ("abiturient_birth", AbiturientBirthInformationForm),
        ("abiturient_education", AbiturientEducationForm),
        ("abiturient_misc", AbiturientMiscInformationForm),
        ("offer", UniversityOfferSearchForm),
        ("accepted_offer", AcceptedOfferForm),
        ("abiturient_parents", AbiturientParentsForm),
        ("abiturient_sensitive", AbiturientSensitiveInformationForm),
        ("representative_contact", RepresentativeContactForm),
        ("representative_sensitive", RepresentativeSensitiveInformationForm),
        ("check", EmptyForm),
    ]

    def should_be_parent(self) -> bool:
        abiturient_birth: dict | None = self.get_cleaned_data_for_step(
            "abiturient_birth"
        )
        if not abiturient_birth:
            return True

        return date.today() - abiturient_birth["birth_date"] < timedelta(
            days=365.25 * 18
        )

    condition_dict = {
        "abiturient_basic": lambda _: True,
        "abiturient_birth": lambda _: True,
        "abiturient_education": lambda _: True,
        "abiturient_misc": lambda _: True,
        "offer": lambda _: True,
        "accepted_offer": lambda _: True,
        "abiturient_parents": lambda _: True,
        "abiturient_sensitive": lambda _: True,
        "representative_contact": should_be_parent,
        "representative_sensitive": should_be_parent,
        "check": lambda _: True,
    }

    def get_template_names(self) -> list[str]:
        return [f"abiturient_form/wizard_steps/{self.steps.current}.html"]

    def get_form_initial(self, step):
        if step == "accepted_offer":
            offer_step = self.get_cleaned_data_for_step("offer")
            offer = offer_step["result_offer"]
            res = super().get_form_initial(step)
            res["offer"] = offer
            return res

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == "accepted_offer":
            context.update(
                {
                    "chosen_contract_offer": self.get_cleaned_data_for_step("offer")[
                        "result_offer"
                    ].type
                    == UniversityOffer.Type.CONTRACT
                }
            )
        elif self.steps.current == "check":
            context.update(
                {k: self.get_cleaned_data_for_step(k) for k in form_list_str[:7]}
            )

            if self.should_be_parent():
                context["has_18_years"] = False
                context.update(
                    {
                        "representative_contact": self.get_cleaned_data_for_step(
                            "representative_contact"
                        ),
                        "representative_sensitive": self.get_cleaned_data_for_step(
                            "representative_sensitive"
                        ),
                    }
                )
            else:
                context["has_18_years"] = True

        return context

    def done(self, form_list, **kwargs):
        """
        # That's easier.
        # And don't forget about empty check form.
        if len(form_list) == 5:
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
        """

        abiturient_basic: AbiturientBasicInformationForm = form_list[0]
        abiturient_birth: AbiturientBirthInformationForm = form_list[1]
        abiturient_education: AbiturientEducationForm = form_list[2]
        abiturient_misc: AbiturientBirthInformationForm = form_list[3]
        offer: UniversityOfferSearchForm = form_list[4]
        accepted_offer: AcceptedOfferForm = form_list[5]
        abiturient_parents: AbiturientParentsForm = form_list[6]
        abiturient_sensitive: AbiturientSensitiveInformationForm = form_list[7]

        if len(form_list) > 9:
            representative_contact: RepresentativeContactForm = form_list[8]
            representative_sensitive: RepresentativeSensitiveInformationForm = (
                form_list[9]
            )
        else:
            representative_contact = None
            representative_sensitive = None

        abiturient = Abiturient(
            contact_information=ContactInformation.objects.create(
                last_name=abiturient_basic.cleaned_data["last_name"],
                first_name=abiturient_basic.cleaned_data["first_name"],
                patronymic=abiturient_basic.cleaned_data["patronymic"],
                phone_number=abiturient_basic.cleaned_data["phone_number"],
            ),
            birth_date=abiturient_birth.cleaned_data["birth_date"],
            birth_country=abiturient_birth.cleaned_data["birth_country"],
            birth_town=abiturient_birth.cleaned_data["birth_town"],
            nationality=abiturient_birth.cleaned_data["nationality"],
            foreign_language=abiturient_birth.cleaned_data["foreign_language"],
            education_institution=abiturient_education.cleaned_data[
                "education_institution"
            ],
            education_place=abiturient_education.cleaned_data["education_place"],
            education_end=abiturient_education.cleaned_data["education_end"],
            work=abiturient_misc.cleaned_data["work"],
            martial_status=abiturient_misc.cleaned_data["martial_status"],
            living_address=abiturient_misc.cleaned_data["living_address"],
            registered_address=abiturient_misc.cleaned_data["registered_address"],
            mother_contact_information=ContactInformation.objects.create(
                last_name=abiturient_parents.cleaned_data["mother_last_name"],
                first_name=abiturient_parents.cleaned_data["mother_first_name"],
                patronymic=abiturient_parents.cleaned_data["mother_patronymic"],
                phone_number=abiturient_parents.cleaned_data["mother_phone"],
            ),
            father_contact_information=ContactInformation.objects.create(
                last_name=abiturient_parents.cleaned_data["father_last_name"],
                first_name=abiturient_parents.cleaned_data["father_first_name"],
                patronymic=abiturient_parents.cleaned_data["father_patronymic"],
                phone_number=abiturient_parents.cleaned_data["father_phone"],
            ),
            sensitive_information=SensitiveInformation.objects.create(
                passport_serie=abiturient_sensitive.cleaned_data["passport_serie"],
                passport_number=abiturient_sensitive.cleaned_data["passport_number"],
                passport_authority=abiturient_sensitive.cleaned_data[
                    "passport_authority"
                ],
                passport_issue_date=abiturient_sensitive.cleaned_data[
                    "passport_issue_date"
                ],
                rntrc=abiturient_sensitive.cleaned_data["rntrc"],
            ),
        )

        if representative_contact is not None and representative_sensitive is not None:
            abiturient.representative = AbiturientRepresentative(
                contact_information=ContactInformation(
                    last_name=representative_contact.cleaned_data["last_name"],
                    first_name=representative_contact.cleaned_data["first_name"],
                    patronymic=representative_contact.cleaned_data["patronymic"],
                    phone_number=representative_contact.cleaned_data["phone_number"],
                ),
                living_address=representative_sensitive.cleaned_data["living_address"],
                sensitive_information=SensitiveInformation(
                    passport_serie=representative_sensitive.cleaned_data[
                        "passport_serie"
                    ],
                    passport_number=representative_sensitive.cleaned_data[
                        "passport_number"
                    ],
                    passport_authority=representative_sensitive.cleaned_data[
                        "passport_authority"
                    ],
                    passport_issue_date=representative_sensitive.cleaned_data[
                        "passport_issue_date"
                    ],
                    rntrc=representative_sensitive.cleaned_data["rntrc"],
                ),
            )

        abiturient.save()

        AcceptedOffer.objects.create(
            offer=offer.cleaned_data["result_offer"],
            abiturient=abiturient,
            created_at=datetime.today(),
            payment_frequency=accepted_offer.cleaned_data["payment_frequency"],
            accepted_year=accepted_offer.cleaned_data["accepted_year"],
        )

        return HttpResponseRedirect(reverse("done"))
