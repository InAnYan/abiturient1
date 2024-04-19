from datetime import datetime
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from accepting_offers.admin import add_content_disposition_header
from accepting_offers.models import AcceptedOffer
from documents.generation import generate_document_response
from documents.models import Document

from docxtpl import DocxTemplate

from university_offers.models import UniversityOffer


def must_be_pk(fn):
    def res_fn(request: HttpRequest):
        if not request.user.groups.filter(name="pk").exists():
            return HttpResponseForbidden(_("pk_panel.must_be_pk"))

        return fn(request)

    return res_fn


@must_be_pk
def main(request: HttpRequest):
    accepted_offers = AcceptedOffer.objects.all()
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
