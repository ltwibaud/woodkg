from thesaurusFunctions import *

iawa_thesaurus_raw = "../../input/iawa_thesaurus/raw"


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    generate_full_combined_oneline_json(
        convert_iawa_tsv_to_json_three_dicts(iawa_thesaurus_raw)
    )

    delete_json_files()


if __name__ == "__main__":
    main()
