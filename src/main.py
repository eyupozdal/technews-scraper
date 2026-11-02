"""
main.py
-------
Entry point of the TechNews Scraper & Aggregator.

This module orchestrates the three independent stages of the pipeline:
    1. Scraping   (src.scraper)
    2. Storage    (src.storage)
    3. Display    (src.display)

Each stage is deliberately kept ignorant of the others, which is what
allows them to be tested, replaced, or extended independently (e.g.
swapping JSON storage for SQLite would only require changes in
`storage.py` and one import line here).
"""

import logging
import sys

from src.config import BASE_URL, OUTPUT_JSON_PATH
from src.display import display_articles
from src.scraper import scrape_latest_news
from src.storage import StorageError, save_to_json

# Configure application-wide logging once, at the entry point.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def run() -> int:
    """
    Execute the full scrape -> store -> display pipeline.

    Returns:
        An exit code: 0 on success, 1 if no data could be retrieved,
        2 if data was retrieved but could not be saved.
    """
    logger.info("Starting TechNews Scraper & Aggregator...")
    logger.info("Target source: %s", BASE_URL)

    articles = scrape_latest_news(BASE_URL)

    if not articles:
        logger.error("No articles were retrieved. Aborting run.")
        display_articles(articles)  # Still show the "no articles" message
        return 1

    logger.info("Successfully parsed %d articles.", len(articles))

    # Display first, so the user sees results even if saving fails.
    display_articles(articles)

    try:
        save_to_json(articles, OUTPUT_JSON_PATH)
    except StorageError as exc:
        logger.error("Failed to persist data: %s", exc)
        return 2

    logger.info("Run completed successfully. Data saved to '%s'.", OUTPUT_JSON_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(run())
