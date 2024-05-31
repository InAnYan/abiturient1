from datetime import date, datetime
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from abiturients.models import (
    Abiturient,
    AbiturientRepresentative,
)
from accepting_offers.models import AcceptedOffer
from university_offers.models import (
    Accreditation,
    EducationalLevel,
    EducationalProgram,
    Faculty,
    Speciality,
    UniversityOffer,
)

from tempfile import NamedTemporaryFile


only_alpha_space_validator = RegexValidator(
    "([^\W]| )+", _("Only alphabetical characters are allowed")
)


class Document(models.Model):
    name = models.CharField(
        max_length=255, validators=[only_alpha_space_validator], verbose_name=_("Name")
    )
    file = models.FileField(upload_to="documents", verbose_name=_("File"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def clean(self):
        super().clean()

        test_representative = AbiturientRepresentative(
            last_name="Test",
            first_name="Test",
            patronymic="Test",
            phone_number="+380123456789",
            living_address="Somewhere",
            passport_serie="Test",
            passport_number=123456,
            passport_authority="Test",
            passport_issue_date=date.today(),
            rntrc=123456789,
        )

        test_representative.save()

        test_abiturient = Abiturient(
            last_name="Test",
            first_name="Test",
            patronymic="Test",
            phone_number="+380123456789",
            birth_date=date.today(),
            birth_country="Test",
            birth_town="Test",
            nationality="Test",
            gender=Abiturient.Gender.MALE,
            education_institution="Test",
            education_place="Test",
            education_end=date.today(),
            work="Test",
            martial_status=Abiturient.MartialStatus.SINGLE,
            foreign_language="Test",
            email="Test",
            living_address="Test",
            registered_address="Test",
            mother_last_name="Test",
            mother_first_name="Test",
            mother_patronymic="Test",
            mother_phone_number="+380123456789",
            father_last_name="Test",
            father_first_name="Test",
            father_patronymic="Test",
            father_phone_number="+380123456789",
            passport_serie="Test",
            passport_number=123456,
            passport_authority="Test",
            passport_issue_date=date.today(),
            rntrc=123456789,
            representative=test_representative,
        )

        test_abiturient.save()

        test_faculty = Faculty(
            full_name="Test",
            abbreviation="Test",
        )

        test_faculty.save()

        test_speciality = Speciality(
            name="Test",
            code=1,
            faculty=test_faculty,
        )

        test_speciality.save()

        test_program = EducationalProgram(name="Test", speciality=test_speciality)

        test_program.save()

        test_accreditation = Accreditation(
            educational_program=test_program,
            level=EducationalLevel.BACHELOR,
            end_date=datetime.today(),
            number=213,
            type=Accreditation.Type.EDUCATIONAL_PROGRAM,
        )

        test_accreditation.save()

        test_offer = UniversityOffer(
            study_begin=date.today(),
            study_duration=311,
            educational_program=test_program,
            type=UniversityOffer.Type.CONTRACT,
            study_form=UniversityOffer.StudyForm.DAY,
            ects=60,
            level=EducationalLevel.BACHELOR,
            basis=UniversityOffer.Basis.PZSO,
        )

        test_offer.save()

        test_object = AcceptedOffer(
            abiturient=test_abiturient,
            offer=test_offer,
            created_at=date.today(),
            payment_frequency=AcceptedOffer.PaymentFrequency.EACH_SEMESTER,
            accepted_year=1,
        )

        test_object.save()

        try:
            template_file = NamedTemporaryFile(delete=False, suffix=".docx")
            template_file.write(self.file.file.file.read())
            template_file.close()

            filled_file = NamedTemporaryFile(delete=False, suffix=".docx")

            from documents.generation import generate_document

            generate_document(test_object, template_file.name, filled_file)

            filled_file.close()

            import os

            os.unlink(template_file.name)
            os.unlink(filled_file.name)

        except Exception as e:
            raise ValidationError(e)

        finally:
            test_object.delete()
            test_offer.delete()
            test_accreditation.delete()
            test_program.delete()
            test_speciality.delete()
            test_faculty.delete()
            test_abiturient.delete()
            test_representative.delete()
