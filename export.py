import requests
import base64
import csv
import os

def make_options_request(url, headers):
    response = requests.options(url, headers=headers)
    print("OPTIONS response status:", response.status_code)
    return response

def make_post_request(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    print("POST response status:", response.status_code)
    return response

def parse_and_save_response(response, file_path):
    response_json = response.json()
    file_content_base64 = response_json['data']['fileContent_base64'].split(',')[1]
    csv_content = base64.b64decode(file_content_base64)
    
    with open(file_path, 'wb') as file:
        file.write(csv_content)
    
    print(f"CSV file saved to {file_path}")
    return file_path

def extract_words_from_csv(file_path):
    words = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter='\t')
        for row in csv_reader:
            if len(row) > 10:  # Ensure the row has enough columns
                word = row[4]  # Fifth column for the word itself
                translation = row[8]  # Fourth column for the translation
                print(f"Extracted word: {word}, translation: {translation}")  # Debug print
                words.append((word, translation))
            else:
                print(f"Row does not have enough columns: {row}")  # Debug print
    return words

def append_words_to_md(md_file_path, words):
    with open(md_file_path, 'a', encoding='utf-8') as file:
        for word, translation in words:
            file.write(f"{word} :: {translation}\n")
    print(f"Words appended to {md_file_path}")

def main():
    options_url = 'https://api-cdn.dioco.io/base_export_itemsCSVExport_7'
    post_url = 'https://api-cdn.dioco.io/base_export_itemsCSVExport_7'
    csv_file_path = 'exported_items.csv'
    md_file_path = '/Users/andriisydoruk/Library/Mobile Documents/iCloud~md~obsidian/Documents/andi/Dict.md'
    
    options_headers = {
        'accept': '*/*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
        'access-control-request-headers': 'content-type',
        'access-control-request-method': 'POST',
        'cache-control': 'no-cache',
        'origin': 'https://www.languagereactor.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.languagereactor.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
    }
    
    post_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.languagereactor.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.languagereactor.com/',
        'sec-ch-ua': '\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '\"Android\"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
    }
    
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
        "userEmail": "mediandrey@gmail.com",
        "diocoToken": "UwR6l31fOW37nN8OdjjQeer7vMZktx7S6I2SwhZ7wODwY3ASDjSo6r0hI88P8TwGfHljykePmO4TJmGCmCMhNw=="
    }

    # make_options_request(options_url, options_headers)
    # post_response = make_post_request(post_url, post_headers, data)
    # csv_file_path = parse_and_save_response(post_response, csv_file_path)
    
    words = extract_words_from_csv(csv_file_path)
    append_words_to_md(md_file_path, words)

if __name__ == "__main__":
    main()
