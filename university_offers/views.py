from typing import List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from university_offers.models import Speciality, UniversityOffer


def filter_objects_by_request(request: HttpRequest, values: str):
    dict = {value: request.GET.get(value) for value in values}
    if any(map(lambda pair: pair[1], dict.items())):  # TODO: Appears not to work.
        return UniversityOffer.objects.filter(**dict)
    else:
        return UniversityOffer.objects.none()


def filter_fields(data, field: str):
    return data.values_list(field, flat=True).distinct()


def filter_choices(data, type):
    return [(int(type(value)), type(value).label) for value in data]


def make_abstract_view(template, fn):
    def view(request: HttpRequest):
        context = {"list": fn(request)}
        return render(request, template, context)

    return view


def make_objects_view(values: List[str]):
    return make_abstract_view(
        "university_offers/ajax/objects.html",
        lambda request: filter_objects_by_request(request, values),
    )


def make_choices_view(values: List[str], field: str, type):
    return make_abstract_view(
        "university_offers/ajax/int_choices.html",
        lambda request: filter_choices(
            filter_fields(filter_objects_by_request(request, values), field), type
        ),
    )


ajax_bases = make_choices_view(["speciality"], "basis", UniversityOffer.Basis)

ajax_levels = make_choices_view(["speciality", "basis"], "level", UniversityOffer.Level)

ajax_study_forms = make_choices_view(
    ["speciality", "basis", "level"], "study_form", UniversityOffer.StudyForm
)

ajax_offer_types = make_choices_view(
    ["speciality", "basis", "level", "study_form"], "type", UniversityOffer.Type
)


def ajax_offer_info(request: HttpRequest):
    offer = list(
        filter_objects_by_request(request, ["speciality", "study_form", "type"])
    )

    if offer:
        context = {"offer": offer[0]}

        return render(request, "university_offers/ajax/offer_info.html", context)
    else:
        return HttpResponse("<p>No information</p>")
