"""
config.py
---------
Centralized configuration for the TechNews Scraper & Aggregator.

Keeping all constants (URLs, headers, timeouts, file paths) in a single
module follows the Single Responsibility Principle and makes the project
easy to reconfigure without touching business logic.
"""

from pathlib import Path

# --- Target source configuration ---------------------------------------
BASE_URL: str = "https://news.ycombinator.com/"

# A realistic User-Agent header reduces the chance of being blocked or
# served a stripped-down version of the page by the target website.
REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# --- Networking behaviour -------------------------------------------------
REQUEST_TIMEOUT_SECONDS: int = 10
MAX_RETRIES: int = 3
RETRY_BACKOFF_SECONDS: float = 1.5

# --- Output configuration -------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
OUTPUT_JSON_PATH: Path = PROJECT_ROOT / "news_data.json"

# Maximum number of articles to display/save (0 = no limit)
MAX_ARTICLES: int = 30
