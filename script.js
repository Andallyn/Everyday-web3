const STORAGE_KEY = "everyday-web3-workspace-v1";
const core = window.EverydayWeb3;
const sampleSources = [
  { title:"Stablecoin checkout launches for independent shops", url:"https://example.com/stablecoin-checkout", category:"commerce", priority:5, summary:"A point-of-sale product lets local merchants accept stablecoins and settle in their preferred currency.", status:"reviewed" },
  { title:"ETH community residency opens applications", url:"https://example.com/residency", category:"community", priority:4, event_date:"2026-08-12", location:"Lisbon, Portugal", summary:"A two-week builder residency combines coworking, local events, and public workshops for consumer crypto teams.", status:"new" },
  { title:"Onchain wellness retreat announced", url:"https://example.com/retreat", category:"wellness", priority:4, event_date:"2026-09-05", location:"Costa Rica", summary:"A token-gated retreat is testing portable membership for wellness programming and community access.", status:"selected", publish_date:"2026-07-18" },
];
let sources = loadSources();

function loadSources() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]").map(core.normalizeSource); }
  catch (_) { return []; }
}
function saveSources(message = "Workspace saved") {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sources));
  document.querySelector("#save-state").textContent = `Saved locally · ${new Date().toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" })}`;
  if (message) toast(message);
  render();
}
function toast(message) {
  const element = document.querySelector("#toast"); element.textContent = message; element.classList.add("show");
  window.clearTimeout(toast.timer); toast.timer = window.setTimeout(() => element.classList.remove("show"), 2200);
}
function escapeHtml(value) { const node = document.createElement("span"); node.textContent = value; return node.innerHTML; }
function ranked() { return [...sources].sort((a,b) => core.scoreSource(b) - core.scoreSource(a)); }
function render() {
  const scored = sources.map((source) => ({ ...source, score:core.scoreSource(source) }));
  document.querySelector("#metric-sources").textContent = sources.length;
  document.querySelector("#metric-ready").textContent = scored.filter((source) => source.score >= 60).length;
  document.querySelector("#metric-scheduled").textContent = sources.filter((source) => source.publish_date).length;
  document.querySelector("#metric-needs").textContent = sources.filter(core.needsDetails).length;
  const queue = document.querySelector("#queue");
  if (!sources.length) { queue.className = "queue empty-state"; queue.innerHTML = "<p>Add a source or load the sample data to build your desk.</p>"; }
  else {
    queue.className = "queue";
    queue.innerHTML = ranked().slice(0,5).map((source) => `<article class="lead-card"><span class="score">${core.scoreSource(source)}</span><div><h3>${escapeHtml(source.title)}</h3><p>${escapeHtml(source.summary || "Add a summary before publishing this story.")}</p><span class="tag">${escapeHtml(source.category)}</span>${core.needsDetails(source) ? '<span class="tag">needs details</span>' : ""}</div><div class="lead-actions"><button class="icon-button" data-schedule="${source.id}" title="Schedule for tomorrow">＋ date</button></div></article>`).join("");
  }
  document.querySelector("#source-table").innerHTML = ranked().map((source) => `<tr><td>${escapeHtml(source.title)}</td><td>${escapeHtml(source.category)}</td><td><span class="status">${escapeHtml(source.status)}</span></td><td>${core.scoreSource(source)}</td><td>${escapeHtml(source.publish_date || "—")}</td><td><button class="icon-button" data-delete="${source.id}" aria-label="Delete ${escapeHtml(source.title)}">Delete</button></td></tr>`).join("") || '<tr><td colspan="6">No sources yet.</td></tr>';
}
document.querySelector("#source-form").addEventListener("submit", (event) => {
  event.preventDefault(); const values = Object.fromEntries(new FormData(event.currentTarget)); sources.unshift(core.normalizeSource(values)); event.currentTarget.reset(); saveSources("Source added");
});
document.querySelector("#load-sample").addEventListener("click", () => { sources = sampleSources.map(core.normalizeSource); saveSources("Sample workspace loaded"); });
document.querySelector("#generate-desk").addEventListener("click", () => { render(); document.querySelector("#queue").scrollIntoView({ behavior:"smooth", block:"center" }); toast(`Desk generated from ${sources.length} sources`); });
document.querySelector("#clear-data").addEventListener("click", () => { if (window.confirm("Clear all sources stored in this browser?")) { sources = []; saveSources("Workspace cleared"); } });
document.querySelector("#csv-import").addEventListener("change", async (event) => { const file = event.target.files[0]; if (!file) return; const imported = core.parseCsv(await file.text()); sources = [...imported, ...sources]; saveSources(`${imported.length} sources imported`); event.target.value = ""; });
document.addEventListener("click", (event) => {
  const deleteId = event.target.dataset.delete, scheduleId = event.target.dataset.schedule;
  if (deleteId) { sources = sources.filter((source) => source.id !== deleteId); saveSources("Source removed"); }
  if (scheduleId) { const tomorrow = new Date(Date.now()+86400000).toISOString().slice(0,10); sources = sources.map((source) => source.id === scheduleId ? { ...source, publish_date:tomorrow, status:"scheduled" } : source); saveSources("Added to tomorrow's schedule"); }
});
document.querySelector("#export-csv").addEventListener("click", () => {
  const csv = core.schedulerCsv(sources); if (!sources.some((source) => source.publish_date)) { toast("Schedule at least one source first"); return; }
  const link = document.createElement("a"); link.href = URL.createObjectURL(new Blob([csv], { type:"text/csv" })); link.download = `everyday-web3-schedule-${new Date().toISOString().slice(0,10)}.csv`; link.click(); URL.revokeObjectURL(link.href); toast("Scheduler CSV downloaded");
});
render();
