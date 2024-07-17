import argparse
import base64
import csv
import os
from typing import Any, Dict, Generator, Optional, Tuple

import requests

TRANSLATION_COLUMN_INDEX = 8
WORD_COLUMN_INDEX = 4
CORRECT_ROW_COUNT = 10


def send_post_request(url: str, data: dict) -> requests.Response:
    response = requests.post(url, json=data)
    print("POST response status:", response.status_code)
    return response


def fetch_response_content(response_json: Dict[str, Any]) -> Optional[str]:
    try:
        if (
            response_json["status"] == "success"
            and response_json["data"] != "NO_ITEMS_FOUND"
        ):
            file_content_full = response_json["data"]["fileContent_base64"]
            file_content_dict = file_content_full.split(",")[1]
            return base64.b64decode(file_content_dict)
        else:
            print(f"No items found in response: {response_json['data']}")
            return None
    except (KeyError, IndexError, TypeError) as e:
        print(f"Failed to decode response content: {e}")
        return None


def save_csv_content(csv_content: bytes, file_path: str) -> Optional[str]:
    try:
        with open(file_path, "wb") as file:
            file.write(csv_content)
        print(f"CSV file saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to save CSV content: {e}")
        return None


def extract_words_from_csv(file_path: str) -> Generator[Tuple[str, str], None, None]:
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter="\t")
            for row in csv_reader:
                if len(row) > CORRECT_ROW_COUNT:
                    word = row[WORD_COLUMN_INDEX]
                    translation = row[TRANSLATION_COLUMN_INDEX]
                    print(f"Extracted word:{word}, translation:{translation}")
                    yield (word, translation)
                else:
                    print(f"Row does not have enough columns: {row}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Failed to extract words from CSV: {e}")


def append_words_to_md(
    md_file_path: str, words: Generator[Tuple[str, str], None, None]
) -> bool:
    try:
        with open(md_file_path, "a", encoding="utf-8") as file:
            for word, translation in words:
                file.write(f"{word} :: {translation}\n")
        print(f"Words appended to {md_file_path}")
        return True
    except Exception as e:
        print(f"Failed to append words to Markdown file: {e}")
        return False


def delete_file(file_path: str) -> bool:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted.")
            return True
        else:
            print(f"File {file_path} does not exist.")
            return False
    except Exception as e:
        print(f"Failed to delete file {file_path}: {e}")
        return False


def main() -> None:
    url = "https://api-cdn.dioco.io/base_export_itemsCSVExport_7"
    parser = argparse.ArgumentParser(description="Export items with specified options.")
    
    parser.add_argument("--csv_save_path", type=str, required=True, help="Path to save the exported CSV file.")
    parser.add_argument("--obsidian_dict_path", type=str, required=True, help="Path to the Obsidian dictionary file.")
    parser.add_argument("--item_type", type=str, default=None, help="Type of item.")
    parser.add_argument("--lang_code", type=str, default="en", help="Language code.")
    parser.add_argument("--learning_stages", type=str, nargs='+', default=["LEARNING"], help="Learning stages.")
    parser.add_argument("--tags", type=str, default=None, help="Tags.")
    parser.add_argument("--source", type=str, default=None, help="Source.")
    parser.add_argument("--preferred_translation_type", type=str, default="machine", help="Preferred translation type.")
    parser.add_argument("--load_more_last_extended_key", type=str, default=None, help="Load more last extended key.")
    parser.add_argument("--load_more_part_num", type=int, default=1, help="Load more part number.")
    parser.add_argument("--export_media", type=bool, default=False, help="Export media.")
    parser.add_argument("--items_since_last_export_only", type=bool, default=True, help="Items since last export only.")
    parser.add_argument("--user_email", type=str, default=os.getenv("EMAIL_API"), help="User email.")
    parser.add_argument("--dioco_token", type=str, default=os.getenv("DIOCO_API_KEY"), help="Dioco token.")

    args = parser.parse_args()

    csv_save_path = args.csv_save_path
    obsidian_dict_path = args.obsidian_dict_path

    data = {
        "itemType": args.item_type,
        "langCode_G": args.lang_code,
        "learningStages": args.learning_stages,
        "tags": args.tags,
        "source": args.source,
        "preferredTranslationType": args.preferred_translation_type,
        "loadMoreLastExtendedKey": args.load_more_last_extended_key,
        "loadMorePartNum": args.load_more_part_num,
        "exportMedia": args.export_media,
        "itemsSinceLastExportOnly": args.items_since_last_export_only,
        "userEmail": args.user_email,
        "diocoToken": args.dioco_token,
    }

    post_response = send_post_request(url, data)
    content = fetch_response_content(post_response)
    csv_file_path = None

    if content:
        csv_file_path = save_csv_content(content, csv_save_path)

    if csv_file_path:
        words = extract_words_from_csv(csv_file_path)
        if append_words_to_md(obsidian_dict_path, words):
            delete_file(csv_file_path)


if __name__ == "__main__":
    main()
