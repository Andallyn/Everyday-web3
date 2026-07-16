# Everyday Web3 Content Engine

A local-first content generator for the commerce, community, lifestyle, and wellness side of Web3 - the companies, events, creators, and products people can use in real life.

This repository also includes a Vercel-ready static landing page at `index.html`.

The engine turns a curated source list from X, Lu.ma, plan.wtf, Cryptonomads, conference notes, Telegram, or your own research into:

- Daily platform drafts for Twitter/X, LinkedIn, Pinterest, Instagram, Telegram, Discord, and blog posts
- A morning track for major Web3 news/events
- An evening track for community, wellness, retreats, co-working, local DAO, and burnout-prevention content
- A weekly "This Week in IRL Web3" roundup
- Source briefs with the engine's category classification
- Daily research briefs, source maps, company watchlists, and scored editorial leads

## Quick start

Open the static landing page locally:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

Generate sample platform drafts:

```bash
python3 -m everyday_web3 generate \
  --input data/sources.sample.csv \
  --config config/everyday_web3.json \
  --output output \
  --date 2026-06-07
```

Generated files are written to `output/YYYY-MM-DD/`.

Generate the media/research desk brief:

```bash
python3 -m everyday_web3 research \
  --input data/sources.sample.csv \
  --registry config/source_registry.json \
  --watchlist data/company_watchlist.sample.csv \
  --output output \
  --date 2026-06-07
```

Research outputs are written to `output/YYYY-MM-DD/research/`.

Show recommended workflow plugins:

```bash
python3 -m everyday_web3 plugins
```

Show recommended MCP servers:

```bash
python3 -m everyday_web3 mcps
```

## Source input format

Create a CSV or JSON file with these fields:

| Field | Purpose |
| --- | --- |
| `title` | Source title, tweet/event headline, or working content idea |
| `url` | Link to X, Lu.ma, plan.wtf, Cryptonomads, article, or notes |
| `summary` | Short description of what happened |
| `category` | One of the Everyday Web3 buckets; can be blank for auto-classification |
| `source_type` | `post`, `article`, `event`, `meetup`, `conference`, etc. |
| `location` | City, country, online, remote, or blank |
| `event_date` | Date if relevant |
| `tags` | Comma-separated tags |
| `people` | Creator, founder, community, or company names |
| `priority` | 1-5; higher items are generated first |
| `notes` | Private editorial notes |

See `data/sources.sample.csv` for examples.

## Everyday Web3 buckets

The default taxonomy lives in `config/everyday_web3.json`:

- Travel
- Food & Drinks
- Real Estate
- Lifestyle & Events
- Shopping
- Mobile
- Health and Wellness
- Fitness
- Art & Luxury
- Collectibles
- Taxes
- Legal
- Hackathons
- Monthly Events

Edit keywords in the config to tune auto-classification.

## Daily workflow

1. Collect sources from your X list, bookmarks, Lu.ma, plan.wtf, Cryptonomads, newsletters, Telegram, and conference notes.
2. Add the best items to a CSV using the source input format.
3. Run `python3 -m everyday_web3 research` to score leads and create the daily research brief.
4. Pick the strongest morning and evening leads.
5. Run `python3 -m everyday_web3 generate` to create platform drafts.
6. Review drafts in `output/YYYY-MM-DD/platforms/`.
7. Paste final versions into your scheduler or publishing tool.
8. Use `weekly_roundup.md` for "This Week in IRL Web3."

## Media/research engine

The research layer is built around three files:

- `config/source_registry.json` - websites, X lists, conference pages, event directories, search layers, and derived company sources to monitor.
- `config/mcp_registry.json` - recommended MCPs for crawling, discovery, editorial ops, browser automation, and community inputs.
- `data/company_watchlist.sample.csv` - starter watchlist format for companies/accounts building IRL Web3 products.
- `data/sources.sample.csv` - daily leads that have been collected manually or by future plugins.

The default source registry includes your X list:

```text
https://x.com/i/lists/1970082106794442856
```

The research command creates:

- `daily_research_brief.md` - top leads, morning desk, evening desk, sources to check, and editor checklist
- `source_map.md` - monitoring plan for websites, feeds, lists, and event sources
- `company_watchlist.md` - watchlist grouped for editorial use
- `scored_leads.csv` - lead ranking with category, shift, format, and ranking reasons

Use this flow to track:

- Web3 conference sites and side-event directories
- Lu.ma, plan.wtf, Cryptonomads, ETHGlobal, ETHDenver, EthCC, Consensus, Token2049, and similar sources
- Company blogs, changelogs, newsletters, press pages, and X announcements
- Creator wellness retreats, local DAO meetups, co-working residencies, meditation/yoga sessions, and community rebuilds

## Recommended plugins and integrations

The generator is built to stay useful before adding paid APIs. Start manually, then add integrations as the workflow becomes repeatable:

- X list/bookmark collector via X API, Readwise Reader, Zapier, or Apify
- Lu.ma, plan.wtf, Cryptonomads, conference, and hackathon event collectors
- Notion or Airtable editorial desk using the CSV fields as schema
- Buffer, Typefully, Hypefury, Publer, or similar scheduling tools
- Canva or Figma templates for Pinterest pins, Instagram carousels, and roundup graphics
- Zapier or Make automations that move saved links into your source spreadsheet

See `docs/plugin_costs.md` for cost tiers and rollout recommendations.

## Recommended MCPs

The repo includes MCP recommendations and a Cursor config template:

- Registry: `config/mcp_registry.json`
- Setup guide: `docs/mcp_setup.md`
- Cursor template: `.cursor/mcp.example.json`

Recommended order:

1. Firecrawl MCP
2. Exa MCP
3. Notion MCP
4. Google Sheets MCP
5. Browserbase MCP
6. GitHub MCP
7. Airtable MCP
8. Discord MCP

To activate them locally, copy `.cursor/mcp.example.json` to `.cursor/mcp.json`, replace placeholders with your own keys, remove MCPs you are not ready to use, then restart Cursor. Do not commit real secrets.

## Extending the engine

- Add categories, keywords, platform display names, and hashtags in `config/everyday_web3.json`.
- Add future collectors by implementing the plugin contract in `everyday_web3/plugins.py`.
- Add new platform rendering rules in `EverydayWeb3Engine.render_body`.
- Add monitoring sources in `config/source_registry.json`.
- Add MCP recommendations in `config/mcp_registry.json`.
- Add companies from your X list to `data/company_watchlist.sample.csv` or your own watchlist file.

## Test

```bash
python3 -m unittest discover
```

## Use the web application

The Vercel deployment is now a functional, local-first personal editorial desk rather than a static marketing page. It supports:

- adding and removing research sources;
- automatic lead scoring and missing-detail warnings;
- a ranked daily priority queue;
- browser persistence between visits;
- CSV source imports and scheduler CSV exports; and
- one-click sample data for testing the workflow.

No account is required in this first usable release. Data is stored in the current browser's `localStorage`, so use CSV export for portable backups and do not expect data to sync across browsers or devices yet. The hosted-account and database path is documented in `plan.md`.

Run it locally with:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. The deployable web files are:

- `index.html`
- `styles.css`
- `app-core.js`
- `script.js`
- `vercel.json`

If `https://everyday-web3.vercel.app/` shows 404, the most likely causes are:

1. Vercel is still pointed at `main` before this branch has been merged.
2. The Vercel project is not connected to this GitHub repository.
3. A deployment has not been triggered yet.
4. The domain is attached to a different Vercel project.

codex/review-everyday-web3-for-improvements-ljlkif
Merge the feature branch into the branch Vercel tracks, then trigger a redeploy if automatic Git deployments are disabled.
Merge this branch or configure Vercel to deploy `cursor/everyday-web3-content-engine-4d63`, then trigger a redeploy.
main
## One-command daily desk

Run the full operator workflow when you want research, draft generation, quality checks, a dashboard, and a scheduler export in one pass:

```bash
python3 -m everyday_web3 daily \
  --input data/sources.sample.csv \
  --config config/everyday_web3.json \
  --registry config/source_registry.json \
  --watchlist data/company_watchlist.sample.csv \
  --output output \
  --date 2026-06-07
```

The daily command writes the normal research and platform outputs plus:

```text
output/YYYY-MM-DD/
├── editorial_dashboard.md
├── draft_quality_report.md
├── scheduler_export.csv
├── content_calendar.md
├── source_briefs.json
├── weekly_roundup.md
├── platforms/
└── research/
```

Use `editorial_dashboard.md` as the daily command center. It shows top leads, morning candidates, evening/community candidates, drafts ready to schedule, missing information warnings, and next actions.

## Draft quality checks

Preview production-readiness warnings without writing the full daily output:

```bash
python3 -m everyday_web3 lint-drafts \
  --input data/sources.sample.csv \
  --date 2026-06-07
```

The checker flags missing source links, missing event dates or locations, repeated hooks, overlong X thread segments, missing CTAs, and missing Pinterest alt text.

## Scheduler export

Create a scheduler-friendly CSV for tools such as Buffer, Typefully, Publer, Hypefury, Metricool, Later, or manual calendar upload:

```bash
python3 -m everyday_web3 export-scheduler \
  --input data/sources.sample.csv \
  --output output \
  --date 2026-06-07 \
  --scheduler buffer
```

The export includes platform, scheduled date, draft status, campaign, post text, source URL, and media notes.

## Editorial database fields

The source input supports operational fields beyond the original content fields:

| Field | Purpose |
| --- | --- |
| `status` | `new`, `reviewed`, `selected`, `drafted`, `scheduled`, `published`, or `archived` |
| `assigned_to` | Person responsible for the lead or draft |
| `publish_date` | Intended publication date |
| `platform_status` | Per-channel production notes |
| `performance_notes` | Qualitative notes after publishing |
| `impressions` | Reach after publishing |
| `engagements` | Likes, replies, comments, or reactions |
| `clicks` | Link clicks |
| `saves` | Saves/bookmarks, especially useful for Pinterest and Instagram |
| `comments` | Comment count or qualitative response volume |
| `winning_hook` | Hook that worked best |
| `repurpose` | Mark `yes` to boost this item for future reuse |

The research scorer now uses freshness, source quality, and performance feedback in addition to priority, high-signal keywords, links, locations, dates, people, and category fit.

## Editorial desk templates

Use these files to move from CSV to an operating database:

- `plan.md` - product roadmap and operating loop.
- `docs/notion_schema.md` - Notion database structure.
- `docs/airtable_schema.md` - Airtable table structure and views.
- `templates/notion_sources_import.csv` - starter import file.
- `templates/airtable_sources_import.csv` - starter import file.

Recommended rollout:

1. Run the manual CSV workflow for one week.
2. Move sources into Notion or Airtable once the statuses are clear.
3. Add Firecrawl and Exa after you know which sources need automation.
4. Use the scheduler export once the publishing cadence is stable.
5. Review performance weekly and mark winners with `repurpose=yes`.
