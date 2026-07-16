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
codex/review-everyday-web3-for-improvements-ljlkif

## Web application roadmap

The deployed product now starts as a **local-first personal desk**, not a brochure. This makes it useful immediately without requiring accounts or paid infrastructure: sources, statuses, and dates persist in the operator's browser, while CSV import and scheduler export keep the data portable.

### Release A: personal desk (current)

- Capture, review, score, schedule, and delete sources in the browser.
- Persist the workspace with browser storage and clearly communicate where data is saved.
- Import the existing source CSV format and export scheduled work as CSV.
- Keep the Python CLI as the advanced batch workflow and scoring reference.

### Release B: private cloud workspace

- Add email or passkey authentication and per-user workspaces.
- Store sources, drafts, schedules, and audit history in Postgres.
- Add a server API with schema validation, migrations, encrypted secrets, backups, and rate limits.
- Sync browser and CLI data through the same API while preserving CSV backup/export.

### Release C: automated research

- Run scheduled collectors for RSS, company sites, event listings, Firecrawl, and Exa.
- Add source provenance, duplicate review, collection health, and fact-check states.
- Move scoring rules into a shared, versioned service so browser and CLI rankings agree.
- Notify the operator about high-confidence leads instead of auto-publishing them.

### Release D: publishing and learning

- Add a rich draft editor, reusable templates, media assets, alt text, and approvals.
- Integrate publishing providers behind explicit review and confirmation steps.
- Ingest channel analytics and connect performance to source, hook, format, and campaign.
- Add team roles only after the personal workflow is stable and used consistently.

### Product safeguards

- Never store third-party API keys in browser code or the repository.
- Keep human approval between generated copy and publishing.
- Record original URLs and collection times for fact-checking and corrections.
- Provide complete data export and account deletion before introducing hosted accounts.
=======
main
