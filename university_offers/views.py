import json
from typing import List
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from university_offers.models import Speciality, UniversityOffer


def offers_json(request: HttpRequest) -> HttpResponse:
    offers = UniversityOffer.objects.filter(
        basis=request.GET.get("basis"),
        type=request.GET.get("offer_type"),
        study_form=request.GET.get("study_form"),
        level=request.GET.get("level"),
    )

    if speciality_id := request.GET.get("speciality"):
        speciality = Speciality.objects.get(id=speciality_id)
        offers = offers.filter(educational_program__speciality__code=speciality.code)

    return JsonResponse([offer.id for offer in offers], safe=False)


def offers_json_to_html(request: HttpRequest) -> HttpResponse:
    offers = [
        UniversityOffer.objects.get(pk=str(id)) for id in json.loads(request.body)
    ]
    context = {"offers": offers}
    return render(request, "university_offers/ajax/offers.html", context)
