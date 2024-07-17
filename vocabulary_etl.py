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
    post_url = "https://api-cdn.dioco.io/base_export_itemsCSVExport_7"
    csv_save_path = "exported_items.csv"
    md_file_path = "/Users/andriisydoruk/Library/Mobile Documents/iCloud~md~obsidian/Documents/andi/Dict.md"

    data = {
        "itemType": None,
        "langCode_G": "en",
        "learningStages": ["LEARNING"],
        "tags": None,
        "source": None,
        "preferredTranslationType": "machine",
        "loadMoreLastExtendedKey": None,
        "loadMorePartNum": 1,
        "exportMedia": False,
        "itemsSinceLastExportOnly": True,
        "userEmail": os.getenv("EMAIL_API"),
        "diocoToken": os.getenv("DIOCO_API_KEY"),
    }

    post_response = send_post_request(post_url, data)
    content = fetch_response_content(post_response)
    csv_file_path = None

    if content:
        csv_file_path = save_csv_content(content, csv_save_path)

    if csv_file_path:
        words = extract_words_from_csv(csv_file_path)
        if append_words_to_md(md_file_path, words):
            delete_file(csv_file_path)


if __name__ == "__main__":
    main()
