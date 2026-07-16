const test = require("node:test");
const assert = require("node:assert/strict");
const core = require("../app-core.js");

test("scores complete, timely sources above incomplete sources", () => {
  const now = new Date("2026-07-16T00:00:00Z");
  const complete = core.normalizeSource({ title:"Event", url:"https://example.com", category:"events", priority:5, event_date:"2026-07-20", location:"London", summary:"A detailed summary that explains why this event matters." });
  const incomplete = core.normalizeSource({ title:"Unknown", priority:1 });
  assert.ok(core.scoreSource(complete, now) > core.scoreSource(incomplete, now));
  assert.equal(core.needsDetails(complete), false);
});

test("parses quoted CSV fields", () => {
  const rows = core.parseCsv('title,url,category,summary\n"A launch, today",https://example.com,commerce,"Useful, local payments"\n');
  assert.equal(rows.length, 1);
  assert.equal(rows[0].title, "A launch, today");
  assert.equal(rows[0].summary, "Useful, local payments");
});

test("scheduler export includes only dated sources and escapes content", () => {
  const csv = core.schedulerCsv([{ title:'A "better" wallet', summary:"For shops", publish_date:"2026-07-18", status:"scheduled", url:"https://example.com", location:"Lagos" }, { title:"Later" }]);
  assert.match(csv, /2026-07-18/);
  assert.match(csv, /A ""better"" wallet/);
  assert.doesNotMatch(csv, /Later/);
});
