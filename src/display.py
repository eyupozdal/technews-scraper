"""
display.py
----------
Handles presentation of the scraped data in the terminal.

Uses the `rich` library for a polished table view. If `rich` is not
installed for some reason, it gracefully falls back to a plain-text
table so the application never crashes just because of a missing
optional dependency.
"""

import logging
import shutil

from src.models import NewsArticle

logger = logging.getLogger(__name__)

try:
    from rich.console import Console
    from rich.table import Table

    _RICH_AVAILABLE = True
except ImportError:  # pragma: no cover - environment-dependent
    _RICH_AVAILABLE = False
    logger.warning("'rich' is not installed; falling back to plain-text output.")


def display_articles(articles: list[NewsArticle]) -> None:
    """
    Print articles to the terminal in a readable table format.

    Args:
        articles: The list of articles to display. If empty, a friendly
            message is shown instead of an empty table.
    """
    if not articles:
        print("\nNo articles were found to display.\n")
        return

    if _RICH_AVAILABLE:
        _display_with_rich(articles)
    else:
        _display_plain(articles)


def _display_with_rich(articles: list[NewsArticle]) -> None:
    """Render a styled table using the `rich` library."""
    console = Console()
    table = Table(
        title="Latest Tech News",
        show_lines=False,
        header_style="bold cyan",
    )

    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Title", style="bold white", overflow="fold")
    table.add_column("Points", justify="right", style="green", width=7)
    table.add_column("Published", style="yellow", width=28)
    table.add_column("URL", style="blue", overflow="fold")

    for index, article in enumerate(articles, start=1):
        table.add_row(
            str(index),
            article.title,
            str(article.points) if article.points is not None else "-",
            article.published_at,
            article.url,
        )

    console.print(table)
    console.print(f"[bold green]Total articles displayed:[/bold green] {len(articles)}")


def _display_plain(articles: list[NewsArticle]) -> None:
    """Fallback renderer: a simple fixed-width text table, no dependencies."""
    width = shutil.get_terminal_size(fallback=(100, 24)).columns
    separator = "-" * min(width, 100)

    print(separator)
    print(f"{'#':<4}{'Title':<60}{'Points':<8}{'Published':<25}")
    print(separator)

    for index, article in enumerate(articles, start=1):
        truncated_title = (
            article.title if len(article.title) <= 57 else article.title[:54] + "..."
        )
        points_display = str(article.points) if article.points is not None else "-"
        print(
            f"{index:<4}{truncated_title:<60}{points_display:<8}{article.published_at:<25}"
        )
        print(f"    -> {article.url}")

    print(separator)
    print(f"Total articles displayed: {len(articles)}")
