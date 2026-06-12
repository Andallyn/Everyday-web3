"""Plugin contracts and integration recommendations.

The first version of this project is intentionally local-first: collect links
from X lists, Lu.ma, plan.wtf, Cryptonomads, Telegram, or newsletters into CSV
or JSON and run the generator. These plugin contracts describe the shape future
collectors should return when API keys or scraping services are added.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import SourceItem


class SourcePlugin(Protocol):
    """A source collector that returns normalized Everyday Web3 source items."""

    name: str

    def fetch(self) -> list[SourceItem]:
        """Fetch and normalize source items."""


@dataclass(frozen=True)
class ManualCsvPlugin:
    """Use a curated CSV export as the source of truth."""

    name: str = "manual_csv"

    def fetch(self) -> list[SourceItem]:
        raise NotImplementedError("Manual CSV input is loaded directly by the CLI.")


@dataclass(frozen=True)
class XListPlugin:
    """Placeholder for an X list collector using the X API or an export tool."""

    list_url: str
    name: str = "x_list"

    def fetch(self) -> list[SourceItem]:
        raise NotImplementedError(
            "Connect this to the X API, a bookmark export, Readwise Reader, or an Apify actor."
        )


@dataclass(frozen=True)
class EventsPlugin:
    """Placeholder for event sources such as Lu.ma, plan.wtf, and Cryptonomads."""

    source_url: str
    name: str = "events"

    def fetch(self) -> list[SourceItem]:
        raise NotImplementedError(
            "Connect this to a calendar/RSS/API feed and return normalized SourceItem objects."
        )


def recommended_plugins() -> list[dict[str, str]]:
    """Return practical integrations for the Everyday Web3 workflow."""

    return [
        {
            "name": "X list/bookmark collector",
            "priority": "1 - core signal layer",
            "cost_tier": "moderate to high depending on X/API/scraping route",
            "use": "Pull links from your Everyday Web3 X list, bookmarked tweets, and quoted recaps.",
            "setup": "Start with manual CSV exports; later connect the X API, Readwise Reader, Zapier, or Apify.",
        },
        {
            "name": "Firecrawl or event feed collector",
            "priority": "2 - conference and website monitoring",
            "cost_tier": "low to moderate depending on crawl volume",
            "use": "Collect Lu.ma, plan.wtf, Cryptonomads, conference, hackathon, and local meetup listings.",
            "setup": "Prefer official ICS/RSS/API feeds when available; normalize title, date, city, URL, and tags.",
        },
        {
            "name": "Exa or Tavily search",
            "priority": "3 - discovery beyond known sources",
            "cost_tier": "low to moderate depending on query volume",
            "use": "Find new retreats, DAO meetups, product launches, city guides, and IRL Web3 announcements.",
            "setup": "Run saved searches for each category and feed strong results into the source CSV/database.",
        },
        {
            "name": "Notion or Airtable editorial desk",
            "priority": "4 - operating system",
            "cost_tier": "low to moderate depending on team size",
            "use": "Keep sources, statuses, categories, hooks, visual notes, and publish dates in one place.",
            "setup": "Use this generator's CSV columns as the database schema, then export CSV for generation.",
        },
        {
            "name": "Buffer, Typefully, Hypefury, or Publer",
            "priority": "5 - publishing workflow",
            "cost_tier": "low to moderate depending on channels",
            "use": "Schedule X threads, LinkedIn posts, Instagram captions, and community announcements.",
            "setup": "Paste generated platform drafts into your scheduler and track which formats perform best.",
        },
        {
            "name": "Canva or Figma template library",
            "priority": "6 - visual system",
            "cost_tier": "low to moderate",
            "use": "Turn generated Pinterest/Instagram visual direction into repeatable carousels and pins.",
            "setup": "Create templates for event preview, creator spotlight, local alpha, and weekly roundup.",
        },
        {
            "name": "Zapier or Make automation",
            "priority": "7 - workflow glue",
            "cost_tier": "low to high depending on task volume",
            "use": "Move new sources from forms, bookmarks, or spreadsheets into the generator input file.",
            "setup": "Trigger on saved links and map fields to title, URL, summary, category, tags, and priority.",
        },
    ]
