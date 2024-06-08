import json

with open("accreditations_offers_joined.json", encoding="utf-8") as f_acc:
    with open("prices_processed.json", encoding="utf-8") as f_prices:
        with open("offers_1.json", "w", encoding="utf-8") as fout_offers:
            with open("prices_1.json", "w", encoding="utf-8") as fout_prices:
                acc_data = json.load(f_acc)
                prices_data = json.load(f_prices)

                to_delete = []

                for entry in acc_data:
                    entry: dict[str, str]

                    if entry["type"] == "небюджетна":
                        found = []
                        for finding in prices_data:
                            if (
                                finding["faculty"] == entry["faculty"]
                                and finding["study_form"] == entry["study_form"]
                                and finding["basis"] == entry["basis"]
                                and finding["speciality_name"]
                                == entry["speciality_name"]
                                and finding["speciality_code"]
                                == entry["speciality_code"]
                                and finding["educational_program_name"]
                                == entry["educational_program_name"]
                            ):
                                found.append(finding)

                        if len(found) != 1:
                            print("ERROR")
                            print(found)
                            print(entry)
                            exit(1)

                        found = found[0]
                        to_delete.append(found)

                        if entry["basis"] == "NRK5":
                            for i in range(1, entry["study_duration"] // 12 + 1):
                                entry[f"year{i}_cost"] = found[f"year1_cost"]

                        else:
                            for i in range(1, 5):
                                if f"year{i}_cost" in found:
                                    entry[f"year{i}_cost"] = found[f"year{i}_cost"]

                prices_data: list
                prices_data = [item for item in prices_data if item not in to_delete]

                json.dump(prices_data, fout_prices, ensure_ascii=False)
                json.dump(acc_data, fout_offers, ensure_ascii=False)
