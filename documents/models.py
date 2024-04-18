from datetime import date, datetime, timedelta
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import jinja2

from persons.models import Person
from accepting_offers.models import AcceptedOffer
from university_offers.models import Faculty, Speciality, UniversityOffer

from docxtpl import DocxTemplate

from tempfile import NamedTemporaryFile


only_alpha_space_validator = RegexValidator("([^\W]| )+", _("generic.only_alpha"))


class Document(models.Model):
    name = models.CharField(max_length=255, validators=[only_alpha_space_validator])
    file = models.FileField(upload_to="documents")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("document.plural")

    def clean(self):
        super().clean()

        test_parent = Person(
            last_name="ParentTest",
            first_name="ParentTest",
            patronymic="ParentTest",
            phone=1111111111,
            email="Parenta@a.com",
            living_address="Parentasd",
            passport_serie="AE",
            passport_number=123456789,
            passport_who_give=1234,
            passport_when_given=datetime.today() - timedelta(days=5),
            inn=123456789123,
        )

        test_abiturient = Person(
            last_name="Test",
            first_name="Test",
            patronymic="Test",
            phone=1111111111,
            email="a@a.com",
            living_address="asd",
            passport_serie="AE",
            passport_number=123456789,
            passport_who_give=1234,
            passport_when_given=datetime.today() - timedelta(days=5),
            inn=123456789123,
            parent=test_parent,
        )

        test_faculty = Faculty(
            full_name="Test",
            abbreviation="Test",
            cipher=1,
        )

        test_speciality = Speciality(
            name="Test",
            code=1,
            specialization=1,
            faculty=test_faculty,
            educational_program_name="asd",
        )

        test_offer = UniversityOffer(
            study_begin=date.today(),
            study_duration=311,
            speciality=test_speciality,
            type=UniversityOffer.Type.CONTRACT,
            study_form=UniversityOffer.StudyForm.DAY,
            ects=60,
        )

        test_object = AcceptedOffer(
            abiturient=test_abiturient,
            offer=test_offer,
            created_at=date.today(),
            payment_type=AcceptedOffer.PaymentType.PRIVATE,
            payment_frequency=AcceptedOffer.PaymentFrequency.EVERY_SEMESTER,
            accepted_year=1,
        )

        try:
            template_file = NamedTemporaryFile(delete=False, suffix=".docx")
            template_file.write(self.file.file.file.read())
            template_file.close()

            filled_file = NamedTemporaryFile(delete=False, suffix=".docx")
            fill_document_for_offer(str(template_file.name), test_object, filled_file)

            filled_file.close()

            import os

            os.unlink(template_file.name)
            os.unlink(filled_file.name)

        except Exception as e:
            raise ValidationError("Got an error: " + str(e))


def fill_document_for_offer(document_path: str, offer: AcceptedOffer, out):
    offer.offer.study_form = UniversityOffer.StudyForm(offer.offer.study_form).label
    offer.offer.type = UniversityOffer.Type(offer.offer.type).label
    doc_templ = DocxTemplate(document_path)
    context = {"offer": offer}
    doc_templ.render(context, jinja2.Environment(undefined=jinja2.StrictUndefined))
    doc_templ.save(out)
