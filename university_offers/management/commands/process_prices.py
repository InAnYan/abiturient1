import code
import json

with open("prices.json", encoding="utf-8") as fin:
    with open("prices_processed.json", "w", encoding="utf-8") as fout:
        data = json.load(fin)

        for entry in data:
            entry: dict[str, str]

            full: str = entry["specialization"]
            del entry["specialization"]

            if (slash := full.find("/")) != -1:
                code_and_speciality = full[:slash].strip()
                code_and_specialization = full[slash + 1 :].strip()
            elif (parent := full.find("(")) != -1:
                code_and_speciality = full[:parent].strip()
                code_and_specialization = full[parent + 1 : -1].strip()
            else:
                code_and_speciality = full
                code_and_specialization = None

            space = code_and_speciality.find(" ")
            assert space != -1

            speciality_code = code_and_speciality[:space]
            speciality_name = code_and_speciality[space + 1 :]

            entry["speciality_code"] = int(speciality_code)
            entry["speciality_name"] = speciality_name

            if code_and_specialization:
                if code_and_specialization.find(".") == -1:
                    specialization_code = None
                    specialization_name = f"Середня освіта {code_and_specialization}"
                else:
                    _, code_and_specialization = code_and_specialization.split(".")

                    space = code_and_specialization.find(" ")
                    specialization_code = code_and_specialization[:space]
                    specialization_name = code_and_specialization[space + 1 :]

                if specialization_code:
                    entry["specialization_code"] = int(specialization_code.strip())
                entry["specialization_name"] = specialization_name.strip()

            for i in range(1, 5):
                if f"year{i}_cost" in entry:
                    entry[f"year{i}_cost"] = int(
                        entry[f"year{i}_cost"].replace(" ", "")
                    )

            for i in range(1, 4):
                if f"semester{i}_cost" in entry:
                    entry[f"semester{i}_cost"] = int(
                        entry[f"semester{i}_cost"].replace(" ", "")
                    )

            if "semester1_cost" in entry:
                entry["year1_cost"] = entry["semester1_cost"] + entry["semester2_cost"]
                entry["year2_cost"] = entry["semester3_cost"]
                for i in range(1, 4):
                    del entry[f"semester{i}_cost"]

        json.dump(data, fout, ensure_ascii=False)
