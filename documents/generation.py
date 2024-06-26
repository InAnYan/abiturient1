from datetime import datetime
from io import BytesIO
import re
from tkinter import W
from typing import Optional
from urllib.request import urlopen

from django.http import HttpResponse

from docx.shared import Cm
from abiturients.models import Abiturient, AbiturientRepresentative
from accepting_offers.models import AcceptedOffer
from documents.models import Document
from university_offers.models import UniversityOffer
from django.utils.translation import gettext_lazy as _

from docxtpl import DocxTemplate, InlineImage

from django.utils import formats


def generate_document(
    accepted_offer: AcceptedOffer,
    path: str,
    out,
    abiturient_sign_datauri: str,
    representative_sign_datauri: Optional[str],
):
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

    if not abiturient.passport_serie:
        abiturient.passport_serie = " " * 4

    if not abiturient.passport_number:
        abiturient.passport_number = "_" * 13  # type: ignore

    if not abiturient.passport_authority:
        abiturient.passport_authority = "_" * 63

    if not abiturient.rntrc:
        abiturient.rntrc = "_" * 13  # type: ignore

    if not abiturient.representative:
        abiturient.representative = AbiturientRepresentative(
            last_name="asd",
            first_name="asd",
            phone_number="+380123456789",
            email="a@a.com",
            living_address="asd",
        )

        representative = abiturient.representative

        representative.first_name = "_" * 7
        representative.last_name = "_" * 7
        representative.patronymic = "_" * 7
        representative.living_address = "_" * 31

        representative.phone_number = "_" * 13
        representative.email = "_" * 17

    assert representative

    if not representative.passport_serie:
        representative.passport_serie = " " * 4

    if not representative.passport_number:
        representative.passport_number = "_" * 13  # type: ignore

    if not representative.passport_authority:
        representative.passport_authority = "_" * 63

    if not representative.rntrc:
        representative.rntrc = "_" * 13  # type: ignore

    doc = DocxTemplate(path)

    with urlopen(abiturient_sign_datauri) as f:
        abiturient_sign = InlineImage(doc, BytesIO(f.read()), width=Cm(3))

    if representative_sign_datauri:
        with urlopen(representative_sign_datauri) as f:
            representative_sign = InlineImage(doc, BytesIO(f.read()), width=Cm(3))
    else:
        representative_sign = "_" * 12

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
        "abiturient_sign": abiturient_sign,
        "representative_sign": representative_sign,
    }
    doc.render(context)
    doc.save(out)


def generate_document_filename(
    accepted_offer: AcceptedOffer, doc_name: str | None = None
) -> str:
    # Please, forgive me for this function.
    # If you specify doc_name, you will generate a docx document
    # If doc_name is None, you will generate a zip

    abiturient = accepted_offer.abiturient

    now = datetime.now()
    formatted_now = formats.date_format(now, "SHORT_DATETIME_FORMAT")

    return (
        (doc_name + " " if doc_name else "")
        + abiturient.full_name
        + " "
        + formatted_now
        + (".docx" if doc_name else ".zip")
    ).replace(":", "_")


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

    filename = generate_document_filename(accepted_offer, doc.name)

    add_content_disposition_header(response, filename)

    generate_document(accepted_offer, doc.file.path, response)

    return response
