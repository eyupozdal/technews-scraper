"""Offline unit tests: no network access required."""

from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from src.scraper import ScraperError, fetch_page, parse_articles

FIXTURE = Path(__file__).parent / "fixtures" / "sample_page.html"


@pytest.fixture
def sample_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parses_valid_articles_and_skips_malformed_rows(sample_html: str) -> None:
    articles = parse_articles(sample_html)
    assert len(articles) == 2  # 3rd row has no title and must be skipped


def test_extracts_fields_correctly(sample_html: str) -> None:
    first = parse_articles(sample_html)[0]
    assert first.title == "A Breakthrough in Local LLM Inference"
    assert first.url == "https://example.com/article-one"
    assert first.points == 245
    assert first.published_at == "2026-09-18T10:00:00"


def test_relative_urls_are_made_absolute(sample_html: str) -> None:
    second = parse_articles(sample_html)[1]
    assert second.url == "https://news.ycombinator.com/item?id=1002"


def test_empty_html_returns_empty_list() -> None:
    assert parse_articles("<html></html>") == []


def test_fetch_page_raises_scraper_error_after_retries() -> None:
    with patch(
        "src.scraper.requests.get", side_effect=requests.ConnectionError("boom")
    ), patch("src.scraper.time.sleep"):
        with pytest.raises(ScraperError):
            fetch_page("https://example.invalid/")
