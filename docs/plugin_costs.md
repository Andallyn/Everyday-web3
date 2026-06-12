# Plugin and Marketplace Cost Guide

From the code side, the generator can support these integrations without adding paid dependencies to the repository. The actual cost comes from the third-party services you connect, how much you crawl, and whether you need official APIs.

Prices change often, so treat the ranges below as planning guidance rather than quotes.

## Recommended setup by budget

### Starter: manual plus low-cost automation

Estimated external cost: **$0-$50/month**

- Google Sheets or Notion as the source database
- Manual CSV export into this generator
- RSS/feed reader for company blogs and newsletters
- Manual review of the X list and saved bookmarks
- Free/low-tier scheduler for posts

Best when: you want to keep costs low while proving which content formats work.

### Operator: automated discovery and scheduling

Estimated external cost: **$50-$250/month**

- Firecrawl or similar web crawler for event/company pages
- Exa/Tavily-style search for discovery queries
- Zapier/Make for moving saved links into the source database
- Typefully/Buffer/Publer/Hypefury for scheduling
- Notion or Airtable editorial desk

Best when: you are publishing daily and need fewer manual tabs open.

### Media desk: high-volume monitoring

Estimated external cost: **$250-$1,000+/month**

- Apify or scraping actors for X/list monitoring where API access is limited
- Firecrawl at higher volume for conference and company websites
- Search API usage for daily discovery across cities/categories
- Airtable/Notion plus automations
- Social scheduling across X, LinkedIn, Instagram, Pinterest, Telegram, and Discord
- Optional managed database/hosting if the generator becomes a web app

Best when: Everyday Web3 becomes a serious publication/research product.

## Plugin recommendations

| Plugin category | Why it matters | Cost sensitivity |
| --- | --- | --- |
| X list collector | Your X list is the core proprietary signal layer for 200+ IRL/lifestyle companies. | Can be expensive or limited if using official API; Apify/scraping also has usage costs and policy considerations. |
| Firecrawl/web crawler | Tracks Lu.ma, plan.wtf, Cryptonomads, conference sites, company blogs, and changelogs. | Depends on crawl volume and frequency. |
| Exa/Tavily search | Finds new wellness retreats, DAO meetups, local alpha, and product announcements outside your known list. | Depends on query volume. |
| RSS/feed reader | Cheap way to track blogs, newsletters, press pages, and changelogs. | Usually low-cost; some sources need RSSHub/custom feeds. |
| Notion/Airtable | Editorial command center for sources, hooks, status, publish dates, and performance. | Low to moderate depending on team size and automation needs. |
| Zapier/Make | Moves saved links/bookmarks/forms into the source database. | Costs rise with task volume. |
| Scheduler | Publishes or queues X threads, LinkedIn posts, Instagram captions, Pinterest pins, and community notes. | Depends on number of channels and accounts. |
| Canva/Figma | Turns generated visual direction into repeatable templates. | Usually low to moderate. |

## My recommendation

Start with the **Operator** setup, but roll it out in this order:

1. Notion or Airtable editorial desk.
2. RSS/feed tracking for blogs, changelogs, and newsletters.
3. Firecrawl for event and conference websites.
4. Exa or Tavily for discovery searches.
5. X list collector through the most reliable compliant route available to you.
6. Scheduler once the daily/weekly formats are stable.

This avoids paying for heavy X or crawling infrastructure before the content pipeline is proven.
