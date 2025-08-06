from iawa_propertiesFunctions import *

input_folder = "../../input/iawa_thesaurus"
input_raw = f"{input_folder}/raw"
input_currated = f"{input_folder}/currated"
temp_folder = "temp"


def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Ce code génère les combinaisons à partir des fichiers JSON et les sauvegarde dans un fichier JSON.
    generate_combinations_from_json(
        pad_json_keys_to_3_digits(
            map_features_to_iawa_ids(
                extract_iawa_features_from_tsv(input_raw),
                extract_iawa_numbers_mapping(input_raw),
            ),
        )
    )
    extract_foi_op_from_tsv(input_currated, input_raw)


if __name__ == "__main__":
    main()
    delete_json_files()
