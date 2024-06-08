import glob
import json
from re import T

with open("offers_1.json", encoding="utf-8") as f_acc:
    with open("prices_1.json", encoding="utf-8") as f_prices:
        with open("offers_2.json", "w", encoding="utf-8") as fout_offers:
            with open("prices_2.json", "w", encoding="utf-8") as fout_prices:
                acc_data = json.load(f_acc)
                prices_data = json.load(f_prices)
                global_to_add = []

                for entry in prices_data:
                    found = []
                    for finding in acc_data:
                        if all(
                            finding[x] == entry[x]
                            for x in [
                                "faculty",
                                "study_form",
                                "educational_program_name",
                                "speciality_code",
                                "speciality_name",
                                "basis",
                            ]
                        ):
                            if "specialization_code" in entry:
                                if all(
                                    finding[x] == entry[x]
                                    for x in [
                                        "specialization_code",
                                        "specialization_name",
                                    ]
                                ):
                                    found.append(finding)
                            else:
                                found.append(finding)

                    if len(found) == 1 or (
                        len(found) == 2
                        and found[0]["study_duration"] != found[1]["study_duration"]
                    ):
                        to_add = []
                        for found_one in found:
                            new_entry = dict(entry)

                            new_entry["study_duration"] = found_one["study_duration"]

                            for field in ["number", "type", "serie", "end"]:
                                if f"accreditation_{field}" in found_one:
                                    new_entry[f"accreditation_{field}"] = found_one[
                                        f"accreditation_{field}"
                                    ]

                            to_add.append(new_entry)

                        global_to_add += to_add

                    else:
                        print("ERROR: ", entry)
                        print("found: ", found)
                        exit(1)

                for entry in global_to_add:
                    entry["type"] = "небюджетна"

                acc_data += global_to_add

                json.dump(acc_data, fout_offers, ensure_ascii=False)
