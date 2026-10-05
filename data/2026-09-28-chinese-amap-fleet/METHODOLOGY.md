# METHODOLOGY.md — Agent-Swarm Hunt Manual (2026-09-28 fleet)

**Last refreshed:** 2026-10-05 ~09:15 UTC (initial build)
**Companion:** [LESSONS.md](LESSONS.md) (what we found) — this file is HOW we hunt.
Living file: extend per run; do not rewrite history.

## 1. Principles

1. **The metadata tells the story.** Timestamps, burst timing, submitter UAs, tag grammars, tunnel subdomains, infrastructure metadata carry the signal; content is secondary.
2. **Agent shape is more than language.** Time and action are agent shape too — cadence, nonce grammars, retry patterns, enumeration order.
3. **A finding that doesn't fit the frame is a lead, never a negative.** Misfits get their own investigation, not a file-and-forget.
4. **Honest zeros are first-class results.** A documented clean negative with stated coverage beats a vague maybe. Null results get the same writeup rigor as finds.
5. **Keep all, annotate, never silently dedupe.** Every record stays; external overlap goes in a per-report annotation sidecar joined at build time, plus a dataset-level provenance record.
6. **No API key is not a stop.** Read the page source, find the frontend's undocumented XHR endpoints, query them directly. Document every endpoint found for reuse.
7. **Grade everything.** Observed fact vs inferred linkage vs upstream assertion — mark which is which, every time.
8. **Hunt agents and swarms, never human operators.** No operator identity work, no registrant details, no person-focused attribution. Infrastructure and behavior only.
9. **Log, don't touch.** Record candidate URLs with context; never live-fetch them (see §5 OPSEC).
10. **Automate with curl.** curl handles this VM's egress proxy; urllib/Python HTTP stacks choke on it. Prefer curl-based collection scripts wherever a surface allows.
11. **A failed check is not a verdict.** Network failures, egress outages, and flaky endpoints produce "could not check", never "zero". Zeros require a working query path.
12. **Write it down as you go.** Steps, rationale, evidence, caveats, complete URL lists — in the durable file, incrementally, not at the end.

## 2. Collection methods

- **Endpoint discovery (the htmx pattern).** When no API key exists: load the site's frontend, find its XHR/search endpoints in page source or devtools, and query them directly with curl. Template: urlquery's `/api/htmx/report/{id}/filter/http`, `/related/ip`, `/related/domain`, `/related/similar` — all keyless, all documented for reuse in `~/workspace/skills/urlquery/bin/` (`uq_htmx.py`, curl variant `uq_htmx_curl.py` when urllib chokes).
- **Pacing.** ≤1 request per 5–10s on keyless endpoints; separate throttles per endpoint. Authenticated endpoints (urlquery `uq.py`) are 429-prone — route through the retry cron, one attempt per run, silent on 429.
- **Search-level analysis.** urlscan.io `/api/v1/search/` works reliably; `/api/v1/result/{uuid}/` 403s under load — do search-level aggregation, fetch individual results sparingly.
- **Corpus building.** Canonical `events.jsonl` + `raw/` page files; per-report annotation sidecar for external overlap; dataset-level provenance record. Corpus counts are canonical — never silently change them; reconcile differences explicitly.
- **Timestamp hygiene.** Use the report's own `date` field (submission time), NOT `@timestamp` (normalization time). Join via `labels.report_id` → raw file `date` fields. Watch for collection-window bias: day-of-week over a collection burst is not a fleet property.
- **Egress-outage pivot.** When live endpoints die, pivot to streaming grep over local corpora (~935MB across `data/*/events.jsonl` + `collections/*/data/*.jsonl`). Mark everything found this way as "pending live re-check" — local corpora skew toward known incidents and cannot establish zero activity on the live surface.
- **Shodan (authenticated).** Skill at `~/workspace/skills/shodan/` (`bin/shodan.py`, curl-based): `search '<query>'`, `host <ip>`, `count '<query>'`, `dns <domain>`. Read-only recon — never probe candidates directly (see OPSEC).

## 3. Detection techniques

- **Timing discriminators.** Cron-driven agents phase-lock to second 0; human-shaped fleets show uniform second distribution (metronome: CV 13.87, same-second parallel volleys). Death-shape: clean cut (steady to end = finished/killed) vs decay (lengthening intervals = dying cron). Nonce-as-clock: epoch nonces decode to session wall-clock — zero time-API usage is itself a signal.
- **Grammar census.** Catalog every nonce/tag/param family before hunting: `zz=oai<digits>`, `uqscan=<word><date><letter>`, `retry={epoch_ms}-{N}`, `<label><epochms>`, 19-digit epoch-ns, `uq[a-z]*=` 32-name family. New grammar = lead. Grammars evolve — track the lineage (`uqn` → `uqtag` → `mark=` → `uqscan` over 10 months).
- **Probe-grammar hunts.** Per language/domain, query the terms an agent would emit (`test/scan/search/check` in-language; `pruef/aufgabe` for German). Hyphenated probe-name patterns (`e898-start`) cut hex-substring noise.
- **Cert + ASN pivots.** crt.sh for cert subjects (relay domains, Let's Encrypt mass-issuance = automation), then Shodan pivot: same cert + same ASN + same banner = cluster. Infra claims need ≥2 pivots.
- **Dead-drop tradecraft recognition.** webhook.site inboxes (view-token trick: `#!/view/<uuid>` → inbox UUID 1:1), httpbun `/anything/` endpoints, chunked sendBeacon exfil grammars (`kind=start/headers{N}/body{N}-{offset}/done`). Decode carrier payloads as TEXT EVIDENCE ONLY — never execute, never fetch onward, never submit anywhere.
- **Rescan-campaign detection (Iranian playbook).** Fixed target lists + re-scan cadence on government domains via urlscan API-method sweeps: same URLs re-scanned on machine intervals = campaign, not coincidence.
- **Forum archaeology.** Reddit (r/netsec, r/blueteamsec, r/threatintel) sorted top/all-time + comment threads; chan archives (archived.moe, 4plebs, warosu.org), 8kun, endchan, Dread (read-only). Match old TTP writeups against corpus behavior; distinguish "forum describes TTP" from "forum shows agent doing TTP".
- **Enumeration-order analysis.** Serial ID walks (MARINA), numbered-file walks (archive.org), alphabetical/sequential target lists — machine enumeration order is agent-shaped.
- **Toolmark taxonomy.** Hunt the 10 classes: agent-started file servers (`python3 -m http.server` indexes containing `SOUL.md`/`MEMORY.md`/`skills/`), persona-file overwrites, exposed MCP `tools/list`, archive.org `ia`-CLI UA model suffixes, Hermes workspace grammar in payloads.
- **Cross-corpus collision.** Same marker in two unrelated contexts (two personas, two incidents) = the interesting case. Maintain the master marker index; collisions get their own investigation.

## 4. Verification protocol

Every candidate gets classified against our corpora AND external/public sources:

| Class | Meaning | Bar |
|---|---|---|
| **OURS** | Already in our corpora | Record IDs cited |
| **KNOWN** | Publicly documented elsewhere | Source cited (Reuters, vendor blog, paper) — do not re-report as a find |
| **GENUINELY NEW** | In neither | Full evidence packet: where found, when, exact marker, corroborating pivots |

**Evidence grades** (writeup-stated, preserved):
- **Confirmed** — multiple independent corroborations, or direct retrieval (dead-drop pull, live re-registration).
- **Agent-shaped, unconfirmed** — behavioral fit, needs a second surface.
- **Lead** — single observation, open thread.
- **Confirmed-negative-as-agent** — verified to be something else (e.g. newsletter-detonation pipeline: programmatic but not agent).

**Procedure:**
1. Corpus cross-reference FIRST: `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141), `data/2026-10-03-openai-agent-traces/events.jsonl`, `data/2026-10-01-oai-tag-sweep/events.jsonl`, plus codebreaker's dead-drop inventory for drop-shaped finds.
2. External corroboration: urlquery htmx (`/related/ip`, `/related/domain`, `/related/similar`), urlscan, crt.sh, Shodan, web search.
3. Quote precisely: report IDs, timestamps (UTC), URLs, the exact marker string. Screenshots/excerpts into `raw/`.
4. Failed checks go in a "Could not check" section — never silently dropped, never counted as zero.

## 5. OPSEC

- **LOG URLs, NEVER live-fetch candidates.** A fetch is a knock on the operator's door: their server logs show someone looking. Big vendors watching the same infrastructure publish first — we lose the find.
- **No live probing.** No port scans of your own, no connecting to candidate C2/relays, no hammering demo URLs. Shodan and crt.sh are already-passive sources; keep it that way.
- **No interaction.** No forum posts, no DMs, no channel joins, no GitHub stars/follows on target repos, no video likes. Read-only, always.
- **No credential/token reuse.** Note exposed secrets; never use them. No replaying JWTs or nonces.
- **Single decisive fetch only.** If one live check is the difference between a lead and GENUINELY NEW, do it once, note that you did, and accept the exposure.
- **No untrusted execution.** Never download+open archives/binaries from shares; never execute decoded payloads; decode as text evidence only.

## 6. Durability patterns

- **Incremental writes.** Every persona writes FINDINGS.md + lane logs as it goes — a dead agent's partial work is still evidence.
- **Resume from state.** Respawn brief = "Read `<dir>/BRIEF.md` and resume from existing files." Never redo completed lanes; check mtimes before re-reading.
- **Detached loops for monitors.** `setsid` + `nohup` + `disown` survives agent death — proven durable when the runtime drops background execs. The live monitor's `monitor_loop.sh` and new-fleets' `retry_loop.sh` are the templates.
- **Watchdog + manifest.** `hunt-watchdog` (hourly) reads `RECOVERY.md` + `PERSONA_MANIFEST.md`, respawns RUNNING personas with no live agent and no FINDINGS.md (max 10/run), stays silent when healthy. Mark personas COMPLETE in the manifest when done.
- **Scheduled refresh jobs.** `chinese-fleet-hunt-watch` (45m progress checks), `lessons-refresh` (hourly LESSONS.md rebuild), `methodology-refresh` (hourly rebuild of this file — scheduled alongside). Jobs stay silent on healthy runs; report only problems.
- **Git discipline.** Work happens on `local`, never `main`; PR workflow for merges; giant local-only blobs are gitignored (kept on disk, never pushed); no secrets in history (push protection is the backstop, not the plan).
- **VM-ephemeral rule.** Everything durable lives under `~/workspace`. `/tmp` is scratch. Crons and the runtime survive restarts; background execs do not — hence detached loops.

## 7. Anti-patterns (mistakes made and corrected)

- **CORS-laundering misattribution** — an early linkage claim was caused by hunter wrapper filenames, not submitter content. WITHDRAWN. Lesson: verify the claim against the raw bytes, not the pipeline's filenames.
- **htmx `url.domain:` zeros are weak negatives** — five lanes corroborated that htmx misses known-live records (gov.eg, go.id, pages.dev, is.gd). Every domain-query zero is provisional until curl/egress corroborates. Never present a single-endpoint zero as a finding.
- **German UI locale ≠ German agent** — DorfWiki agents wrote English through a German-localized MediaWiki (`Beschreibe hier die neue Seite.` is the site's locale). Genuinely German agent writing is a separate, much smaller set. Check whose locale the language belongs to.
- **`exit_node` is shared egress, not identity** — urlquery's `settings.exit_node` is the scanner's shared egress IP, not per-agent infrastructure. Do not build attribution on it.
- **Regex traps** — unescaped dots (`civilrightsdata.ed.gov/ngsw.json` matching `gov.ng`), `translate.goog` proxies inflating `gov.tr` counts. Strip translate proxies; escape dots; eyeball every hit.
- **Dismissing off-frame findings** — twice corrected by the user: "don't dismiss it just because it doesn't fit yet." The SHADOW-AETHER holiday inversion and the AIS dead-drop hypothesis are examined on their own terms.
- **Submitter-IP dead end** — urlquery has no submitter-IP field; `/related/ip` joins on the TARGET's resolved IP. Don't burn hours on attribution the schema can't answer.
- **Weather-as-cover** — `wttr.in` usage looked like cover traffic; it was a Hermes-family marker. Test the boring hypothesis against the data before the exciting one.
- **Toolmark absence ≠ clean** — zero toolmark strings in scan records is expected: the fleet submits through urlquery's own scanner; toolmarks live in the operator's harness, not the scan. Absence at the wrong layer proves nothing.

---
*Sources: 70 persona/lane writeups (see LESSONS.md build notes), RECOVERY.md, standing hunt doctrine. Method sections mined from: metronome, speedrunner, toolmark-reader, tracker, global-south-scout, arabic, polyglot, night-owl, german-archaeologist, librarian, codebreaker.*
