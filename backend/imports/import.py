from backend.core.config import config
from backend.imports.types.file import import_folder
from backend.imports.types.web import import_web_list
from backend.imports.bootstrap import bootstrap
from backend.core.vector_store import delete_collection
from backend.core.sql_store import reset_database, truncate_tables

import os
import argparse
import asyncio
import time

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"
)


def reset_db():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--truncate", action="store_true")
    args = parser.parse_args()
    if args.reset:
        delete_collection()
        reset_database()
        print(f"🧹 DB is reset")
    elif args.truncate:
        delete_collection()
        truncate_tables()
        print(f"🧹 DB is truncate")


async def main():
    start = time.perf_counter()
    bootstrap()
    reset_db()

    await asyncio.gather(
        import_folder(config.DATA_PATH),
        import_web_list(seed_urls=config.WEB_CRAWLER.source),
    )

    end = time.perf_counter()
    print(f"⏱ Total time: {end - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
