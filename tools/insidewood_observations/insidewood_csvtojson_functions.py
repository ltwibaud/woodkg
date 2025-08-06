import json
import os
import re
import csv

folder_path = "../../input/insidewood_observations"
input_dir = folder_path + "/raw"
export_dir = folder_path + "/currated"


def convert_first_tsv_in_insidewood():

    # Liste les fichiers .tsv
    tsv_files = [f for f in os.listdir(input_dir) if f.endswith(".tsv")]

    if not tsv_files:
        print("❌ Aucun fichier .tsv trouvé dans le dossier InsideWood_import.")
        return None

    # Prend le premier fichier
    filename = tsv_files[0]
    tsv_file_path = os.path.join(input_dir, filename)

    # Génére un chemin de sortie dans le dossier courant
    json_file_name = os.path.splitext(filename)[0] + ".json"
    json_file_path = os.path.join(os.getcwd(), json_file_name)

    # Convertit
    data = []
    with open(tsv_file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            data.append(row)

    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier converti : {json_file_path}")
    return json_file_path


import json
import os


def remove_fossil_hardwood(input_file, output_file=None):
    # Charger les données JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Garder uniquement les objets où "Type of Wood" n'est pas "Fossil Hardwood"
    filtered_data = [
        item for item in data if item.get("Type of Wood") != "Fossil Hardwood"
    ]

    # Nom du fichier de sortie
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_no_fossil{ext}"

    # Écriture dans le fichier de sortie
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(
        f"✅ {len(data) - len(filtered_data)} lignes supprimées (Fossil Hardwood). Fichier : {output_file}"
    )
    return output_file


def rename_json_keys(input_file, output_file=None):
    def clean_key(key):
        # Supprime les "MH"/"mh" dans les clés de type "1MH", "23mh", etc.
        return re.sub(r"(\d+)[Mm][Hh]", r"\1", key)

    # Charge le fichier JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Applique le renommage des clés
    new_data = []
    for item in data:
        new_item = {clean_key(k): v for k, v in item.items()}
        new_data.append(new_item)

    # Génère un nom de fichier si non fourni
    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}_without_mh.json"

    # Sauvegarde le JSON modifié
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Clés renommées sauvegardées dans '{output_file}'")
    return output_file


def filter_json_by_key_number(input_file, output_file=None, max_number=221):
    def get_number(key):
        match = re.match(r"^(\d+)", key)
        return int(match.group(1)) if match else None

    # Lecture du fichier JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filtrage
    filtered_data = []
    for item in data:
        new_item = {}
        for key, value in item.items():
            num = get_number(key)
            if num is None or num <= max_number:
                new_item[key] = value
        filtered_data.append(new_item)

    # Génération automatique du nom de sortie si besoin
    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = base + "_filtré.json"

    # Sauvegarde
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Fichier filtré sauvegardé dans '{output_file}'")
    return output_file


def extract_taxa_and_numeric_keys(input_file, output_file=None):
    """
    Extracts only the 'Taxa' key and all keys that start with a number.

    Args:
        input_file (str): path to the input JSON file
        output_file (str, optional): path to the output JSON file.
                                     If None, creates one with suffix '_taxa_and_numbers.json'

    Returns:
        str: path to the output JSON file
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = []
    for entry in data:
        new_entry = {}

        # Keep "Taxa" if it exists
        if "Taxa" in entry:
            new_entry["Taxa"] = entry["Taxa"]

        # Keep keys that start with a number
        for key, value in entry.items():
            if re.match(r"^\d+", key):
                new_entry[key] = value

        result.append(new_entry)

    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}_taxa_and_numbers.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Extraction completed, result saved to '{output_file}'")
    return output_file


def extract_iawa_information(json_obj):
    family = ""
    original_string = json_obj["Taxa"].replace("?", "")

    for x in original_string.split("|"):
        x = x.replace("Synonym:", "").strip()

        # Famille en majuscules
        family_match = re.search(r"[A-Z][A-Z]+\s[A-Z][A-Z]+|[A-Z][A-Z]+", x)
        family = family_match.group(0) if family_match else ""

        # Genre / espèce
        genre_match = re.search(
            r"[A-Z][a-z]+\s(spp\.|sp\.|SPP\.|SP\.|sect\.)|"
            r"[A-Z][a-z]+\s[a-z]+\s(subsp\.|var\.)\s[a-z]+|"
            r"[A-Z][a-z]+\s(aff\.|cf\.)\s[a-z\-]+|"
            r"[A-Z][a-z]+\s[a-z\-]+|"
            r"[A-Z][a-z]+\.*",
            x,
        )
        genre = genre_match.group(0) if genre_match else ""

        # Nom usuel entre parenthèses
        usual_name_match = re.search(r"\([A-Z][A-Z,\s]+\)", x)
        usual_name = usual_name_match.group(0) if usual_name_match else ""

        # On suppose que seul le premier élément traité nous intéresse
        return family, genre, usual_name, original_string


def parse_iawa_file(json_input_path, json_output_path):
    results = []

    with open(json_input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for obj in data:
        try:
            family, genre, usual_name, original_string = extract_iawa_information(obj)
            results.append(
                {
                    "family": family,
                    "genre": genre,
                    "usual_name": usual_name,
                    "original": original_string,
                }
            )
        except Exception as e:
            print(f"Erreur lors du traitement de l'entrée : {obj}\n{e}")

    # Écriture dans un fichier JSON
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"✅ Résultats écrits dans '{json_output_path}'")


def extract_iawa_information(json_obj):
    family = ""
    original_string = json_obj["Taxa"].replace("?", "")

    for x in original_string.split("|"):
        x = x.replace("Synonym:", "").strip()

        family_match = re.search(r"[A-Z][A-Z]+\s[A-Z][A-Z]+|[A-Z][A-Z]+", x)
        family = family_match.group(0) if family_match else ""

        genre_match = re.search(
            r"[A-Z][a-z]+\s(spp\.|sp\.|SPP\.|SP\.|sect\.)|"
            r"[A-Z][a-z]+\s[a-z]+\s(subsp\.|var\.)\s[a-z]+|"
            r"[A-Z][a-z]+\s(aff\.|cf\.)\s[a-z\-]+|"
            r"[A-Z][a-z]+\s[a-z\-]+|"
            r"[A-Z][a-z]+\.*",
            x,
        )
        genre = genre_match.group(0) if genre_match else ""

        usual_name_match = re.search(r"\([A-Z][A-Z,\s]+\)", x)
        usual_name = usual_name_match.group(0) if usual_name_match else ""

        return family, genre, usual_name, original_string


def rewrite_taxa_with_genre(json_input_path, json_output_path=None):
    if json_output_path is None:
        base, _ = os.path.splitext(json_input_path)
        json_output_path = f"{base}_resultats.json"

    with open(json_input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_data = []

    for obj in data:
        try:
            _, genre, _, _ = extract_iawa_information(obj)
            new_obj = obj.copy()
            new_obj["Taxa"] = genre  # Remplacement du champ "Taxa"
            updated_data.append(new_obj)
        except Exception as e:
            print(f"Erreur lors du traitement de l'entrée : {obj}\n{e}")
            updated_data.append(obj)  # Si erreur, on garde l'objet d'origine

    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON mis à jour avec les genres dans '{json_output_path}'")
    return json_output_path


def transform_single_taxa_dict(input_dict):
    result = {}

    # Renomme "Taxa" en "Taxon"
    result["Taxon"] = input_dict.get("Taxa", "")

    for key, value in input_dict.items():
        if key.strip() == "Taxa" or (isinstance(value, str) and value.strip() == ""):
            continue

        # Extraction du nombre au début de la clé
        match = re.match(r"^(\d+)", key)
        if match:
            num = match.group(1)
            # clé devient le nombre sur 3 chiffres uniquement
            new_key = num.zfill(3)
            result[new_key] = value
        else:
            # on garde la clé telle quelle si pas de nombre au début
            result[key] = value

    return result


def transform_json_file(input_json_path):
    # Création du chemin du dossier d'export

    os.makedirs(export_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

    base_name = os.path.splitext(os.path.basename(input_json_path))[0]
    output_json_path = os.path.join(export_dir, f"{base_name}_homogene.json")

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_list = json.load(f)

    transformed_list = [transform_single_taxa_dict(taxa) for taxa in input_list]

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(transformed_list, f, ensure_ascii=False, indent=4)

    print(f"✅ Transformation terminée, fichier sauvegardé sous : {output_json_path}")
    return output_json_path


def delete_json_files():
    for file in os.listdir("."):
        if file.endswith(".json") and os.path.isfile(file):
            os.remove(file)
            print(f" Deleted: {file}")
