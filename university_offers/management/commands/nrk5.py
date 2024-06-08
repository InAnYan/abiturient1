import json

with open("offers_2.json", encoding="utf-8") as fin:
    with open("offers_3.json", "w", encoding="utf-8") as fout:
        data = json.load(fin)

        for entry in data:
            if entry["type"] == "небюджетна" and entry["basis"] == "NRK5":
                cost = entry["year1_cost"]
                for i in range(1, entry["study_duration"] // 12 + 1):
                    entry[f"year{i}_cost"] = cost

        json.dump(data, fout, ensure_ascii=False)
