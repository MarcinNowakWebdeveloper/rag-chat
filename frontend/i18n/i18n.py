import json
import os
from typing import List


class I18n:
    def __init__(self, lang: str):
        self.base_path = os.path.dirname(__file__)
        self.available_languages = self.get_available_languages()

        # fallback jeśli język nie istnieje
        if lang not in self.available_languages:
            lang = "en"

        self.lang = lang

        file_path = os.path.join(self.base_path, f"{lang}.json")

        with open(file_path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def t(self, key: str) -> str:
        return self.translations.get(key, key)

    @staticmethod
    def get_available_languages() -> List[str]:
        base_path = os.path.dirname(__file__)

        files = os.listdir(base_path)

        langs = [f.replace(".json", "") for f in files if f.endswith(".json")]

        return sorted(langs)
