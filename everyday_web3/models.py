"""Core data structures for the Everyday Web3 content engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


def split_list(value: str | list[str] | None) -> list[str]:
    """Normalize comma/pipe separated values into a clean list."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    parts: list[str] = []
    for chunk in str(value).replace("|", ",").split(","):
        cleaned = chunk.strip()
        if cleaned:
            parts.append(cleaned)
    return parts


@dataclass(frozen=True)
class SourceItem:
    """One source or piece of raw alpha that can become content."""

    title: str
    url: str = ""
    summary: str = ""
    category: str = ""
    source_type: str = "article"
    location: str = ""
    event_date: str = ""
    tags: list[str] = field(default_factory=list)
    people: list[str] = field(default_factory=list)
    priority: int = 3
    notes: str = ""

    @classmethod
    def from_mapping(cls, row: dict[str, Any]) -> "SourceItem":
        title = str(row.get("title") or row.get("name") or "").strip()
        if not title:
            raise ValueError("source item is missing a title")

        priority_value = row.get("priority", 3)
        try:
            priority = int(priority_value)
        except (TypeError, ValueError):
            priority = 3

        return cls(
            title=title,
            url=str(row.get("url") or row.get("link") or "").strip(),
            summary=str(row.get("summary") or row.get("description") or "").strip(),
            category=str(row.get("category") or "").strip(),
            source_type=str(row.get("source_type") or row.get("type") or "article").strip(),
            location=str(row.get("location") or row.get("city") or "").strip(),
            event_date=str(row.get("event_date") or row.get("date") or "").strip(),
            tags=split_list(row.get("tags")),
            people=split_list(row.get("people") or row.get("creators")),
            priority=max(1, min(5, priority)),
            notes=str(row.get("notes") or "").strip(),
        )

    @property
    def searchable_text(self) -> str:
        return " ".join(
            [
                self.title,
                self.summary,
                self.category,
                self.source_type,
                self.location,
                " ".join(self.tags),
                " ".join(self.people),
                self.notes,
            ]
        ).lower()


@dataclass(frozen=True)
class ContentIdea:
    """A generated content idea adapted to a platform."""

    title: str
    platform: str
    category: str
    format_name: str
    shift: str
    hook: str
    angle: str
    body: str
    cta: str
    hashtags: list[str]
    sources: list[SourceItem]

    def to_markdown(self) -> str:
        source_lines = "\n".join(
            f"- {source.title}{f' ({source.url})' if source.url else ''}" for source in self.sources
        )
        hashtag_line = " ".join(self.hashtags)
        return "\n".join(
            [
                f"## {self.title}",
                "",
                f"- Platform: {self.platform}",
                f"- Format: {self.format_name}",
                f"- Category: {self.category}",
                f"- Shift: {self.shift}",
                "",
                "### Hook",
                self.hook,
                "",
                "### Angle",
                self.angle,
                "",
                "### Draft",
                self.body,
                "",
                "### CTA",
                self.cta,
                "",
                "### Hashtags",
                hashtag_line,
                "",
                "### Sources",
                source_lines or "- Add source",
                "",
            ]
        )


@dataclass(frozen=True)
class GenerationContext:
    """Settings that apply to one generator run."""

    run_date: date
    brand_name: str
    voice: str
    platforms: list[str]
