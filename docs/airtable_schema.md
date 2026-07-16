# Airtable Editorial Desk Schema

Recommended Airtable tables:

1. Sources
2. Content Drafts
3. Publishing Calendar
4. Companies
5. Performance

## Sources table fields

Use the columns from `templates/airtable_sources_import.csv`: title, url, summary, category, source_type, location, event_date, tags, people, priority, notes, status, assigned_to, publish_date, platform_status, performance_notes, impressions, engagements, clicks, saves, comments, winning_hook, repurpose.

## Suggested views

- New Leads: `status = new`
- Today: `publish_date = today`
- Needs Info: empty URL, event date, or summary
- Ready to Schedule: `status = drafted`
- Published Winners: `repurpose = yes`

## Automations

- When status becomes `selected`, create draft records for target platforms.
- When status becomes `published`, create or update a performance record.
- When `repurpose = yes`, add the item to the weekly roundup queue.
