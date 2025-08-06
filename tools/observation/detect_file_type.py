import os
import sys


def detect_single_file_type(file_path):
    if not os.path.isfile(file_path):
        return "Error: The provided path is not a valid file."

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".json":
        return "json"
    elif ext in [".csv", ".tsv"]:
        return "csv"
    else:
        return "Error: File must be a .json, .csv, or .tsv."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = detect_single_file_type(file_path)
    print(result)
