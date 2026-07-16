"""Operational helpers for the Everyday Web3 editorial workflow."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date, datetime
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

from .engine import EVENING_SHIFT, MORNING_SHIFT, EverydayWeb3Engine
from .models import ContentIdea, SourceItem
from .research import ScoredLead


@dataclass(frozen=True)
class DraftIssue:
    """A production-readiness warning for a generated draft."""

    severity: str
    platform: str
    title: str
    message: str


def source_identity(source: SourceItem) -> str:
    """Build a stable identity key for deduping imported leads."""

    if source.url:
        parsed = urlparse(source.url.strip().lower())
        return f"url:{parsed.netloc}{parsed.path}".rstrip("/")
    normalized_title = re.sub(r"[^a-z0-9]+", " ", source.title.lower()).strip()
    return f"title:{normalized_title}|date:{source.event_date}|place:{source.location.lower()}"


def dedupe_sources(sources: list[SourceItem]) -> list[SourceItem]:
    """Keep the highest-priority source for each normalized URL/title identity."""

    by_key: dict[str, SourceItem] = {}
    for source in sources:
        key = source_identity(source)
        current = by_key.get(key)
        if current is None or source.priority > current.priority:
            by_key[key] = source
    return sorted(by_key.values(), key=lambda item: item.priority, reverse=True)


def freshness_label(source: SourceItem, run_date: date) -> str:
    """Classify source freshness for editorial prioritization."""

    if not source.event_date:
        return "evergreen"
    try:
        event_date = date.fromisoformat(source.event_date[:10])
    except ValueError:
        return "needs_date_review"

    delta = (event_date - run_date).days
    if delta < -14:
        return "stale"
    if delta < 0:
        return "recent"
    if delta == 0:
        return "today"
    if delta <= 7:
        return "this_week"
    return "upcoming_event"


def build_editorial_dashboard(
    run_date: date,
    leads: list[ScoredLead],
    ideas: list[ContentIdea],
    issues: list[DraftIssue],
) -> str:
    """Render a one-page daily command center for the operator."""

    morning = [lead for lead in leads if lead.shift == MORNING_SHIFT][:5]
    evening = [lead for lead in leads if lead.shift == EVENING_SHIFT][:5]
    ready = [
        idea
        for idea in ideas
        if not any(
            issue.title == idea.title and issue.severity == "error" for issue in issues
        )
    ]

    lines = [
        f"# Everyday Web3 Editorial Dashboard - {run_date.isoformat()}",
        "",
        "Use this file as today's single operating view: pick leads, fix warnings, then schedule approved drafts.",
        "",
        "## Today's top leads",
        "",
    ]
    for index, lead in enumerate(leads[:5], start=1):
        lines.append(
            f"{index}. **{lead.source.title}** — score {lead.score}; {lead.category}; {lead.format_name}; freshness: {lead.freshness}"
        )
    if not leads:
        lines.append("- Add sources to the input CSV, then rerun the daily command.")

    lines.extend(["", "## Morning candidates", ""])
    lines.extend(_lead_lines(morning))
    lines.extend(["", "## Evening/community candidates", ""])
    lines.extend(_lead_lines(evening))

    lines.extend(["", "## Drafts ready to schedule", ""])
    for idea in ready[:12]:
        lines.append(f"- **{idea.platform}:** {idea.title}")
    if not ready:
        lines.append("- No ready drafts yet; resolve lint issues first.")

    lines.extend(["", "## Missing info and quality warnings", ""])
    for issue in issues[:20]:
        lines.append(
            f"- **{issue.severity.upper()}** [{issue.platform}] {issue.title}: {issue.message}"
        )
    if not issues:
        lines.append("- No blocking warnings found in generated drafts.")

    lines.extend(
        [
            "",
            "## Suggested next actions",
            "",
            "1. Fact-check the top morning and evening leads from original sources.",
            "2. Add missing links, dates, locations, or alt text flagged above.",
            "3. Export scheduler CSV and assign publish times.",
            "4. After publishing, add impressions, clicks, saves, comments, and winning hooks to performance notes.",
            "",
        ]
    )
    return "\n".join(lines)


def _lead_lines(leads: list[ScoredLead]) -> list[str]:
    if not leads:
        return ["- No candidates yet."]
    return [
        f"- {lead.source.title} ({lead.category}, score {lead.score}, {lead.freshness})"
        for lead in leads
    ]


def lint_ideas(ideas: list[ContentIdea]) -> list[DraftIssue]:
    """Check drafts for production-readiness issues."""

    issues: list[DraftIssue] = []
    seen_hooks: set[str] = set()
    for idea in ideas:
        title = idea.title
        platform = idea.platform
        source = idea.sources[0] if idea.sources else None
        if source and not source.url:
            issues.append(DraftIssue("warning", platform, title, "missing source link"))
        if (
            source
            and source.source_type.lower() in {"event", "meetup", "conference"}
            and not source.event_date
        ):
            issues.append(
                DraftIssue(
                    "warning",
                    platform,
                    title,
                    "event-style source is missing an event_date",
                )
            )
        if (
            source
            and source.source_type.lower() in {"event", "meetup", "conference"}
            and not source.location
        ):
            issues.append(
                DraftIssue(
                    "warning",
                    platform,
                    title,
                    "event-style source is missing a location",
                )
            )
        if not idea.cta.strip():
            issues.append(DraftIssue("error", platform, title, "missing CTA"))
        if platform == "Twitter/X":
            for segment in idea.body.split("\n\n"):
                if len(segment) > 280:
                    issues.append(
                        DraftIssue(
                            "warning",
                            platform,
                            title,
                            "X thread segment is over 280 characters",
                        )
                    )
                    break
        if platform == "Pinterest" and "Alt text:" not in idea.body:
            issues.append(
                DraftIssue(
                    "warning", platform, title, "Pinterest draft is missing alt text"
                )
            )
        source_title = source.title.lower() if source else title.lower()
        hook_key = re.sub(r"\s+", " ", f"{idea.hook.lower()}|{source_title}").strip()
        if hook_key in seen_hooks and idea.platform == "Twitter/X":
            issues.append(
                DraftIssue("warning", platform, title, "hook is repeated across drafts")
            )
        seen_hooks.add(hook_key)
    return issues


def render_lint_report(issues: list[DraftIssue]) -> str:
    lines = ["# Everyday Web3 Draft Quality Report", ""]
    if not issues:
        lines.append("No draft quality issues found.")
    else:
        lines.extend(
            ["| Severity | Platform | Draft | Issue |", "| --- | --- | --- | --- |"]
        )
        for issue in issues:
            lines.append(
                f"| {issue.severity} | {issue.platform} | {issue.title} | {issue.message} |"
            )
    lines.append("")
    return "\n".join(lines)


def build_scheduler_csv(
    ideas: list[ContentIdea], run_date: date, scheduler: str = "generic"
) -> str:
    """Export drafts in a scheduler-friendly CSV shape."""

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "scheduler",
            "platform",
            "scheduled_date",
            "status",
            "campaign",
            "post_text",
            "source_url",
            "media_notes",
        ]
    )
    for idea in ideas:
        source = idea.sources[0] if idea.sources else None
        source_url = source.url if source else ""
        media_notes = ""
        if idea.platform in {"Instagram", "Pinterest"}:
            media_notes = (
                "Create carousel/pin from visual direction and include alt text."
            )
        writer.writerow(
            [
                scheduler,
                idea.platform,
                run_date.isoformat(),
                "draft",
                "Everyday Web3",
                idea.body,
                source_url,
                media_notes,
            ]
        )
    return buffer.getvalue()


def write_text(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path
