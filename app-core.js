(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.EverydayWeb3 = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const requiredEventCategories = new Set(["events", "community", "travel", "wellness"]);

  function normalizeSource(source, index = 0) {
    return {
      id: source.id || `source-${Date.now()}-${index}`,
      title: String(source.title || "Untitled source").trim(),
      url: String(source.url || source.source_url || "").trim(),
      category: String(source.category || "community").trim().toLowerCase(),
      priority: Number(source.priority || 3),
      event_date: String(source.event_date || "").trim(),
      location: String(source.location || "").trim(),
      summary: String(source.summary || source.description || "").trim(),
      status: String(source.status || "new").trim().toLowerCase(),
      publish_date: String(source.publish_date || "").trim(),
      created_at: source.created_at || new Date().toISOString(),
    };
  }

  function scoreSource(source, now = new Date()) {
    let score = Math.min(40, Math.max(0, Number(source.priority || 0) * 8));
    if (source.url) score += 12;
    if (source.summary && source.summary.length >= 35) score += 12;
    if (source.location) score += 8;
    if (source.event_date) {
      const days = Math.ceil((new Date(`${source.event_date}T12:00:00`) - now) / 86400000);
      score += days >= 0 && days <= 30 ? 18 : 8;
    }
    if (["commerce", "lifestyle", "wellness", "events"].includes(source.category)) score += 8;
    return Math.min(100, score);
  }

  function needsDetails(source) {
    return !source.url || (requiredEventCategories.has(source.category) && (!source.event_date || !source.location));
  }

  function parseCsv(text) {
    const rows = [];
    let row = [], field = "", quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const char = text[i], next = text[i + 1];
      if (char === '"' && quoted && next === '"') { field += '"'; i += 1; }
      else if (char === '"') quoted = !quoted;
      else if (char === "," && !quoted) { row.push(field); field = ""; }
      else if ((char === "\n" || char === "\r") && !quoted) {
        if (char === "\r" && next === "\n") i += 1;
        row.push(field); if (row.some((value) => value.trim())) rows.push(row); row = []; field = "";
      } else field += char;
    }
    row.push(field); if (row.some((value) => value.trim())) rows.push(row);
    if (rows.length < 2) return [];
    const headers = rows[0].map((value) => value.trim().toLowerCase());
    return rows.slice(1).map((values, index) => normalizeSource(Object.fromEntries(headers.map((header, position) => [header, values[position] || ""])), index));
  }

  function escapeCsv(value) { return `"${String(value || "").replace(/"/g, '""')}"`; }
  function schedulerCsv(sources) {
    const header = ["platform", "scheduled_date", "status", "post_text", "source_url", "media_notes"];
    const rows = sources.filter((source) => source.publish_date).map((source) => ["multi-channel", source.publish_date, source.status, `${source.title}\n\n${source.summary}`, source.url, source.location ? `Location: ${source.location}` : ""]);
    return [header, ...rows].map((row) => row.map(escapeCsv).join(",")).join("\n");
  }

  return { normalizeSource, scoreSource, needsDetails, parseCsv, schedulerCsv };
});
