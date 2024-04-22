from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from accepting_offers.models import AcceptedOffer
from documents.generation import generate_document_response
from documents.models import Document


def must_be_pk(fn):
    def res_fn(request: HttpRequest):
        if not request.user.groups.filter(name="pk").exists():
            return render(request, "pk_panel/unauthorized.html")

        return fn(request)

    return res_fn


@must_be_pk
def main(request: HttpRequest):
    accepted_offers = AcceptedOffer.objects.filter(
        offer__speciality__faculty=request.user.faculty
    )

    if query := request.GET.get("query"):
        """
        query_words = query.lower().split()

        def rank(offer: AcceptedOffer) -> int:
            offer_words = str(offer).lower().split()
            count = 0
            for query_word in query_words:
                if any(query_word in elem for elem in offer_words):
                    count -= 1

            return count

        accepted_offers = sorted(accepted_offers, key=rank)

        accepted_offers = SearchQuerySet().models(AcceptedOffer).filter(content=query)
        """

        def rank(offer: AcceptedOffer) -> int:
            from thefuzz import fuzz

            return fuzz.partial_ratio(query, str(offer))

        accepted_offers = sorted(accepted_offers, key=rank, reverse=True)

    documents = Document.objects.all()
    context = {"offers": accepted_offers, "documents": documents}
    return render(request, "pk_panel/main.html", context)


@must_be_pk
def gen_doc(request: HttpRequest):
    offer_id = request.GET.get("offer_id")
    doc_id = request.GET.get("doc_id")
    if not offer_id:
        return HttpResponseBadRequest("offer_id is required")
    elif not doc_id:
        return HttpResponseBadRequest("doc_id is required")

    offer = AcceptedOffer.objects.get(id=offer_id)
    doc = Document.objects.get(id=doc_id)

    return generate_document_response(offer, doc)
