"""
scraper.py
----------
Responsible ONLY for network communication and HTML parsing.

Design principle: this module knows nothing about how data will be
displayed or stored. It simply fetches raw HTML and turns it into a
clean list of `NewsArticle` objects. This separation of concerns makes
the scraper easy to unit test and easy to swap out (e.g. replace HN
with another source) without touching storage/display code.
"""

import logging
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout

from src.config import (
    BASE_URL,
    MAX_ARTICLES,
    MAX_RETRIES,
    REQUEST_HEADERS,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_BACKOFF_SECONDS,
)
from src.models import NewsArticle

logger = logging.getLogger(__name__)


class ScraperError(Exception):
    """Raised when the scraper cannot retrieve or parse the target page."""


def fetch_page(url: str = BASE_URL) -> str:
    """
    Fetch the raw HTML content of a given URL with retry logic.

    Args:
        url: The target URL to request.

    Returns:
        The raw HTML content as a string.

    Raises:
        ScraperError: If all retry attempts fail due to network issues
            or a non-200 HTTP status code.
    """
    last_exception: Optional[Exception] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Fetching %s (attempt %d/%d)", url, attempt, MAX_RETRIES)
            response = requests.get(
                url,
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx
            return response.text

        except Timeout as exc:
            last_exception = exc
            logger.warning("Request timed out on attempt %d", attempt)

        except RequestException as exc:
            # Covers ConnectionError, HTTPError, TooManyRedirects, etc.
            last_exception = exc
            logger.warning("Request failed on attempt %d: %s", attempt, exc)

        # Exponential-ish backoff before retrying (skip after last attempt)
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    raise ScraperError(
        f"Failed to fetch '{url}' after {MAX_RETRIES} attempts: {last_exception}"
    )


def parse_articles(html: str, source_name: str = "Hacker News") -> list[NewsArticle]:
    """
    Parse raw HTML from Hacker News into a list of NewsArticle objects.

    The parser is defensive: if an individual row is missing an expected
    element (title, link, or timestamp), that row is skipped and logged
    rather than crashing the whole run.

    Args:
        html: Raw HTML content of the listing page.
        source_name: Human-readable name of the source site.

    Returns:
        A list of successfully parsed NewsArticle instances.
    """
    soup = BeautifulSoup(html, "html.parser")
    articles: list[NewsArticle] = []

    # Each story on Hacker News lives in a <tr class="athing">, and its
    # metadata (age, points) lives in the *next* sibling <tr class="subtext">.
    story_rows = soup.find_all("tr", class_="athing")

    if not story_rows:
        logger.warning(
            "No story rows found. The site's HTML structure may have changed."
        )

    for row in story_rows:
        try:
            article = _parse_single_row(row, source_name)
            if article is not None:
                articles.append(article)
        except Exception as exc:  # noqa: BLE001 - defensive parsing boundary
            # We deliberately catch broad exceptions here because a single
            # malformed row should never stop the entire scraping process.
            logger.warning("Skipping a malformed row due to: %s", exc)
            continue

        if MAX_ARTICLES and len(articles) >= MAX_ARTICLES:
            break

    return articles


def _parse_single_row(row, source_name: str) -> Optional[NewsArticle]:
    """
    Parse a single <tr class="athing"> row plus its metadata sibling row.

    Returns None (instead of raising) when required elements are missing,
    so the caller can decide how to log/skip it.
    """
    title_span = row.find("span", class_="titleline")
    if title_span is None or title_span.find("a") is None:
        logger.debug("Missing title element for row id=%s", row.get("id"))
        return None

    link_tag = title_span.find("a")
    title = link_tag.get_text(strip=True)
    url = link_tag.get("href", "").strip()

    # Hacker News sometimes uses relative URLs for "Ask HN" / local items.
    if url.startswith("item?id="):
        url = BASE_URL + url

    # The metadata (age, points) is in the immediately following <tr>.
    subtext_row = row.find_next_sibling("tr")
    published_at = "Unknown"
    points: Optional[int] = None

    if subtext_row is not None:
        age_tag = subtext_row.find("span", class_="age")
        if age_tag is not None:
            # The 'title' attribute holds a full ISO-8601 timestamp,
            # while the visible text holds a relative string like "3 hours ago".
            published_at = age_tag.get("title", age_tag.get_text(strip=True))

        score_tag = subtext_row.find("span", class_="score")
        if score_tag is not None:
            digits = "".join(ch for ch in score_tag.get_text() if ch.isdigit())
            points = int(digits) if digits else None

    if not title or not url:
        logger.debug("Incomplete data (title/url) for row id=%s", row.get("id"))
        return None

    return NewsArticle(
        title=title,
        url=url,
        published_at=published_at,
        source=source_name,
        points=points,
    )


def scrape_latest_news(url: str = BASE_URL) -> list[NewsArticle]:
    """
    High-level convenience function: fetch + parse in one call.

    Args:
        url: The target listing page URL.

    Returns:
        A list of NewsArticle objects. Returns an empty list (rather than
        raising) if fetching fails, so the calling code can decide how to
        handle a completely failed run.
    """
    try:
        html = fetch_page(url)
    except ScraperError as exc:
        logger.error("Scraping aborted: %s", exc)
        return []

    return parse_articles(html)
