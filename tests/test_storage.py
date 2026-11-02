"""Tests for JSON persistence."""

import pytest

from src.models import NewsArticle
from src.storage import StorageError, load_from_json, save_to_json


def test_save_and_load_round_trip(tmp_path) -> None:
    path = tmp_path / "out.json"
    articles = [NewsArticle("T", "https://x.com", "now", "HN", 5)]
    save_to_json(articles, path)
    assert load_from_json(path) == [articles[0].to_dict()]


def test_load_missing_file_returns_empty_list(tmp_path) -> None:
    assert load_from_json(tmp_path / "nope.json") == []


def test_load_corrupted_file_raises_storage_error(tmp_path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(StorageError):
        load_from_json(path)
