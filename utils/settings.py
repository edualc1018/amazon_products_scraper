from typing import List

from .file import get_base_directory

import json

settings_json = f"{get_base_directory()}/settings.json"

with open(settings_json, "r") as file:
    settings = json.load(file)


def get_search_terms() -> List[str]:
    return settings["search_terms"]


def get_cookie_string() -> str:
    return settings["cookie_string"]


def get_limit() -> int or "all":
    return settings["pages"]


def is_show_html() -> bool:
    return settings["show_html"]


def get_group() -> str or bool:
    return settings["group"]


def get_delay():
    return settings["delay"]
