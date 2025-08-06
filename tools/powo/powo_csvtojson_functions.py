import csv
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.join(script_dir, "../../input/powo")
raw = os.path.join(folder_path, "raw")
currated = os.path.join(folder_path, "currated")


def convert_csv_to_json_lines(csv_path, json_lines_path):
    with open(csv_path, encoding="utf-8") as f_in, open(
        json_lines_path, "w", encoding="utf-8"
    ) as f_out:
        reader = csv.DictReader(f_in, delimiter="|")
        for row in reader:
            f_out.write(json.dumps(row, ensure_ascii=False) + "\n")


def wcvpJson(csv_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for i in range(1, 16):
        csv_file = os.path.join(csv_folder, f"partie_{i}.csv")
        json_lines_file = os.path.join(output_folder, f"powo_taxonomy_{i}.json")

        if os.path.exists(csv_file):
            print(f"✅ Traitement de {csv_file} → {json_lines_file}")
            convert_csv_to_json_lines(csv_file, json_lines_file)
        else:
            print(f"⚠️ Fichier introuvable : {csv_file}")
