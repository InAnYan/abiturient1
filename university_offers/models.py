from django.db import models
from django.core.validators import MinValueValidator


# Факультет.
class Faculty(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=255, unique=True)
    cipher = models.IntegerField(validators=[MinValueValidator(1)], unique=True)

    def __str__(self) -> str:
        return self.full_name


# Спеціальність.
class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.IntegerField(validators=[MinValueValidator(1)])
    specialization = models.IntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    end_of_accreditation = models.DateField(null=True, blank=True)  # TODO: ???
    educational_program_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        code = str(self.code).zfill(3)
        if self.specialization:
            code += "." + str(self.specialization).zfill(3)

        return self.faculty.abbreviation + " - " + code + " " + self.name


# Конкурсна пропозиція.
class UniversityOffer(models.Model):
    class Type(models.IntegerChoices):
        BUDGET = 1, "Бюджет"
        CONTRACT = 2, "Контракт"

    class StudyForm(models.IntegerChoices):
        DAY = 1, "Денна"
        DISTANCE = 2, "Заочна"
        EVENING = 3, "Вечірня"

    study_begin = models.DateField()
    study_duration = models.IntegerField(validators=[MinValueValidator(1)])
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    type = models.PositiveIntegerField(choices=Type.choices)
    study_form = models.PositiveIntegerField(choices=StudyForm.choices)
    ects = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return (
            str(self.speciality)
            + " - "
            + self.StudyForm(self.study_form).label
            + " - "
            + self.Type(self.type).label
        )
