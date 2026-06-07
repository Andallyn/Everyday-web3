# Everyday Web3 Content Engine

A local-first content generator for the commerce, community, lifestyle, and wellness side of Web3 - the companies, events, creators, and products people can use in real life.

The engine turns a curated source list from X, Lu.ma, plan.wtf, Cryptonomads, conference notes, Telegram, or your own research into:

- Daily platform drafts for Twitter/X, LinkedIn, Pinterest, Instagram, Telegram, Discord, and blog posts
- A morning track for major Web3 news/events
- An evening track for community, wellness, retreats, co-working, local DAO, and burnout-prevention content
- A weekly "This Week in IRL Web3" roundup
- Source briefs with the engine's category classification

## Quick start

Run the sample generator:

```bash
python -m everyday_web3.cli generate \
  --input data/sources.sample.csv \
  --config config/everyday_web3.json \
  --output output \
  --date 2026-06-07
```

Generated files are written to `output/YYYY-MM-DD/`.

Show recommended workflow plugins:

```bash
python -m everyday_web3.cli plugins
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
3. Run the generator.
4. Review drafts in `output/YYYY-MM-DD/platforms/`.
5. Paste final versions into your scheduler or publishing tool.
6. Use `weekly_roundup.md` for "This Week in IRL Web3."

## Recommended plugins and integrations

The generator is built to stay useful before adding paid APIs. Start manually, then add integrations as the workflow becomes repeatable:

- X list/bookmark collector via X API, Readwise Reader, Zapier, or Apify
- Lu.ma, plan.wtf, Cryptonomads, conference, and hackathon event collectors
- Notion or Airtable editorial desk using the CSV fields as schema
- Buffer, Typefully, Hypefury, Publer, or similar scheduling tools
- Canva or Figma templates for Pinterest pins, Instagram carousels, and roundup graphics
- Zapier or Make automations that move saved links into your source spreadsheet

## Extending the engine

- Add categories, keywords, platform display names, and hashtags in `config/everyday_web3.json`.
- Add future collectors by implementing the plugin contract in `everyday_web3/plugins.py`.
- Add new platform rendering rules in `EverydayWeb3Engine.render_body`.

## Test

```bash
python -m unittest discover
```