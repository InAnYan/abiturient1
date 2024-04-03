from django.http import HttpRequest
from django.shortcuts import render

from university_offers.models import Speciality, UniversityOffer


def ajax_specialities(request: HttpRequest):
    faculty = 0

    for key, value in request.GET.items():
        if key.endswith("faculty") and value:
            faculty = int(value)

    context = {"list": Speciality.objects.filter(faculty=faculty)}

    return render(request, "university_offers/ajax/main.html", context)


def ajax_study_forms(request: HttpRequest):
    speciality = None

    for key, value in request.GET.items():
        if key.endswith("speciality") and value:
            speciality = int(value)

    context = {
        "list": (
            [
                UniversityOffer.StudyForm(value).label
                for value in UniversityOffer.objects.filter(speciality=speciality)
                .values_list("study_form", flat=True)
                .distinct()
            ]
            if speciality is not None
            else []
        )
    }

    return render(request, "university_offers/ajax/main.html", context)


def ajax_offer_types(request: HttpRequest):
    speciality = None
    study_form = None

    for key, value in request.GET.items():
        if key.endswith("speciality") and value:
            speciality = int(value)
        elif key.endswith("study_form") and value:
            study_form = int(value)

    context = {
        "list": (
            [
                UniversityOffer.Type(value).label
                for value in UniversityOffer.objects.filter(
                    speciality=speciality, study_form=study_form
                )
                .values_list("type", flat=True)
                .distinct()
            ]
            if speciality is not None and study_form is not None
            else []
        )
    }

    return render(request, "university_offers/ajax/main.html", context)
