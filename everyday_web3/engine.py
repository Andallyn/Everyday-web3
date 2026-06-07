"""Generation logic for Everyday Web3 content."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

from .models import ContentIdea, GenerationContext, SourceItem


DEFAULT_HASHTAGS = ["#EverydayWeb3", "#IRLWeb3", "#Web3"]
DEFAULT_CATEGORY = "Lifestyle & Events"
MORNING_SHIFT = "Morning: major Web3 news/events"
EVENING_SHIFT = "Evening: community/wellness events"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "content"


def clean_hashtag(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]", "", value.title())
    return f"#{cleaned}" if cleaned else ""


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def load_sources(path: Path) -> list[SourceItem]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open(encoding="utf-8") as file:
            raw_items = json.load(file)
        if not isinstance(raw_items, list):
            raise ValueError("JSON source input must be a list of objects")
        return [SourceItem.from_mapping(item) for item in raw_items]

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [SourceItem.from_mapping(row) for row in reader]


class EverydayWeb3Engine:
    """Turn curated Everyday Web3 sources into platform-ready content."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.categories = config.get("categories", [])
        self.platforms = config.get("platforms", {})
        self.shifts = config.get("shifts", {})

    def generate(
        self,
        sources: list[SourceItem],
        context: GenerationContext,
        limit: int = 8,
    ) -> list[ContentIdea]:
        ranked_sources = sorted(sources, key=lambda item: item.priority, reverse=True)[:limit]
        ideas: list[ContentIdea] = []

        for source in ranked_sources:
            category = self.classify_category(source)
            shift = self.detect_shift(source)
            format_name = self.pick_format(source, category, shift)
            for platform in context.platforms:
                ideas.append(
                    self.create_platform_idea(
                        source=source,
                        category=category,
                        shift=shift,
                        format_name=format_name,
                        platform=platform,
                        context=context,
                    )
                )

        return ideas

    def classify_category(self, source: SourceItem) -> str:
        declared = source.category.strip().lower()
        for category in self.categories:
            name = category.get("name", "")
            if declared and declared == name.lower():
                return name

        best_category = DEFAULT_CATEGORY
        best_score = 0
        text = source.searchable_text
        for category in self.categories:
            score = 0
            for keyword in category.get("keywords", []):
                if keyword.lower() in text:
                    score += 1
            if score > best_score:
                best_category = category.get("name", DEFAULT_CATEGORY)
                best_score = score

        return best_category

    def detect_shift(self, source: SourceItem) -> str:
        text = source.searchable_text
        evening_keywords = self.shifts.get(
            "evening_keywords",
            ["wellness", "retreat", "burnout", "meditation", "yoga", "coworking"],
        )
        if any(keyword.lower() in text for keyword in evening_keywords):
            return EVENING_SHIFT

        if source.source_type.lower() in {"event", "meetup", "conference"} and "community" in text:
            return EVENING_SHIFT

        return MORNING_SHIFT

    def pick_format(self, source: SourceItem, category: str, shift: str) -> str:
        text = source.searchable_text
        if any(word in text for word in ["burnout", "recovery", "mental health"]):
            return "Burnout Prevention"
        if source.people and any(word in text for word in ["creator", "founder", "artist", "builder"]):
            return "Creator Spotlight"
        if any(word in text for word in ["dao", "community rebuild", "local community"]):
            return "Community Building"
        if source.location and any(word in text for word in ["meetup", "coworking", "residency"]):
            return "Local Alpha"
        if source.source_type.lower() in {"event", "meetup", "conference"} or source.event_date:
            return "Event Preview"
        if shift == EVENING_SHIFT or category in {"Health and Wellness", "Fitness"}:
            return "Community/Wellness Curation"
        return "Daily Recap"

    def create_platform_idea(
        self,
        source: SourceItem,
        category: str,
        shift: str,
        format_name: str,
        platform: str,
        context: GenerationContext,
    ) -> ContentIdea:
        platform_key = platform.lower().strip()
        title = f"{format_name}: {source.title}"
        hook = self.build_hook(source, category, format_name)
        angle = self.build_angle(source, category, shift)
        body = self.render_body(source, platform_key, format_name, category, shift, context)
        cta = self.cta_for(platform_key, format_name)
        hashtags = self.hashtags_for(category, platform_key)

        return ContentIdea(
            title=title,
            platform=self.platform_display_name(platform_key),
            category=category,
            format_name=format_name,
            shift=shift,
            hook=hook,
            angle=angle,
            body=body,
            cta=cta,
            hashtags=hashtags,
            sources=[source],
        )

    def build_hook(self, source: SourceItem, category: str, format_name: str) -> str:
        if format_name == "Burnout Prevention":
            return f"Web3 burnout is real, and {source.title} gives creators a practical reset point."
        if format_name == "Creator Spotlight":
            person = source.people[0] if source.people else "a Web3 creator"
            return f"{person} is showing what sustainable building in Web3 can look like offline."
        if format_name == "Local Alpha":
            place = f" in {source.location}" if source.location else ""
            return f"Local alpha{place}: this is where Web3 leaves the group chat and becomes useful."
        if format_name == "Event Preview":
            timing = f" on {source.event_date}" if source.event_date else ""
            return f"{source.title}{timing} belongs on your Everyday Web3 radar."
        if format_name == "Community Building":
            return f"{source.title} is a useful case study in rebuilding Web3 community IRL."
        return f"Everyday Web3 watch: {source.title} shows where crypto meets real life."

    def build_angle(self, source: SourceItem, category: str, shift: str) -> str:
        real_world_phrase = {
            "Travel": "travelers and nomads",
            "Food & Drinks": "restaurants, cafes, and hospitality",
            "Real Estate": "places people live, work, and gather",
            "Lifestyle & Events": "IRL communities",
            "Shopping": "consumer commerce",
            "Mobile": "apps people can use daily",
            "Health and Wellness": "creator sustainability",
            "Fitness": "movement and recovery",
            "Art & Luxury": "culture and ownership",
            "Collectibles": "fandom and physical-digital goods",
            "Taxes": "financial reality for crypto users",
            "Legal": "the rules that make adoption possible",
            "Hackathons": "builders shipping usable products",
            "Monthly Events": "the global event circuit",
        }.get(category, "real-world adoption")

        track = "community/wellness" if shift == EVENING_SHIFT else "news/events"
        return f"Frame this as {track} coverage for {real_world_phrase}, with the focus on usefulness instead of hype."

    def render_body(
        self,
        source: SourceItem,
        platform: str,
        format_name: str,
        category: str,
        shift: str,
        context: GenerationContext,
    ) -> str:
        summary = source.summary or "Add a short summary of what happened and why it matters."
        location = f"\nLocation: {source.location}" if source.location else ""
        event_date = f"\nDate: {source.event_date}" if source.event_date else ""
        source_line = f"\nSource: {source.url}" if source.url else ""

        if platform in {"x", "twitter"}:
            return self.render_x_thread(source, summary, category, format_name, location, event_date, source_line)
        if platform == "linkedin":
            return self.render_linkedin_post(source, summary, category, format_name, shift, source_line)
        if platform == "instagram":
            return self.render_instagram_carousel(source, summary, category, format_name)
        if platform == "pinterest":
            return self.render_pinterest_pin(source, summary, category, format_name)
        if platform in {"telegram", "discord"}:
            return self.render_community_post(source, summary, category, location, event_date, source_line)
        if platform == "blog":
            return self.render_blog_outline(source, summary, category, format_name, source_line)

        return "\n".join([source.title, "", summary, location, event_date, source_line]).strip()

    def render_x_thread(
        self,
        source: SourceItem,
        summary: str,
        category: str,
        format_name: str,
        location: str,
        event_date: str,
        source_line: str,
    ) -> str:
        return "\n\n".join(
            [
                f"1/ Everyday Web3: {source.title}",
                f"2/ Category: {category}. Format: {format_name}.",
                f"3/ What happened: {summary}",
                "4/ Why it matters: this is the commerce/lifestyle side of Web3 people can use in real life.",
                f"5/ Save this if you track IRL adoption.{location}{event_date}",
                f"6/ More details:{source_line or ' add source link here.'}",
            ]
        )

    def render_linkedin_post(
        self,
        source: SourceItem,
        summary: str,
        category: str,
        format_name: str,
        shift: str,
        source_line: str,
    ) -> str:
        return "\n\n".join(
            [
                f"{source.title} is a strong {format_name.lower()} for Everyday Web3.",
                summary,
                f"The useful angle: {category} is where Web3 becomes easier to understand because it touches normal behavior - travel, community, wellness, payments, ownership, or events.",
                f"Content track: {shift}.",
                "Post structure:\n- What happened\n- Who it helps\n- Why it matters outside crypto Twitter\n- What to watch next",
                source_line.strip() or "Source: add link",
            ]
        )

    def render_instagram_carousel(
        self,
        source: SourceItem,
        summary: str,
        category: str,
        format_name: str,
    ) -> str:
        return "\n".join(
            [
                "Slide 1: IRL Web3 worth knowing",
                f"Slide 2: {source.title}",
                f"Slide 3: Category - {category}",
                f"Slide 4: {summary}",
                "Slide 5: Why it matters - useful Web3 beats abstract Web3.",
                f"Slide 6: Save this for your {format_name.lower()} list.",
                "Caption: Real adoption looks like products, places, and communities people can actually use.",
            ]
        )

    def render_pinterest_pin(
        self,
        source: SourceItem,
        summary: str,
        category: str,
        format_name: str,
    ) -> str:
        board = "Everyday Web3 IRL"
        if category in {"Health and Wellness", "Fitness"}:
            board = "Web3 Creator Wellness"
        elif category in {"Travel", "Monthly Events", "Hackathons"}:
            board = "Web3 Cities, Conferences & Meetups"
        elif category in {"Art & Luxury", "Collectibles"}:
            board = "Web3 Culture, Art & Collectibles"

        return "\n".join(
            [
                f"Pin title: {source.title}",
                f"Board: {board}",
                f"Overlay text: {format_name} for IRL Web3",
                f"Description: {summary}",
                "Visual direction: use event photos, city details, product screenshots, or calm wellness imagery.",
                "Alt text: Everyday Web3 example showing real-world crypto adoption.",
            ]
        )

    def render_community_post(
        self,
        source: SourceItem,
        summary: str,
        category: str,
        location: str,
        event_date: str,
        source_line: str,
    ) -> str:
        return "\n".join(
            [
                f"Local alpha: {source.title}",
                f"Category: {category}",
                summary,
                location.strip(),
                event_date.strip(),
                "Why share it: useful for founders, creators, nomads, and community leads looking for IRL Web3 touchpoints.",
                source_line.strip() or "Source: add link",
            ]
        ).strip()

    def render_blog_outline(
        self,
        source: SourceItem,
        summary: str,
        category: str,
        format_name: str,
        source_line: str,
    ) -> str:
        return "\n".join(
            [
                f"# {source.title}",
                "",
                "## Opening thesis",
                f"This is an Everyday Web3 story because it turns {category.lower()} into a real-world adoption lens.",
                "",
                "## What happened",
                summary,
                "",
                "## Why it matters",
                "- Shows where Web3 touches normal life",
                "- Creates a bridge between crypto-native culture and mainstream behavior",
                "- Gives founders/operators a practical example to learn from",
                "",
                f"## Content format to repurpose",
                format_name,
                "",
                "## Source",
                source_line.replace("Source: ", "") or "Add link",
            ]
        )

    def cta_for(self, platform: str, format_name: str) -> str:
        if platform in {"x", "twitter"}:
            return "Reply with another Everyday Web3 example I should track."
        if platform == "linkedin":
            return "What real-world Web3 use case deserves more attention?"
        if platform == "pinterest":
            return "Save this to your IRL Web3 inspiration board."
        if platform in {"telegram", "discord"}:
            return "Drop a city or community event I should add to the next roundup."
        if platform == "blog":
            return "Subscribe for the weekly This Week in IRL Web3 roundup."
        if format_name == "Burnout Prevention":
            return "Share this with a creator who needs a reset."
        return "Follow for more Everyday Web3."

    def hashtags_for(self, category: str, platform: str) -> list[str]:
        configured = self.platforms.get(platform, {}).get("hashtags", DEFAULT_HASHTAGS)
        tags = list(dict.fromkeys(configured + [clean_hashtag(category)]))
        if platform in {"telegram", "discord"}:
            return tags[:3]
        return tags[:5]

    def platform_display_name(self, platform: str) -> str:
        return self.platforms.get(platform, {}).get("display_name", platform.title())

    def build_calendar_markdown(self, ideas: list[ContentIdea], run_date: date) -> str:
        lines = [
            f"# Everyday Web3 Content Calendar - {run_date.isoformat()}",
            "",
            "| Shift | Category | Platform | Format | Idea |",
            "| --- | --- | --- | --- | --- |",
        ]
        for idea in ideas:
            lines.append(
                f"| {idea.shift} | {idea.category} | {idea.platform} | {idea.format_name} | {idea.title} |"
            )
        lines.append("")
        return "\n".join(lines)

    def build_weekly_roundup(self, sources: list[SourceItem], run_date: date) -> str:
        grouped: dict[str, list[SourceItem]] = defaultdict(list)
        for source in sorted(sources, key=lambda item: item.priority, reverse=True):
            grouped[self.detect_shift(source)].append(source)

        lines = [
            f"# This Week in IRL Web3 - {run_date.isoformat()}",
            "",
            "A combined roundup for the commerce, community, and wellness side of Web3.",
            "",
        ]
        for shift in [MORNING_SHIFT, EVENING_SHIFT]:
            lines.extend([f"## {shift}", ""])
            if not grouped.get(shift):
                lines.extend(["- Add curated sources for this track.", ""])
                continue
            for source in grouped[shift][:5]:
                category = self.classify_category(source)
                summary = source.summary or "Add summary."
                url = f" ({source.url})" if source.url else ""
                lines.append(f"- **{category}: {source.title}** - {summary}{url}")
            lines.append("")

        lines.extend(
            [
                "## Suggested CTA",
                "Which IRL Web3 product, event, or creator wellness space should be in next week's roundup?",
                "",
            ]
        )
        return "\n".join(lines)

    def dump_source_briefs(self, sources: list[SourceItem]) -> str:
        payload = [asdict(source) | {"classified_category": self.classify_category(source)} for source in sources]
        return json.dumps(payload, indent=2)


def write_generation_outputs(
    engine: EverydayWeb3Engine,
    sources: list[SourceItem],
    ideas: list[ContentIdea],
    output_dir: Path,
    run_date: date,
    include_weekly: bool = True,
) -> list[Path]:
    run_dir = output_dir / run_date.isoformat()
    platform_dir = run_dir / "platforms"
    platform_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []

    calendar_path = run_dir / "content_calendar.md"
    calendar_path.write_text(engine.build_calendar_markdown(ideas, run_date), encoding="utf-8")
    written.append(calendar_path)

    briefs_path = run_dir / "source_briefs.json"
    briefs_path.write_text(engine.dump_source_briefs(sources), encoding="utf-8")
    written.append(briefs_path)

    by_platform: dict[str, list[ContentIdea]] = defaultdict(list)
    for idea in ideas:
        by_platform[slugify(idea.platform)].append(idea)

    for platform, platform_ideas in by_platform.items():
        body = "\n---\n\n".join(idea.to_markdown() for idea in platform_ideas)
        platform_path = platform_dir / f"{platform}.md"
        platform_path.write_text(body, encoding="utf-8")
        written.append(platform_path)

    if include_weekly:
        roundup_path = run_dir / "weekly_roundup.md"
        roundup_path.write_text(engine.build_weekly_roundup(sources, run_date), encoding="utf-8")
        written.append(roundup_path)

    return written
