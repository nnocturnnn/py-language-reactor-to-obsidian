# py-language-reactor-to-obsidian

## Overview

This script is designed to export items from the Language Reactor dictionary, process the returned data, and append words along with their translations to an Obsidian Markdown file. This can be particularly useful for creating flashcards for language learning in Obsidian.

## Installation

1. Ensure you have Python 3 installed.
2. Install the required Python libraries:

    ```bash
    pip install requests
    ```

## Usage

The script accepts several command-line arguments to customize its behavior. Below is the usage format:

```bash
python script_name.py --csv_save_path <path_to_save_csv> --obsidian_dict_path <path_to_md_file> [options]
```
### Required Arguments
- **--csv_save_path**: Specify the path where the exported CSV file will be saved.
- **--obsidian_dict_path**: Provide the path to the Obsidian dictionary Markdown file.

### Optional Arguments
- **--item_type**: Define the type of item. (default: `None`)
- **--lang_code**: Set the language code. (default: `"en"`)
- **--learning_stages**: List the learning stages. (default: `["LEARNING"]`)
- **--tags**: Assign tags. (default: `None`)
- **--source**: Specify the source. (default: `None`)
- **--preferred_translation_type**: Set the preferred translation type. (default: `"machine"`)
- **--load_more_last_extended_key**: Provide the key for loading more data. (default: `None`)
- **--load_more_part_num**: Specify the part number for loading more data. (default: `1`)
- **--export_media**: Choose whether to export media. (default: `False`)
- **--items_since_last_export_only**: Export items since the last export only. (default: `True`)
- **--user_email**: Provide the user email. (default: environment variable `EMAIL_API`)
- **--dioco_token**: Provide the Dioco token. (default: environment variable `DIOCO_API_KEY`)
