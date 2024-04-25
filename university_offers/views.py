from typing import List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from university_offers.models import Speciality, UniversityOffer


def ajax_offers(request: HttpRequest) -> HttpResponse:
    offers = UniversityOffer.objects.filter(
        basis=request.GET.get("basis"),
        type=request.GET.get("offer_type"),
        study_form=request.GET.get("study_form"),
        level=request.GET.get("level"),
    )

    if faculty := request.GET.get("faculty"):
        offers = offers.filter(faculty=faculty)

    if speciality_id := request.GET.get("speciality"):
        speciality = Speciality.objects.get(id=speciality_id)
        offers = offers.filter(
            educational_program__speciality__code=speciality.code,
            educational_program__speciality__specialization=speciality.specialization,
        )

    if educational_program_name := request.GET.get("educational_program_name"):

        def rank(offer: UniversityOffer) -> int:
            from thefuzz import fuzz

            return fuzz.partial_ratio(
                educational_program_name, offer.educational_program.name
            )

        q = sorted(q, key=rank, reverse=True)

    context = {"offers": offers}
    return render(request, "university_offers/ajax/offers.html", context)
