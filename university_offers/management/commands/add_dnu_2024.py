import datetime
from typing import Any, Dict
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

import json


from abiturient1.settings import BASE_DIR
from university_offers.models import (
    Accreditation,
    EducationalLevel,
    EducationalProgram,
    Faculty,
    Speciality,
    UniversityOffer,
)


class Command(BaseCommand):
    help = _("Add educational programs, accreditations, and offers for DNU 2024")

    def handle(self, *args, **options):
        with open(
            BASE_DIR
            / "university_offers"
            / "management"
            / "commands"
            / "offers_3.json",
            encoding="utf-8",
        ) as fin:
            data = json.load(fin)

            for item in data:
                self.load(item)

    def load(self, item: Dict[str, Any]):
        faculty = self.load_faculty(item)
        speciality = self.load_speciality(item, faculty)
        program = self.load_program(item, speciality)

        self.load_accreditation(item, program)

        self.make_offer(item, program).save()

    def load_faculty(self, item: Dict[str, Any]) -> Faculty:
        res = list(Faculty.objects.filter(full_name=item["faculty"]))
        if len(res) != 1:
            print(res)
            raise Exception("something with faculty: " + item["faculty"])
        return res[0]

    def load_speciality(self, item: Dict[str, Any], faculty: Faculty) -> Speciality:
        q = Speciality.objects.filter(code=item["speciality_code"], faculty=faculty)

        if "specialization_code" in item:
            q = q.filter(specialization_code=item["specialization_code"])

        if q:
            return q.get()

        obj = Speciality(
            code=item["speciality_code"],
            name=(
                item["specialization_name"]
                if "specialization_name" in item
                else item["speciality_name"]
            ),
            faculty=faculty,
        )

        if "specialization_code" in item:
            obj.specialization_code = item["specialization_code"]

        obj.save()
        return obj

    def load_program(
        self, item: Dict[str, Any], speciality: Speciality
    ) -> EducationalProgram:
        q = EducationalProgram.objects.filter(
            speciality=speciality, name=item["educational_program_name"]
        )

        if q:
            return q.get()

        obj = EducationalProgram(
            speciality=speciality,
            name=item["educational_program_name"],
        )

        obj.save()
        return obj

    def load_accreditation(self, item: Dict[str, Any], program: EducationalProgram):
        if "accreditation_number" in item:
            q = Accreditation.objects.filter(
                educational_program=program,
                level=self.to_level(item["basis"]),
                end_date=self.to_date(item["accreditation_end"]),
                number=int(item["accreditation_number"]),
                type=self.to_acc_type(item["accreditation_type"]),
            )

            if "accreditation_serie" in item:
                q = q.filter(serie=item["accreditation_serie"])

            if q:
                return q.get()
            else:
                obj = Accreditation(
                    educational_program=program,
                    level=self.to_level(item["basis"]),
                    end_date=self.to_date(item["accreditation_end"]),
                    number=int(item["accreditation_number"]),
                    type=self.to_acc_type(item["accreditation_type"]),
                )

                if "accreditation_serie" in item:
                    obj.serie = item["accreditation_serie"]

                obj.save()

    def make_offer(self, item: Dict[str, Any], program: EducationalProgram):
        costs = [0, 0, 0, 0]

        for i in range(0, len(costs)):
            if f"year{i + 1}_cost" in item:
                costs[i] = item[f"year{i + 1}_cost"]

        return UniversityOffer.objects.create(
            study_begin=datetime.datetime.now(),
            study_duration=item["study_duration"],
            educational_program=program,
            level=self.to_level(item["basis"]),
            basis=self.to_basis(item["basis"]),
            type=self.to_offer_type(item["type"]),
            study_form=self.to_study_form(item["study_form"]),
            ects=0,
            year1_cost=costs[0],
            year2_cost=costs[1],
            year3_cost=costs[2],
            year4_cost=costs[3],
        )

    def to_level(self, basis: str) -> EducationalLevel:
        match basis:
            case "PZSO" | "NRK5":
                return EducationalLevel.BACHELOR
            case "NRK67":
                return EducationalLevel.MASTER
            case _:
                raise Exception("It can't be: " + basis)

    def to_date(self, text: str) -> datetime.date:
        return datetime.datetime.strptime(text, "%d.%m.%Y").date()

    def to_basis(self, text: str) -> UniversityOffer.Basis:
        match text:
            case "PZSO":
                return UniversityOffer.Basis.PZSO
            case "NRK5":
                return UniversityOffer.Basis.NRK_5
            case "NRK67":
                return UniversityOffer.Basis.NRK_6_7
            case _:
                raise Exception("It can't be: " + text)

    def to_offer_type(self, text: str) -> UniversityOffer.Type:
        match text:
            case "небюджетна":
                return UniversityOffer.Type.CONTRACT
            case "відкрита" | "фіксована":
                return UniversityOffer.Type.BUDGET
            case _:
                raise Exception("It can't be: " + text)

    def to_study_form(self, text: str) -> UniversityOffer.StudyForm:
        match text:
            case "DAY":
                return UniversityOffer.StudyForm.DAY
            case "OVER_DISTANCE":
                return UniversityOffer.StudyForm.OVER_DISTANCE
            case "DISTANCE":
                return UniversityOffer.StudyForm.DISTANCE
            case _:
                raise Exception("It can't be: " + text)

    def to_acc_type(self, text: str) -> Accreditation.Type:
        match text:
            case "educational_program":
                return Accreditation.Type.EDUCATIONAL_PROGRAM
            case "speciality":
                return Accreditation.Type.SPECIALITY
            case _:
                raise Exception("It can't be: " + text)
