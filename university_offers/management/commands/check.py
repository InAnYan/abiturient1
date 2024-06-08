import json

with open("offers_3.json", encoding="utf-8") as fin:
    data = json.load(fin)

    for entry in data:
        if entry["type"] == "небюджетна":
            for i in range(1, entry["study_duration"] // 12 + 1):
                if f"year{i}_cost" not in entry:
                    print("ERROR: ", entry)
                    exit(1)
        else:
            for i in range(1, 5):
                if f"year{i}_cost" in entry:
                    print("ERROR: ", entry)
                    exit(1)
