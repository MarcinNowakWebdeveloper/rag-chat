from backend.core.config import config
from backend.imports.types.file import import_folder
from backend.imports.types.web import import_web_list
from backend.core.vector_store import delete_collection

import os
import argparse

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"
)


def reset_db():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()
    if args.reset:
        delete_collection()
        print(f"🧹 DB is reset")


if __name__ == "__main__":
    reset_db()
    import_folder(config.DATA_PATH)
    import_web_list(seed_urls=config.WEB_CRAWLER.source)
