# Everyday Web3 Product Plan

Everyday Web3 is an operator-first media and research engine for finding, scoring, drafting, scheduling, and learning from IRL Web3 stories.

## Product goal

Build a repeatable daily desk for the commerce, community, lifestyle, wellness, travel, mobile, art, event, and legal/tax sides of Web3: the products, places, people, and communities normal people can actually use.

## Target users

- Solo media operators publishing daily across X, LinkedIn, Instagram, Pinterest, Telegram, Discord, and a blog.
- Web3 researchers tracking companies, conferences, local meetups, creator wellness, and consumer adoption.
- Community leads and content strategists who need a daily editorial queue instead of scattered bookmarks.

## Operating loop

1. Collect leads from X lists, event directories, company sites, newsletters, community channels, and search discovery.
2. Run `python3 -m everyday_web3 daily` to dedupe sources, score leads, create research outputs, generate drafts, lint drafts, create the dashboard, and export scheduler CSV.
3. Review `output/YYYY-MM-DD/editorial_dashboard.md`.
4. Fact-check top morning and evening leads from original sources.
5. Fix missing links, dates, locations, media notes, and platform warnings.
6. Schedule approved drafts.
7. Add performance notes after publishing.
8. Use performance feedback to boost formats that deserve repurposing.

## Phase 1: Daily efficiency

- Add a one-command `daily` workflow.
- Create an editorial dashboard.
- Add draft linting and quality warnings.
- Add status, publish date, platform status, ownership, and performance fields to source inputs.

## Phase 2: Cleaner inputs

- Dedupe imported sources by URL or normalized title/date/location.
- Label source freshness as `today`, `this_week`, `upcoming_event`, `recent`, `stale`, `evergreen`, or `needs_date_review`.
- Estimate source quality from source type and URL.
- Surface missing-field warnings before publishing.

## Phase 3: Publishing workflow

- Export scheduler-ready CSV files.
- Document Notion and Airtable schemas.
- Provide import templates for editorial databases.
- Treat visual platform media notes and alt text as first-class production fields.

## Phase 4: Learning loop

- Capture impressions, engagements, clicks, saves, comments, winning hooks, and repurpose flags.
- Add prior performance feedback to lead scoring.
- Use performance notes to decide which formats should become weekly roundups, carousels, or evergreen blog posts.

## Near-term recommendations

1. Run the manual CSV workflow for a week to prove categories and formats.
2. Move sources into Notion or Airtable using the provided schemas.
3. Add Firecrawl/Exa only after the dashboard shows what information is repeatedly missing.
4. Add scheduler exports when the daily publishing cadence is stable.
5. Review performance every Friday and mark winners with `repurpose=yes`.
