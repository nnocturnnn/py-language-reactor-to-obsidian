import os
import shutil
import zipfile

import pandas as pd
import requests

url = "https://lb.dioco.io/base_items_itemsCSVExport_7"

headers = {
    "Accept":
    "application/json, text/plain, */*",
    "Accept-Language":
    "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
    "Connection":
    "keep-alive",
    "Content-Type":
    "application/json",
    "Origin":
    "https://www.languagereactor.com",
    "Referer":
    "https://www.languagereactor.com/",
    "Sec-Fetch-Dest":
    "empty",
    "Sec-Fetch-Mode":
    "cors",
    "Sec-Fetch-Site":
    "cross-site",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320",
}

data = {
    "itemType":
    None,
    "langCode_G":
    "en",
    "learningStages": ["LEARNING"],
    "tags":
    None,
    "source":
    None,
    "preferredTranslationType":
    "machine",
    "loadMoreLastExtendedKey":
    None,
    "loadMorePartNum":
    1,
    "exportMedia":
    False,
    "itemsSinceLastExportOnly":
    False,
    "userEmail":
    "mediandrey@gmail.com",
    "diocoToken":
    "UwR6l31fOW37nN8OdjjQeer7vMZktx7S6I2SwhZ7wODwY3ASDjSo6r0hI88P8TwGfHljykePmO4TJmGCmCMhNw==",
}

# def get_data_url() -> str:
#     response = requests.post(url, json=data, headers=headers)

#     if response.status_code == 200:
#         print(response.text)
#     else:
#         print(f"Request failed with status code {response.status_code}")
#     return response.json()['data']['file_path']


def download_csv_lr(file_url: str) -> None:
    """

    :param file_url: str:

    """
    local_filename = "lr.zip"
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File '{local_filename}' has been downloaded.")
    else:
        print(
            f"Failed to download the file. Status code: {response.status_code}"
        )
    return local_filename


def unzip(filename: str) -> None:
    """

    :param filename: str:

    """
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("unziplr")
    try:
        os.remove(filename)
        print(f"File '{filename}' has been removed.")
    except OSError as e:
        print(f"Error: {e}")
    try:
        os.rename("unziplr/items.csv", "items.csv")
        print("Done")
    except OSError as e:
        print(f"Error: {e}")
    try:
        shutil.rmtree("unziplr")
        print(f"Directory unziplr and its contents have been removed.")
    except Exception as e:
        print(f"Error: {e}")


def prepare_to_import(input_file: str, output_file: str) -> None:
    """

    :param input_file: str:
    :param output_file: str:

    """
    try:
        df = pd.read_csv(input_file, delimiter="\t")
        df["Combined_Column"] = df.apply(
            lambda row: f"{row.iloc[4]} [{row.iloc[5]}] ({row.iloc[6]})",
            axis=1)
        df = df[["Combined_Column", df.columns[8]]]
        df.to_csv(output_file, index=False)
    except Exception as e:
        print(f"n error occurred: {str(e)}")
    try:
        os.remove(input_file)
        print(f"File '{input_file}' has been removed.")
    except OSError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    unzip(download_csv_lr(""))
    prepare_to_import("items.csv", "out.csv")
