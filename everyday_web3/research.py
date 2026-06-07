"""Media and research workflow for Everyday Web3.

This module does not pretend to fetch private or rate-limited sources by itself.
Instead, it creates the operating system for a research desk: source registries,
company watchlists, scoring, daily briefs, and plugin-ready data shapes.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from .engine import EVENING_SHIFT, MORNING_SHIFT, EverydayWeb3Engine, slugify
from .models import SourceItem, split_list


HIGH_SIGNAL_TERMS = [
    "launch",
    "announces",
    "announced",
    "partnership",
    "opens",
    "ships",
    "checkout",
    "wallet",
    "payment",
    "merchant",
    "retreat",
    "meetup",
    "conference",
    "hackathon",
    "residency",
    "coworking",
    "community",
    "burnout",
    "meditation",
    "yoga",
]


@dataclass(frozen=True)
class MonitoredSource:
    """A website, feed, list, or community channel to check."""

    name: str
    url: str
    source_type: str
    track: str
    cadence: str
    plugin: str
    priority: int = 3
    keywords: list[str] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_mapping(cls, row: dict[str, Any]) -> "MonitoredSource":
        return cls(
            name=str(row.get("name") or "").strip(),
            url=str(row.get("url") or "").strip(),
            source_type=str(row.get("source_type") or row.get("type") or "website").strip(),
            track=str(row.get("track") or "both").strip(),
            cadence=str(row.get("cadence") or "daily").strip(),
            plugin=str(row.get("plugin") or "manual_review").strip(),
            priority=int(row.get("priority") or 3),
            keywords=split_list(row.get("keywords")),
            notes=str(row.get("notes") or "").strip(),
        )


@dataclass(frozen=True)
class CompanyProfile:
    """A company or account in the Everyday Web3 coverage universe."""

    name: str
    category: str
    website: str = ""
    x_handle: str = ""
    source_url: str = ""
    region: str = ""
    tags: list[str] = field(default_factory=list)
    priority: int = 3
    notes: str = ""

    @classmethod
    def from_mapping(cls, row: dict[str, Any]) -> "CompanyProfile":
        return cls(
            name=str(row.get("name") or "").strip(),
            category=str(row.get("category") or "").strip(),
            website=str(row.get("website") or "").strip(),
            x_handle=str(row.get("x_handle") or row.get("twitter") or "").strip(),
            source_url=str(row.get("source_url") or row.get("url") or "").strip(),
            region=str(row.get("region") or "").strip(),
            tags=split_list(row.get("tags")),
            priority=int(row.get("priority") or 3),
            notes=str(row.get("notes") or "").strip(),
        )


@dataclass(frozen=True)
class ScoredLead:
    """A source item with editorial priority signals attached."""

    source: SourceItem
    score: int
    category: str
    shift: str
    format_name: str
    reasons: list[str]


def load_source_registry(path: Path) -> list[MonitoredSource]:
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)

    raw_sources = payload.get("sources", payload if isinstance(payload, list) else [])
    if not isinstance(raw_sources, list):
        raise ValueError("source registry must be a list or an object with a sources list")

    return [MonitoredSource.from_mapping(row) for row in raw_sources]


def load_company_watchlist(path: Path) -> list[CompanyProfile]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open(encoding="utf-8") as file:
            payload = json.load(file)
        if not isinstance(payload, list):
            raise ValueError("company watchlist JSON must be a list")
        return [CompanyProfile.from_mapping(row) for row in payload]

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [CompanyProfile.from_mapping(row) for row in reader]


class ResearchEngine:
    """Prioritize sources and produce a media/research desk brief."""

    def __init__(self, content_engine: EverydayWeb3Engine) -> None:
        self.content_engine = content_engine

    def score_leads(self, sources: list[SourceItem], limit: int = 20) -> list[ScoredLead]:
        scored = [self.score_source(source) for source in sources]
        return sorted(scored, key=lambda lead: lead.score, reverse=True)[:limit]

    def score_source(self, source: SourceItem) -> ScoredLead:
        category = self.content_engine.classify_category(source)
        shift = self.content_engine.detect_shift(source)
        format_name = self.content_engine.pick_format(source, category, shift)
        reasons: list[str] = []
        score = source.priority * 10

        text = source.searchable_text
        matched_terms = [term for term in HIGH_SIGNAL_TERMS if term in text]
        if matched_terms:
            score += min(len(matched_terms), 5) * 4
            reasons.append(f"high-signal terms: {', '.join(matched_terms[:5])}")

        if source.url:
            score += 3
            reasons.append("has source link")

        if source.location:
            score += 4
            reasons.append("has IRL location")

        if source.event_date:
            score += 4
            reasons.append("has event date")

        if source.people:
            score += 3
            reasons.append("has creator/company/person angle")

        if shift == EVENING_SHIFT:
            score += 4
            reasons.append("fits new community/wellness track")

        if category in {"Shopping", "Mobile", "Food & Drinks", "Travel", "Health and Wellness"}:
            score += 3
            reasons.append("strong everyday adoption category")

        if not reasons:
            reasons.append("baseline editorial fit")

        return ScoredLead(
            source=source,
            score=score,
            category=category,
            shift=shift,
            format_name=format_name,
            reasons=reasons,
        )

    def build_daily_brief(
        self,
        run_date: date,
        leads: list[ScoredLead],
        registry: list[MonitoredSource],
        companies: list[CompanyProfile],
    ) -> str:
        lines = [
            f"# Everyday Web3 Research Brief - {run_date.isoformat()}",
            "",
            "Use this as the daily editorial queue before generating final posts.",
            "",
            "## Top leads to review",
            "",
        ]

        for index, lead in enumerate(leads[:10], start=1):
            source = lead.source
            url = f" ({source.url})" if source.url else ""
            lines.extend(
                [
                    f"### {index}. {source.title}",
                    f"- Score: {lead.score}",
                    f"- Category: {lead.category}",
                    f"- Shift: {lead.shift}",
                    f"- Suggested format: {lead.format_name}",
                    f"- Why it ranks: {'; '.join(lead.reasons)}",
                    f"- Summary: {source.summary or 'Add summary after review.'}{url}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Morning desk",
                "",
                self._shift_queue(leads, MORNING_SHIFT),
                "",
                "## Evening desk",
                "",
                self._shift_queue(leads, EVENING_SHIFT),
                "",
                "## Sources to check next",
                "",
            ]
        )

        for source in sorted(registry, key=lambda item: item.priority, reverse=True)[:12]:
            lines.append(
                f"- **{source.name}** [{source.source_type}] - {source.cadence}; plugin: {source.plugin}; {source.url}"
            )

        lines.extend(["", "## Company watchlist focus", ""])
        for company in sorted(companies, key=lambda item: item.priority, reverse=True)[:12]:
            handle = f" / {company.x_handle}" if company.x_handle else ""
            lines.append(
                f"- **{company.name}**{handle} - {company.category}; tags: {', '.join(company.tags) or 'add tags'}"
            )

        lines.extend(
            [
                "",
                "## Editor checklist",
                "",
                "- Confirm facts from the original source before publishing.",
                "- Capture screenshots or visuals for Pinterest/Instagram if the source is event or product-led.",
                "- Add one sentence answering: why does this matter to people outside crypto?",
                "- Save strong companies, founders, venues, and cities back into the watchlist.",
                "",
            ]
        )
        return "\n".join(lines)

    def build_source_map(self, registry: list[MonitoredSource]) -> str:
        lines = [
            "# Everyday Web3 Source Map",
            "",
            "| Source | Type | Track | Cadence | Plugin | Priority |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for source in sorted(registry, key=lambda item: (item.track, -item.priority, item.name.lower())):
            lines.append(
                f"| [{source.name}]({source.url}) | {source.source_type} | {source.track} | {source.cadence} | {source.plugin} | {source.priority} |"
            )
        lines.append("")
        return "\n".join(lines)

    def build_company_map(self, companies: list[CompanyProfile]) -> str:
        lines = [
            "# Everyday Web3 Company Watchlist",
            "",
            "| Company | Category | Region | X | Website/Source | Priority | Tags |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for company in sorted(companies, key=lambda item: (-item.priority, item.category, item.name.lower())):
            link = company.website or company.source_url
            lines.append(
                f"| {company.name} | {company.category} | {company.region} | {company.x_handle} | {link} | {company.priority} | {', '.join(company.tags)} |"
            )
        lines.append("")
        return "\n".join(lines)

    def build_scored_leads_csv(self, leads: list[ScoredLead]) -> str:
        rows = [
            [
                "score",
                "title",
                "category",
                "shift",
                "format",
                "location",
                "event_date",
                "url",
                "reasons",
            ]
        ]
        for lead in leads:
            source = lead.source
            rows.append(
                [
                    str(lead.score),
                    source.title,
                    lead.category,
                    lead.shift,
                    lead.format_name,
                    source.location,
                    source.event_date,
                    source.url,
                    "; ".join(lead.reasons),
                ]
            )

        return "\n".join(",".join(_csv_escape(cell) for cell in row) for row in rows) + "\n"

    def _shift_queue(self, leads: list[ScoredLead], shift: str) -> str:
        matching = [lead for lead in leads if lead.shift == shift][:5]
        if not matching:
            return "- No leads yet. Check the source map and add items to the source CSV."
        return "\n".join(
            f"- {lead.source.title} ({lead.category}, score {lead.score})" for lead in matching
        )


def _csv_escape(value: str) -> str:
    if any(char in value for char in [",", '"', "\n"]):
        return '"' + value.replace('"', '""') + '"'
    return value


def write_research_outputs(
    research_engine: ResearchEngine,
    sources: list[SourceItem],
    registry: list[MonitoredSource],
    companies: list[CompanyProfile],
    output_dir: Path,
    run_date: date,
    limit: int = 20,
) -> list[Path]:
    run_dir = output_dir / run_date.isoformat() / "research"
    run_dir.mkdir(parents=True, exist_ok=True)

    leads = research_engine.score_leads(sources, limit=limit)
    files = {
        "daily_research_brief.md": research_engine.build_daily_brief(run_date, leads, registry, companies),
        "source_map.md": research_engine.build_source_map(registry),
        "company_watchlist.md": research_engine.build_company_map(companies),
        "scored_leads.csv": research_engine.build_scored_leads_csv(leads),
    }

    written: list[Path] = []
    for filename, body in files.items():
        path = run_dir / slugify(filename.replace(".", "-"))
        if filename.endswith(".csv"):
            path = run_dir / filename
        else:
            path = run_dir / filename
        path.write_text(body, encoding="utf-8")
        written.append(path)

    return written
