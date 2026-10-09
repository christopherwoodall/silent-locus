# ARCHIVIST — Round 2 Provenance Audit

*Filed 2026-10-05 ~08:40 UTC. Chair: Hunter S. Thompson. Lane: the numbers.*
*Standing: agents/infrastructure only; no redaction from evidence; every finding graded OURS/KNOWN/GENUINELY NEW × OBSERVED/PUBLIC SOURCE/INFERENCE. Settled Round 1 kills not re-litigated.*

## Method

All counts recomputed from the bytes on disk (`wc -l`, python set-equality on IDs, `sha256sum -c`, grep) — never from PROVENANCE prose alone. Every arithmetic claim below was verified against the actual ingest dirs.

---

## Finding 1 — pastebin-k4be arithmetic HOLDS

**Claim:** `data/2025-10-24-pastebin-k4be/` holds 198 events, all investigator-verified, spanning 2025-10-24 → 2026-09-05.

**Evidence (OBSERVED):**
- `events.jsonl`: 198 rows, 198 unique fingerprints, 198 unique `paste.id`s.
- `@timestamp` range: 2025-10-24T22:21:18+00:00 → 2026-09-05T11:33:32+00:00 — matches the claimed span exactly.
- `raw/manifest.jsonl`: 198 rows, unique IDs. `raw/<pid>.txt`: 198 bodies.
- `rollup.jsonl`: 24 rows × `paste_day_burst`; `labels."paste.count"` sums to 198.
- `sha256sum -c SHA256SUMS`: green (all entries OK).
- Reconciliation files live at `data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane1-reconciliation/` — `RECONCILIATION.md`, `reconciliation.json` (ID lists for overlap/new), `census.jsonl` (per-paste jd verdict/inclusion/body metadata), `taxonomy.json`, `GRAMMAR_TAXONOMY.md`, `analyze_corpus.py`, `build_lane1_ingest.py`.

**Classification:** Novelty — see Finding 3 (wound). Evidence OBSERVED.

**Actionability:** Counts green; no action. NOTE: the reconciliation artifacts live in the fleet persona's working dir, not inside the collection dir itself — the collection's PROVENANCE.md narrates the results but the ID-level reconciliation evidence is one directory away. Future consumers should be pointed at `lane1-reconciliation/`.

---

## Finding 2 — linuxiarz arithmetic HOLDS, to the byte

**Claim:** `data/2026-05-26-paste-linuxiarz/events.jsonl` = 381 events = 131/131 matched to the 2026-09-27 ingest + 250 new; 88 additional shellac bodies; 162 Wayback rows (35 full bodies, 127 view-only).

**Evidence (OBSERVED):**
- `events.jsonl`: 381 rows, 381 unique fingerprints, 381 unique `paste.id`s.
- Set-equality check: `reconciliation.json`'s `jd_linuxiarz_overlap_ours` (131) == the original cohort (rows with `timestamp_source = labels:paste.source_date_literal`) EXACTLY; `jd_linuxiarz_new_vs_ours` (250) == the extension cohort EXACTLY; union = 381, cohorts disjoint.
- `timestamp_source` grades: 131 `labels:paste.source_date_literal` (originals) + 88 `labels:paste.jd_time` (new shellac, range 2022-07-06T11:47:19Z → 2026-06-18T15:36:36Z — matches the claimed 2022-07-06 → 2026-06-18) + 162 `fallback:no_recoverable_date` (all Wayback rows: 35 full-body + 127 view-only). 131+88+35+127 = 381. ✓
- Bodies: 254 `.txt` files on disk = 131 + 88 + 35 ✓; every body has an event row (0 orphans); 127 events body-less = the view-only set exactly.
- `confidence`: 254 `confirmed` / 127 `medium` — matches body availability exactly.
- `raw/manifest.jsonl`: 381 unique IDs. `rollup.jsonl`: frozen at 3 rows × `paste_day_burst` (11/119/1 = 131 — the original wave, documented in PROVENANCE.md).
- `sha256sum -c SHA256SUMS`: green.

**Classification:** OURS (131) / GENUINELY NEW (250). Evidence OBSERVED. The "131/131 matched, zero divergence" claim is verified by exact set equality, not eyeballing.

**Actionability:** None needed — this is the gold-standard reconciliation to copy.

---

## Finding 3 — WOUND: k4be "ALL new / host was never in our corpus" is FALSE

**Claim (as written):** RECONCILIATION.md §2 says "k4be: 198 records, all new (host was never in our corpus)."

**Evidence (OBSERVED):**
- `data/2026-05-27-paste-archive/raw/k4be.pl/metadata.jsonl`: 20 pastebin.k4be.pl metadata records (pre-existing, from the 2026-09-28 paste sweep).
- `data/2026-05-27-paste-archive/events.jsonl`: 20 `pastebin_probe` events (record_kind `pastebin_probe`, confidence `medium`) — the same 20 paste IDs.
- Overlap with the 198 "new" k4be paste IDs: **20/20 — exact**. Genuinely-new IDs: **178/198**.
- 17 of the 20 had bodies: 6 at `raw/k4be.pl/<id>.txt`, 11 at `raw/bodies/k4be.pl/<id>.txt` (presentation-layer text — extractor header + line numbers, NOT byte-exact; the jd bodies are the raw paste bodies, differing by a consistent ~180-byte framing delta, e.g. `11e9447e`: prior 769 bytes vs jd 587 bytes — different artifacts of the same pastes, not contradictions).
- The k4be manifest's `external_overlap` annotations reference only the joshuadavid GitHub export; they do NOT annotate the overlap with our own prior `2026-05-27-paste-archive` capture — a gap against the keep-all + annotate policy (internal overlap should be annotated too).

**Classification:** OURS (the 20 were ours first, as probes). Evidence OBSERVED.

**Actionability:** Amend the novelty claim to: "198 investigator-verified events: 178 genuinely-new paste IDs + 20 re-captures (previously held as `pastebin_probe` events with presentation-layer bodies in `2026-05-27-paste-archive`; this ingest adds investigator raw bodies + jd verdict metadata)." Add internal-overlap annotations to the 20 manifest rows. The 178 genuinely-new IDs are untouched by this wound — the core novelty stands, the framing was overstated.

---

## Finding 4 — The events-count discrepancy (2,110 / 2,141 / 2,159), audited

**The three numbers, decoded from the bytes:**

1. **2,110** — STALE TEXT, not a current artifact. It appears only in `PROVENANCE.md` line 33 ("2,110 `venue_finding` records (one per report; deduped by report_id)"). It is reproducible from NOTHING on disk: not the file (2,141), not the raw base pages (1,970 unique reports), not the API collect stats (1,974). The collection's own git commit message says "(2141 urlquery reports…)" — the file has had 2,141 rows since ingestion. 2,110 is a stale-draft/transcription figure that survived the recent PROVENANCE.md touch-up (the uncommitted diff leaves that line untouched). Otherwise the sentence's description is accurate: one record per report, deduped by report_id (verified: 2,141 rows, 2,141 unique report_ids, all `record_kind: venue_finding`).

2. **2,141** — CANONICAL. Composition fully verified:
   - 1,970 base urlquery sweep reports (`raw/page_000.json`–`page_019.json`; urlquery `api_total_hits` was 1,974 at collect, 1,970 saved) — all 1,970 present in events.jsonl, zero missing.
   - 171 pivot/infra reports: `raw/infra/httpbun/page_000.json` (65) + `raw/gaode/page_000.json` (30) + `raw/infra/livecodes/page_000.json` (26) + `raw/pivots/sub_poi_navi/page_000.json` (21) + `raw/infra/hrefli/page_000.json` (19) + individual `report_*.json` files (10: 1 root + 6 ltzh + 3 fanyi) = 171. All 171 verified present in raw content; the 171 event report_ids are disjoint from the 1,970 base IDs. 1,970 + 171 = 2,141. ✓
   - Event `@timestamp` span: 2026-09-28T20:57:23Z → 2026-10-05T01:12:40Z. `route`: 2,002 direct / 118 carrier / 21 relay.

3. **2,159** — UNREPRODUCED. Honest null: the number does not appear in any repo artifact as an event count (every "2159" grep hit is a byte count or URL substring). Nearest live figures: the urlquery remine file `raw/lanes/chinese-infra/q_amap_window.json` already shows `total_hits: 1,977` vs `COLLECT_STATS.json`'s `api_total_hits: 1,974` — the API total drifts upward as urlquery's index grows. A fresh remine plausibly returns ~2,159, but no stored remine records that number.

**Classification:** 2,110 = stale prose (INFERENCE on its origin: earlier-draft carryover). 2,141 = OURS/OBSERVED. 2,159 = unreproduced (honest null).

**Actionability (recommended resolution):** Do NOT change any canonical count. Keep **2,141** canonical — it is the file. Fix PROVENANCE.md line 33: "2,141 `venue_finding` records (one per report; deduped by report_id) = 1,970 base sweep + 171 pivot/infra reports." Treat any remine figure as a live-API observation: record it with its exact query string + run date, and reconcile against events.jsonl (dedupe by report_id) before it ever touches the canonical count. If the Chair wants the remine absorbed, the 171→N pivot delta must be itemized first.

---

## Finding 5 — Chinese-only URL inventory VERIFIED

**Claim:** `personas/codebreaker/raw/url-inventory-chinese-swarm.jsonl` = 375 unique URLs; split 26 / 123 / 115 / 40 / 29 / 17 / 4 / 16 / 5.

**Evidence (OBSERVED):**
- 375 rows, 375 unique `url` values. Class counter: `livecodes-carrier` 26, `httpbun-carrier` 123, `httpbin-carrier` 115, `webhook-deaddrop` 40, `hrefli-wrapper` 29, `shortener` 17, `jina-proxy` 4, `staging-host` 16, `hospital-backend-target` 5. Sum = 375. **Exact match on all nine categories.**
- Zero `REDACTED` / placeholder patterns across the whole file (full URLs preserved, per the 2026-10-05 no-redaction standing rule).
- Every row carries a `records` provenance array (dataset, report ref, report URL, timestamp, file origin).
- Minor fidelity note (not a violation): 8 `httpbun-carrier` rows store display-truncated URLs (151 chars) with honest `truncated: true` flags; full values recoverable via the `records` refs and the sibling full `url-inventory.jsonl` (the miner script `mine_url_inventory.py` documents the fold; generated with `FLEET_ONLY=1`). The miner's `lhr-tunnel` and `aihw-tableau` classes simply had zero hits in the chinese-swarm run — not an error.

**Classification:** GENUINELY NEW inventory (Chinese-swarm-only cut). Evidence OBSERVED.

**Actionability:** None required. If the 8 truncated URLs are ever cited, cite via the full-inventory companion or the source report URL in `records`.

---

## Finding 6 — Round 1 citation integrity: 5 of 6 landed, 1 FAILED

Spot-checked the corrections GRADES.md lists as applied:

- ✅ `CONTEXT.md` fresh-inbox framing (line 18: the 178.63.67.106 correction is verbatim).
- ✅ `CONTEXT.md` xss-osint-insert kill (line 19), `?r=` kill (line 20), Tencent kill (line 23).
- ✅ Dead-drop-diver `FINDINGS.md` SHAPE-3 (dates + layer confusion corrected, lines 27–30) and SHAPE-4 (retired as grammar, lines 32–34).
- ✅ `IP_LOG.md`: 178.63.67.106 precision fix, 62.234.187.97 + jina-orz.fit downgraded KILLED, letss.win IPs (95.169.18.20, 207.57.145.214) downgraded to WATCHLIST, new watchlist rows appended (160.19.212.117 et al.).

- ❌ **FAIL — CONTEXT.md line 24 still states "11 live webhook.site inboxes."** Round 1 kill #8 explicitly killed that figure: "unreconciled figure, killed as a claim. Only 4 confirmed ALIVE (newest beacon 03:05Z)." The killed claim survives in the "Tonight's verified finds" section — the exact place future personas are told not to re-report. **Wound: amend line 24** to the Round 1-verified figure ("4 confirmed ALIVE, newest beacon 03:05Z; '11' was an unreconciled claim, killed Round 1").

**Classification:** Process wound (stale citation), not a factual dispute. Evidence OBSERVED.

**Actionability:** One-line edit to `counsel/CONTEXT.md` line 24. Recommend the Chair sweep CONTEXT.md once more for other pre-kill phrasing (e.g. "11 live" may echo in persona files that copied it).

---

## Off-frame / leads (not negatives)

- The `2026-05-27-paste-archive` collection's own PROVENANCE (lines 72–75) says "20 pastebin.k4be.pl (17 bodies, 3 metadata-only)" while its `metadata.jsonl` `body_status` counts are 6 body / 11 meta-only / 3 reply-form-only — internally consistent only if the 11 "meta-only" rows have their bodies at `raw/bodies/k4be.pl/` (they do, 11 files). Not a discrepancy, but the `body_status` field is location-relative and misleading; worth a one-line clarifier in that PROVENANCE.
- The urlquery API total for the amap query is drifting upward (1,974 → 1,977 in stored files; possibly ~2,159 live). If the fleet is ever re-mined, the delta belongs in `raw/lanes/` with a run date, per Finding 4's resolution.

## Summary for the Chair

Arithmetic across all three ingest lanes holds: k4be 198/198 (dates, rollup, SHA256SUMS green), linuxiarz 381 = 131+88+35+127 with exact set-equality on the 131/131 reconciliation and 250/250 new. The fleet's 2,141 canonical events = 1,970 base + 171 pivots, fully itemized and traceable; 2,110 is stale prose in PROVENANCE.md (fix the line, not the count); 2,159 is unreproduced from stored bytes (honest null). The 375-URL chinese-swarm inventory verifies exactly on all nine categories with zero redactions. One real wound: k4be's "all new / host never in our corpus" claim misses 20 pre-existing `pastebin_probe` records in `2026-05-27-paste-archive` — true figure is 178 genuinely-new + 20 re-captures. One citation failure: CONTEXT.md line 24 still carries the Round-1-killed "11 live webhook.site inboxes" figure. Reconciliation artifacts for lane-1 live at `personas/pastebin-plunderer/raw/deep-dive/lane1-reconciliation/` (not inside the collection dirs).
