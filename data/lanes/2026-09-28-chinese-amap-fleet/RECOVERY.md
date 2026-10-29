# Hunt Recovery Guide — 2026-10-05

Everything running for the Chinese Amap fleet / agent-swarm hunt, and how to restart it after a VM outage. All state lives under `~/workspace` (persists). Nothing critical lives in `/tmp`.

## Durable scheduled jobs (survive VM restarts via runtime)

| Job | ID | Cadence | Purpose |
|---|---|---|---|
| Hunt watch | `chinese-fleet-hunt-watch` | 45 min | Progress check-ins on the fleet hunt |
| UA burst retry | `ua-burst-retry` | 30 min | One authenticated API attempt per run for the Sep 29 httpbin UA burst; saves to `ua-burst-2026-09-29.json`, logs to `live-monitor/LOG.md`, disables itself on success |
| Hunt watchdog | `hunt-watchdog` | 1 hour | Verifies hunt agents + crons alive, respawns dead agents from this crib, quiet when healthy |

Check with `cron.list` / `cron.status`. If a job is missing, recreate from the descriptions above.

## Subagents (runtime-managed recovery)

| Agent | Task | Output |
|---|---|---|
| Live monitor | Poll urlquery via keyless htmx (`uq_htmx.py`), track new tag words/task families (currently: museum family) | `live-monitor/LOG.md` |
| Farmable surfaces | Sweep urlquery alternatives (urlscan, OTX, VT, ANY.RUN, Hybrid Analysis) for agent/swarm BEHAVIOR; foreign-TLD sweep | `farmable-surfaces/FINDINGS.md` |
| New fleets | Burst detection over recent urlquery submissions via htmx; exclude known `uq` operator; grade new clusters | `new-fleets/FINDINGS.md` |
| Full-sweep coordinator | Fans out per-surface subagents: web archives, CT, pastes, GitHub, social, Shodan/FOFA, corpus re-mine, non-Western (ZoomEye/Quake/ThreatBook/Baidu/Yandex/Megalodon/Naver), 12 trick classes (proxies, scanners, tunnels, shorteners, dead-drops, pastes, archives, screenshots, staged programs, file drops, intel DBs, messaging) | `full-sweep/FINDINGS.md` |
| cachedview deep-scan coordinator | 7-angle fan-out: service recon, urlquery+urlscan mining, sibling archive-oracles, oracle-as-proxy tradecraft, jmail.world follow-up, attribution shape | `cachedview/FINDINGS.md` |
| 10 persona hunters | Metronome (timing), Grammarian (tag grammars), Tracker (infrastructure), Profiler (submitters), Cartographer (targets), Night Owl (work patterns/TZ), Contrarian (misfits), Mimic (predict operator's next), Auditor (detection workloads), Historian (campaign timelines) | `personas/<name>/FINDINGS.md` |
| 4 more personas | OSINT Expert (disclosures/chatter), Model Whisperer (model attribution), Trade Labourer (infra supply chain), Codebreaker (encoding/obfuscation) | `personas/<name>/FINDINGS.md` |
| 10 agent-focused personas (not operators) | Global South Scout, Polyglot, Toolmark Reader, Toddler Watcher, Ghost Hunter, Forager, Scavenger, Apprentice, Border Crosser, Librarian | `personas/<name>/FINDINGS.md` |
| 7 culture/language/eval personas | Cultural Anthropologist (East Asia), Cultural Anthropologist (Global), Linguist (Chinese), Linguist (Multilingual), Harness Researcher (fragment→harness lookup), Eval Coordinator (trace→eval-question linkage), OSINT Codebreaker (uploaded eval info) — each may fan out further | `personas/<name>/FINDINGS.md` |

Standing doctrines (BigSexyWarlock69): metadata tells the story; misfits are leads, never negatives; agents and swarms only; no API key is not a stop (read source, find the XHR); document every undocumented endpoint for reuse.

If an agent is gone after restart, respawn with the task + output path from the table. State files in each output dir let a fresh agent resume.

## Killed / converted

- `proc_a0bc991c6a6a` (UA burst retry loop, background exec) — killed 2026-10-05, replaced by `ua-burst-retry` cron. Do not rerun as exec.
- **TEARDOWN 2026-10-05 09:30 CDT (BigSexyWarlock69: "tear down all of the watchers for this. Unnheist too")** — all fleet-hunt watchers disabled, not deleted (definitions kept, re-enable anytime):
  - `chinese-fleet-hunt-watch` (45m), `ua-burst-retry` (30m), `infra-watchlist-refresh` (6h), `hunt-watchdog` (1h) — goal-owned, disabled.
  - `methodology-refresh` (1h), `lessons-refresh` (1h) — disabled.
  - `un-heist-render-watch` (15m) — the UN Heist render watchdog, disabled.
  - Detached loops killed: `monitor_loop.sh` (live monitor) and `retry_loop.sh` (new-fleets).
  - No active watcher subagents remain. Disabling `hunt-watchdog` stops future respawns of these agents.

## Keyless routes (no API key, no rate-limit budget)

- `~/workspace/skills/urlquery/bin/uq_htmx.py search --query QUERY --limit N` — undocumented htmx endpoint, separate throttle. Polite pacing (sleep between calls).
- Authenticated `uq.py` is throttled (429) — use only via the retry cron.

## Restart checklist after VM loss

1. `cron.list` — confirm `chinese-fleet-hunt-watch` and `ua-burst-retry` exist and are enabled.
2. `subagent.list` — confirm live monitor, farmable surfaces, new-fleets agents are running; respawn missing ones per table above.
3. `tail live-monitor/LOG.md` — check last poll time; backfill gap with htmx if needed.
4. Verify `~/workspace/silent-locus` git status is clean-ish (work happens on `local`, never `main`).
