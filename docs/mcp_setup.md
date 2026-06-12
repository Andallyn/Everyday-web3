# Everyday Web3 MCP Setup

MCPs let Cursor connect the Everyday Web3 engine to external research and workflow tools. They are useful once you want the engine to monitor sites, search the web, work with an editorial database, or collect community submissions.

## Recommended order

1. **Firecrawl MCP** - crawl conference pages, event directories, company blogs, changelogs, and press pages.
2. **Exa MCP** - discover new IRL Web3 events, product announcements, wellness retreats, and local alpha.
3. **Notion MCP** - run the editorial desk: source links, category, status, hooks, publish dates, and performance notes.
4. **Google Sheets MCP** - lightweight spreadsheet database that exports cleanly to the generator's CSV format.
5. **Browserbase MCP** - dynamic pages, screenshots, conference schedules, and pages simple crawlers cannot parse.
6. **GitHub MCP** - repo issues, PR context, roadmap, and engine development workflow.
7. **Airtable MCP** - structured source registry, company watchlist, content calendar, and performance metrics.
8. **Discord MCP** - community-submitted links, private research channels, and event suggestions.

## Safe setup

This repo includes a template:

```text
.cursor/mcp.example.json
```

To activate it locally:

```bash
cp .cursor/mcp.example.json .cursor/mcp.json
```

Then:

1. Replace every `YOUR_...` placeholder with your own keys.
2. Remove MCPs you are not using yet.
3. Do **not** commit `.cursor/mcp.json` if it contains real secrets.
4. Restart Cursor.
5. Open Cursor Settings -> Tools & MCP and confirm each server is connected.

The committed file is an example only, so the project does not try to start broken MCP servers during deployment.

## CLI helpers

Show the recommended MCP stack:

```bash
python3 -m everyday_web3 mcps
```

Output the registry as JSON:

```bash
python3 -m everyday_web3 mcps --format json
```

Print a Cursor config template:

```bash
python3 -m everyday_web3 mcps --format cursor-config
```

## Where each MCP fits

| MCP | Everyday Web3 use |
| --- | --- |
| Firecrawl | Lu.ma, plan.wtf, Cryptonomads, conference sites, company blogs, changelogs |
| Exa | Discovery searches for retreats, meetups, city guides, product launches, and IRL Web3 news |
| Notion | Editorial database and content calendar |
| Google Sheets | Simple source spreadsheet and CSV export |
| Browserbase | Dynamic sites, browser screenshots, complex conference schedules |
| GitHub | Issues, PRs, roadmap, and engine maintenance |
| Airtable | Structured media database and performance tracking |
| Discord | Community submissions and private research brief channels |

## Security notes

- Treat MCP tokens like production API keys.
- Prefer least-privilege tokens.
- Keep secrets in local Cursor config, not committed repo files.
- If an MCP can write data, test it on a small database/server first.
- Disable MCPs you do not actively need; fewer connected tools means fewer accidental actions.
