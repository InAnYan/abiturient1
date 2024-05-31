from datetime import datetime

from django.http import HttpResponse
from abiturients.models import Abiturient
from accepting_offers.models import AcceptedOffer
from documents.models import Document
from university_offers.models import EducationalLevel, UniversityOffer
from django.utils.translation import gettext_lazy as _

from docxtpl import DocxTemplate

from django.utils import formats


def generate_document(accepted_offer: AcceptedOffer, path: str, out):
    offer = accepted_offer.offer
    abiturient = accepted_offer.abiturient
    educational_program = offer.educational_program
    speciality = educational_program.speciality
    faculty = speciality.faculty
    representative = abiturient.representative

    """
    offer.study_form = UniversityOffer.StudyForm(offer.study_form).label
    offer.type = UniversityOffer.Type(offer.type).label
    offer.level = EducationalLevel(offer.level).label
    offer.basis = UniversityOffer.Basis(offer.basis).label

    abiturient.gender = Abiturient.Gender(abiturient.gender).label
    """

    doc = DocxTemplate(path)
    context = {
        "accepted_offer": accepted_offer,
        "offer": offer,
        "abiturient": abiturient,
        "speciality": speciality,
        "educational_program": educational_program,
        "faculty": faculty,
        "representative": representative,
        "Abiturient": Abiturient,
        "UniversityOffer": UniversityOffer,
    }
    doc.render(context)
    doc.save(out)


def generate_document_filename(accepted_offer: AcceptedOffer, doc: Document) -> str:
    abiturient = accepted_offer.abiturient

    now = datetime.now()
    formatted_now = formats.date_format(now, "SHORT_DATETIME_FORMAT")

    return doc.name + "_" + abiturient.full_name + "_" + formatted_now + '.docx"'


# Source: https://medium.com/@JeremyLaine/non-ascii-content-disposition-header-in-django-3a20acc05f0d
from urllib.parse import quote


def add_content_disposition_header(response, filename):
    """
    Add an RFC5987 / RFC6266 compliant Content-Disposition header to an
    HttpResponse to tell the browser to save the HTTP response to a file.
    """
    try:
        filename.encode("ascii")
        file_expr = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(filename))
    response["Content-Disposition"] = "attachment; {}".format(file_expr)
    return response


# --------------------------------------------------------------------------------------------------


def generate_document_response(accepted_offer: AcceptedOffer, doc: Document):
    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    )

    filename = generate_document_filename(accepted_offer, doc)

    add_content_disposition_header(response, filename)

    generate_document(accepted_offer, doc.file.path, response)

    return response
