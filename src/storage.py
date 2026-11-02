"""
storage.py
----------
Handles persistence of scraped data. Currently implements JSON storage,
but is structured so that adding a SQLite backend later only requires
adding a new function here — no changes needed in scraper.py or display.py.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.config import OUTPUT_JSON_PATH
from src.models import NewsArticle

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Raised when reading from or writing to the storage backend fails."""


def save_to_json(
    articles: list[NewsArticle], output_path: Path = OUTPUT_JSON_PATH
) -> None:
    """
    Persist a list of NewsArticle objects to a JSON file.

    The output includes a small metadata envelope (scraped_at, count) so
    consumers of the JSON file know when and how much data was collected.

    Args:
        articles: The articles to save.
        output_path: Destination file path.

    Raises:
        StorageError: If the file cannot be written (e.g. permissions,
            invalid path, disk full).
    """
    payload = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "count": len(articles),
        "articles": [article.to_dict() for article in articles],
    }

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
        logger.info("Saved %d articles to %s", len(articles), output_path)

    except OSError as exc:
        raise StorageError(f"Could not write to '{output_path}': {exc}") from exc


def load_from_json(input_path: Path = OUTPUT_JSON_PATH) -> list[dict]:
    """
    Load previously saved articles from a JSON file.

    Args:
        input_path: Path to the JSON file to read.

    Returns:
        A list of article dictionaries. Returns an empty list if the file
        does not exist yet (first run scenario).

    Raises:
        StorageError: If the file exists but contains invalid JSON.
    """
    if not input_path.exists():
        logger.info("No existing data file at %s; starting fresh.", input_path)
        return []

    try:
        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("articles", [])

    except json.JSONDecodeError as exc:
        raise StorageError(f"Corrupted JSON file at '{input_path}': {exc}") from exc
