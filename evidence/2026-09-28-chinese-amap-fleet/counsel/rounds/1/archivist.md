# ARCHIVIST — Round 1 Report

*Provenance and memory. Nothing enters without a citation. Filed 2026-10-05 ~08:10 UTC.*

## LANE 1: Litterbox / catbox sweep

**Question:** Is `litter.catbox.moe` a live dead-drop surface for agents, or a one-off?

### Method (OBSERVED)
- urlquery htmx search (`bin/uq_htmx_curl.py`, search endpoint = URL metadata only; no candidate URLs fetched or probed, per lane rules).
- Queries: `litter.catbox.moe` (68 reports, 3 pages), `litterbox` (8 reports), `files.catbox.moe` (first page, 24 reports).
- Corpus correlation: `grep` across `2026-09-28-chinese-amap-fleet/events.jsonl`, `2026-10-01-oai-tag-sweep/events.jsonl`, `openai-agent-traces/data/traces.jsonl`.

### What the domain is (PUBLIC SOURCE)
`litter.catbox.moe` is the **official** file-storage subdomain of catbox.moe's Litterbox temporary file service: uploads happen at `litterbox.catbox.moe`, files land at `litter.catbox.moe/<random>.<ext>`. Confirmed by hagezi/dns-blocklists#7819 and vjt/grappa-irc commit 764486b079499e314a078ff610dc0aa054c8f09c ("POSTed a 1x1 PNG to the litterbox endpoint; response URL host is `litter.catbox.moe`"). The 6-char random filenames are the service's **native** grammar, not agent grammar. The subdomain carries a known malware-drop reputation (blocked by threat-intel feeds; NextDNS metadata #1196 notes it as temp hosting "commonly used to temporally sharing file").

### The epoch-nonce family (OBSERVED — genuinely new detail)
Seven urlquery reports of `<6char>.html?x=<epoch.fraction>`, where each nonce decodes to **seconds before its own report timestamp** (self-nonce, generation-time grammar):

| report_id | submitted URL | report date | nonce decodes to |
|---|---|---|---|
| (htmx) | `litter.catbox.moe/jf6rdd.html?x=1776567917.882642` | 2026-04-19T03:05Z | 03:05:17 |
| (htmx) | `litter.catbox.moe/xhtk71.html?x=1776568215.0723984` | 2026-04-19T03:10Z | 03:10:15 |
| (htmx) | `litter.catbox.moe/fb9x8g.html?x=1776568484.4107835` | 2026-04-19T03:15Z | 03:14:44 |
| (htmx) | `litter.catbox.moe/xnb7w2.html?x=1776568713.4424078` | 2026-04-19T03:19Z | 03:18:33 |
| (htmx) | `litter.catbox.moe/i9toke.html?x=1776568916.8594236` | 2026-04-19T03:22Z | 03:21:56 |
| (htmx) | `litter.catbox.moe/ic8j49.html?x=1776569099.4976683` | 2026-04-19T03:25Z | 03:24:59 |
| `c6ec491c-5d36-4fbb-a996-ea19508b3218` (in-corpus, tag-sweep) | `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` | 2026-05-10T08:12:57Z | 08:12:25 (32s before report) |

The Apr 19 burst: 6 sequential uploads, ~4-minute cadence, 03:05–03:25 UTC — a programmatic upload-then-verify loop.

### Surrounding activity (OBSERVED)
- **Apr 26–27:** ~12 `.html` reports in two waves (18:14–19:12 UTC Apr 26; 05:47–06:09 Apr 27).
- **May 1–2:** ~15+ `.html` reports (22:13–23:12 May 1; 14:27–15:25 May 2).
- **May 12:** `.js`/`.mjs` pair, same minute (`h8nc9u.js`, `7rrc6l.mjs`).
- **May 13:** `.png`/`.jpg` pair.
- **Jul 27:** `z4gr71.apk` — an Android APK on a temp host; graded **HUMAN-KIT-SHAPED** (malware distribution grammar; Litterbox blocks .exe/.jar but .apk is not on its blocklist per public source).
- Older (2025): scattered .gif/.mov/.jpg/.txt + bare-domain scans — ordinary human temp-host use.
- `litterbox` query: only bare-domain scans of the official `litterbox.catbox.moe` — no markers.
- `files.catbox.moe` first page: zero agent-marker params.

### Corpus correlation (OBSERVED)
- Only ONE of the 68 reports is in-corpus: `c6ec491c` (tag-sweep, tagged `epoch_nonce`, hunt campaign `reader-proxy-ops`). It is the May 10 row above.
- **Zero** hits for `litter.catbox.moe`, `catbox.moe`, or `litterbox` in amap-fleet `events.jsonl` and oai-traces `traces.jsonl`.
- **Zero** `zz=`, `uqscan=`, or other agent-marker grammar on any litterbox URL observed.

### Verdict
**A historical one-off cluster, NOT a live dead-drop surface.** Last report Jul 27; the `.html`+epoch-nonce activity is confined to Apr 19–May 10. The self-nonce grammar is **agent-shaped (INFERENCE)** and matches the toolkit's self-nonce family, but agent attribution is unproven: the same behavior fits a human malware/phishing operator testing pages on a service with a documented malware-drop reputation. Novelty: the Apr 19 six-report burst timeline and the full burst chronology are **GENUINELY NEW** (CONTEXT knew only the single May 10 URL); the official-subdomain confirmation and malware reputation are **PUBLIC SOURCE**.

---

## LANE 2: PROVENANCE AUDIT

### Audit A — `zz=oai` epoch+random decomposition: **HOLDS (3/3)**

Verified independently against `openai-agent-traces/data/traces.jsonl`:

| row trace_id | `zz` value | 10-digit prefix decodes to | row `@timestamp` | delta |
|---|---|---|---|---|
| `d60a7ec3…` | `oai17816815195423336` | 2026-06-17 07:31:59 UTC | 2026-06-17T07:32:01Z | +2s |
| (row 2) | `oai17816816778282371` | 2026-06-17 07:34:37 UTC | 2026-06-17T07:34:39Z | +2s |
| (row 3) | `oai17816817718757665` | 2026-06-17 07:36:11 UTC | 2026-06-17T07:36:13Z | +2s |

Suffixes `5423336`, `8282371`, `8757665` are all 7 digits. The decomposition (`oai` + 10-digit epoch seconds + 7-digit random) is sound; nonces are generated ~2s before capture — consistent with an agent stamping request time into the URL. **Citation: verified, primary source = corpus rows themselves.**

### Audit B — Fresh webhook.site inbox `3b5027e4-…?page=header3` (scanned 2026-10-05T03:18Z): **HOLDS**

Primary source: `personas/metronome/raw/htmx_webhook_site.json` — raw htmx search result listing `webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517?page=header3` with `date: 2026-10-05T03:18:00Z`, report_id `c9104bb8-8c1f-428f-b421-c57d0d4d53be`. Corroborated by `personas/tracker/raw/deaddrops.md` (same URL, 03:19) and `personas/evaluator/raw/http_c9104bb8-…html` (shows `x-token-id: 3b5027e4-…` and `Referer: …?page=header3` in the captured traffic). `new-fleets/FINDINGS.md` documents the same-session burst context (4 UUID inboxes, `?page=header3`, `?run=<epoch-ms>` via href.li). **Citation: verified, multi-file primary evidence.**

### Audit note — `?r=<19-digit>` nonce family (two inboxes, shared `178207` prefix, 13 days apart): **UNVERIFIED from the shared record**

`grep` for `[?&]r=[0-9]{15,22}` across all three corpora returns **zero** rows; `grep 178207` across the counsel directory hits only CONTEXT.md itself. The evidence lives with another lane and is not present in any file I can cite. This is not a failure — it is an incomplete citation: the claim cannot be checked from the shared corpus. Recommend the claiming lane file its raw report IDs/rows.

---

## Grades & novelty ledger

| Finding | Grade | Novelty |
|---|---|---|
| Apr 19 six-report epoch-nonce `.html` burst (~4-min cadence) | OBSERVED | **GENUINELY NEW** |
| May 10 `hdcf0x.html?x=…` nonce = 32s pre-report (self-nonce) | OBSERVED | OURS (already in-corpus as `epoch_nonce`) |
| Apr 26–27 / May 1–2 `.html` bursts; May 12 `.js`/`.mjs`; Jul 27 `.apk` | OBSERVED | **GENUINELY NEW** |
| `litter.catbox.moe` = official Litterbox storage subdomain; 6-char names native | PUBLIC SOURCE | KNOWN (public) |
| Litterbox malware-drop reputation (threat-intel blocklisting) | PUBLIC SOURCE | KNOWN (public) |
| Agent attribution of the nonce family | INFERENCE | open — agent-shaped, unproven |
| `z4gr71.apk` graded HUMAN-KIT-SHAPED | INFERENCE | OURS |
| Litterbox is a live agent dead-drop surface | — | **REFUTED by timeline** (last activity Jul 27; nonce activity Apr 19–May 10) |
| `zz=oai` decomposition | verified OBSERVED | KNOWN (tonight) — audit HOLDS |
| `3b5027e4` inbox freshness/identity | verified OBSERVED | KNOWN (tonight) — audit HOLDS |
| `?r=<19-digit>` family | — | citation incomplete — needs raw evidence filed |

## Open threads for other lanes
- The Apr 19 nonce-burst predates all documented agent incident windows (UNCTADstat Apr–Jun overlaps; Artifactory May 7+; DoE Jun 17; HF Jul 10–13). If the nonce family is agent-linked, Apr 19 is an early data point worth reconciling with the Nov-2025-origin thesis.
- The `.apk` (Jul 27) and the malware-reputation context belong more naturally to a human-threat lane than an agent lane.
