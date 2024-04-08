from django.http import HttpRequest
from django.shortcuts import render

from university_offers.models import Speciality, UniversityOffer


def ajax_specialities(request: HttpRequest):
    faculty = request.GET.get("faculty")

    context = {"list": Speciality.objects.filter(faculty=faculty) if faculty else []}

    return render(request, "university_offers/ajax/objects.html", context)


def ajax_study_forms(request: HttpRequest):
    speciality = request.GET.get("speciality")

    context = {
        "list": (
            [
                (
                    int(UniversityOffer.StudyForm(value)),
                    UniversityOffer.StudyForm(value).label,
                )
                for value in UniversityOffer.objects.filter(speciality=speciality)
                .values_list("study_form", flat=True)
                .distinct()
            ]
            if speciality
            else []
        )
    }

    return render(request, "university_offers/ajax/int_choices.html", context)


def ajax_offer_types(request: HttpRequest):
    speciality = request.GET.get("speciality")
    study_form = request.GET.get("study_form")

    context = {
        "list": (
            [
                (
                    int(UniversityOffer.Type(value)),
                    UniversityOffer.Type(value).label,
                )
                for value in UniversityOffer.objects.filter(
                    speciality=speciality, study_form=study_form
                )
                .values_list("type", flat=True)
                .distinct()
            ]
            if speciality and study_form
            else []
        )
    }

    return render(request, "university_offers/ajax/int_choices.html", context)


def ajax_offer_info(request: HttpRequest):
    speciality = request.GET.get("speciality")
    study_form = request.GET.get("study_form")
    type = request.GET.get("type")

    offer = UniversityOffer.objects.get(
        speciality=speciality, study_form=study_form, type=type
    )

    context = {"offer": offer}

    return render(request, "university_offers/ajax/offer_info.html", context)
