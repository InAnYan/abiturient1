from typing import Iterable, List
from django import template

from documents.models import Document
from university_offers.models import UniversityOffer

register = template.Library()


@register.filter
def lowerfirst(value):
    """
    Lowercases the first letter of a string.
    """
    if not value:
        return value
    return value[0].lower() + value[1:]


@register.filter
def filter_documents(
    docs: Iterable[Document], offer: UniversityOffer
) -> Iterable[Document]:
    res = []

    for doc in docs:
        if doc.only_for_contract and offer.type != UniversityOffer.Type.CONTRACT:
            continue
        if doc.only_for_full_time and offer.study_form != UniversityOffer.StudyForm.DAY:
            continue
        res.append(doc)

    return res
