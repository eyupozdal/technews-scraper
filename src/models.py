"""
models.py
---------
Defines the core data structure used across the application.

Using a `dataclass` gives us type-checked, self-documenting objects instead
of passing around loosely structured dictionaries between modules.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True, slots=True)
class NewsArticle:
    """
    Represents a single scraped news article.

    Attributes:
        title: The headline of the article.
        url: The direct link to the article (or discussion page as fallback).
        published_at: A human-readable or ISO-like timestamp/age string.
        source: The name of the website the article was scraped from.
        points: Optional score/upvote count, if available on the source site.
    """

    title: str
    url: str
    published_at: str
    source: str
    points: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert the dataclass instance into a plain dictionary.

        Useful for JSON serialization, since `json.dump` cannot natively
        serialize dataclass instances.
        """
        return asdict(self)
