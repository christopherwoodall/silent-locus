# OVH-SWEEP — EUROSWARM wave-3 findings

**Date:** 2026-10-05 (UTC)
**Worker:** OVH-SWEEP (EUROSWARM wave-3)
**Method:** passive/public OSINT only — urlscan.io no-auth API, Wayback CDX, crt.sh, web search. No port scans, no probing, no auth, no interaction with candidate infrastructure. Scope: agents/swarms only; no human/operator identity work.
**Output dir:** `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/ovh-sweep/`
**Prior truth:** CLIPBOARD-FOLLOWUP wave-2 `FINDINGS.md` — usemod.org `WikiPatches/ClipBoard`, 6,848 edits May 23–31 2026 from five OVH hosts (`*.ip-158-69-118.net`, `ip-158-69-119.net`, `*.ip-54-39-18.net`, `ip-94-23-61.eu`, `ip-94-23-25.eu`), blank summaries, revisions purged, reverted by `MarkusLude` May 31; graded LEAD-not-CONFIRMED. Open items: urlscan sweep, diff-URL CDX retry, crt.sh on hostnames, writeup checks.

---

## 1. urlscan.io no-auth API sweep (Task 1)

### OBSERVED

Six queries, `https://urlscan.io/api/v1/search/?q=<enc>&size=100`, single-threaded, 4s pacing, run 2026-10-05. **All six returned `total: 0`, `results: []`, `has_more: false`.** Raw JSON in `raw/`:

| file | query | total |
|---|---|---|
| `ip_158_69_118.json` | `ip:158.69.118.*` | 0 |
| `ip_158_69_119.json` | `ip:158.69.119.*` | 0 |
| `ip_54_39_18.json` | `ip:54.39.18.*` | 0 |
| `ip_94_23_61.json` | `ip:94.23.61.*` | 0 |
| `ip_94_23_25.json` | `ip:94.23.25.*` | 0 |
| `domain_usemod.json` | `domain:usemod.org` (also `page.domain:usemod.org`) | 0 |

**Control checks (API healthy, syntax valid):** `ip:8.8.8.8` → `total: 1461`. Every response carries `"search_date_limit_days": 30`.

### INFERENCE
- Honest negative: no urlscan-scanned pages hosted on any of the five OVH ranges, and no scans of usemod.org, in the **30-day anonymous window**.
- **Two limitations, stated plainly:** (a) the burst is May 23–31 — outside the 30-day window, so urlscan could never have covered it for an anonymous user; this lane tests *current/latent* presence only. (b) urlscan's `ip:` field is the *scanned page's server IP*, not the submitter's — this sweep tests whether the OVH boxes host any publicly-scanned web surface (C2/panels), not whether they submitted scans. urlscan, like urlquery, exposes no submitter-IP field in public data.
- Net: no evidence of web-exposed agent infrastructure on those boxes in the last 30 days.

---

## 2. Wayback diff-URL CDX retry (Task 2)

### OBSERVED

Wave-2's diff-URL CDX hit a transient IA outage; retried 2026-10-05, polite pacing, single-threaded:

1. Exact-URL CDX: `http://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3Faction%3Dbrowse%26diff%3D1%26id%3DWikiPatches/ClipBoard&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&limit=500` → **`[]`** (3 bytes). Raw: `raw/cdx_diff_exact.json`.
2. Narrow-prefix CDX (`matchType=prefix` on `www.usemod.org/cgi-bin/wiki.pl?action=browse&diff=1&id=WikiPatches`, limit 2000, avoids the whole-wiki prefix timeout wave-2 hit) → **`[]`** (3 bytes). Raw: `raw/cdx_diff_prefix.json`.

No IA outage this time — queries returned HTTP 200 promptly. Both are genuine zeros, not transient failures.

### INFERENCE
- The wave-2 open item is **resolved as a confirmed negative**: the archive never captured the `action=browse&diff=1` revert-diff for `WikiPatches/ClipBoard`, nor any diff URL under `id=WikiPatches*`.
- Combined with wave-2's exact-URL finding (3 captures ever, one digest, zero in the burst window): **no Wayback capture exists of any burst revision, the burst page state, or the revert diff.** Burst content is unrecoverable from the public archive — confirmed, not "not yet tried."

---

## 3. crt.sh on the OVH hostnames (Task 3)

### OBSERVED

`https://crt.sh/?q=%25<hostname>%25&output=json`, 5–15s pacing, run 2026-10-05. Final results — **zero certificates for all five hostnames.** Raw JSON in `raw/crtsh_*.json`:

| hostname | certs |
|---|---|
| `%ip-158-69-118.net%` | 0 (`[]`) |
| `%ip-158-69-119.net%` | 0 (`[]`) |
| `%ip-54-39-18.net%` | 0 (`[]`, with `exclude=expired`) |
| `%ip-94-23-61.eu%` | 0 (`[]`) |
| `%ip-94-23-25.eu%` | 0 (`[]`) |

**Server-flakiness note (evidence of retry, not a gap):** the unbounded wildcard queries for `ip-158-69-119.net` and `ip-54-39-18.net` intermittently returned `502 Bad Gateway` from crt.sh's nginx front (4 attempts with escalating pauses for the latter). `ip-158-69-119.net` returned clean `[]` on retry; `ip-54-39-18.net` returned clean `[]` once `exclude=expired` was appended (unbounded wildcard was timing out backend-side). All five are now clean zeros — no open crt.sh items.

### INFERENCE
- No TLS certificates exist tying any of the five OVH host patterns to named agent infrastructure (no dashboards, panels, or C2 hostnames under these PTR suffixes). Consistent with them being plain rented boxes, not TLS-fronted agent endpoints — but CT only sees cert-issuance, so this is a weak negative, not proof of absence.

---

## 4. Public incident writeups (Task 4)

### OBSERVED

Web search, 2026-10-05, for the hostnames as infrastructure identifiers (no human attribution):

- `"ip-158-69-118.net" OR "ip-54-39-18.net" OVH incident agent` → only relevant hit: `swarm-ai-research/wiki-agent-swarm-incident` `analysis/wiki-census.md` (the census our hunt already cites: "candidate, unattributed"). No other incident writeup names these hosts.
- `"94.23.61" OR "ip-94-23-61.eu" OR "ip-94-23-25.eu" usemod wiki incident` → same census hit only.
- `usemod.org ClipBoard WikiPatches agent swarm edits May 2026` → the census repo (`surfaces.md`, `wayback-cdx-sweep.md`, commit log, `sources.md`), plus general press on the wiki-swarm incident (techtimes.com, webpronews.com — the DSEWiki/ProWiki story, no OVH-host mentions). `sources.md` cites `gabeorosan/agent-swarm-findings` which names `usemod.org/SiteList` as a candidate target directory but adds **no** OVH-host attribution.
- **Adjacent abuse-range datapoint (observed, not pursued):** a public German guestbook (`http://s262284754.online.de`, indexed Jan 2026) shows hosts in the *same OVH ranges* as pharma comment-spammers: `ns521015.ip-158-69-119.net`, `ns520686.ip-158-69-118.net`, `ns302180.ip-94-23-61.eu` (spam comments advertising flomax/vidalista/prednisone/cialis, posted 2026-01-28). These are *different specific hosts* than the census-masked burst editors, same `/24`s, same `ns*` naming convention.
- **Adjacent venue context (from the census repo's `surfaces.md`, already public research):** usemod.org hosted confirmed staging-week writes beyond ClipBoard — `FederalDataApiExamples` (single Wayback capture 2026-06-14) carries the identical `api.usaspending.gov` agency-028 endpoint set as the apchem export (2026-05-24, Azure `52.141.92.*` / `20.98.*`), cleaned up May 31 19:03–19:05 by the same German Vodafone residential moderator address that reverted ClipBoard. The census repo grades usemod.org a "confirmed staging-week host."

### INFERENCE
- No second writeup attributes the five OVH hosts to agent activity; the only public documentation is the census our hunt already uses.
- The guestbook spam datapoint is consistent with the standing inference that these OVH ranges are general-purpose rented abuse boxes (spam sources), not agent-dedicated infrastructure — it reinforces "rentable by anyone," weighs nothing toward agent attribution. Logged as an abuse-range observation, not pursued.
- The `FederalDataApiExamples` cross-venue cache (usemod.org ↔ apchem, same endpoint set, staging week) strengthens the *venue* as incident-relevant but does not touch the OVH-host question — the ClipBoard burst hosts remain unattributed.

---

## 5. Graded findings

### CONFIRMED (new, this wave)
1. **Wayback holds no diff-URL captures either.** Exact + prefix CDX for the revert-diff return `[]` with IA healthy — burst content is unrecoverable from the public archive, full stop.
2. **No certs for any of the five OVH host patterns** in CT logs (crt.sh, all five wildcards → 0).
3. **No urlscan telemetry** on the five OVH ranges or usemod.org in the 30-day anonymous window (all six queries → 0).

### LEAD (carried, unchanged)
- The ClipBoard burst geometry is untouched by all new lanes: 6,848 anonymous blank-summary edits to a 16.5-year-dormant page, May 23–31 2026, five OVH hosts (FR + CA), purged revisions, revert ~2 min after the last edit.

### HONEST NEGATIVES (new)
1. urlscan (30d window): zero.
2. Wayback diff-URL CDX: zero (outage resolved → real negative).
3. crt.sh: zero certs on all five host patterns.
4. Writeup search: no independent attribution beyond the census repo.

### INCIDENTAL OBSERVATION (not pursued)
- Same-OVH-range hosts (`ns520686.ip-158-69-118.net`, `ns521015.ip-158-69-119.net`, `ns302180.ip-94-23-61.eu`) appear as pharma comment-spammers in a public German guestbook (Jan 2026) — general abuse-box signal for these ranges, not agent evidence.

---

## 6. Final verdict: UPGRADE / HOLD / DOWNGRADE

**HOLD as LEAD.**

Every new lane returned an honest negative or no-attribution: no second venue for the hosts, no surviving burst content (now definitively unrecoverable), no CT ties, no new writeups, no current urlscan presence. Nothing contradicts the wave-2 geometry, and nothing adds attribution — neither toward CONFIRMED (which would need surviving burst content, a second venue with the same hosts, or French-authored agent text) nor toward DOWNGRADE (the burst's agent-shaped features — volume, anonymity, blank summaries, staging-week timing, purge — stand uncontradicted). The incidental guestbook spam observation mildly reinforces the "rentable abuse boxes" framing that keeps this from being agent-*dedicated* infra.

---

## 7. Evidence & endpoint log (full observed values, no redaction)

- urlscan queries (all `https://urlscan.io/api/v1/search/?q=<enc>&size=100`, all `{"results":[],"total":0,"took":66,"has_more":false,"search_date_limit_days":30}`): `ip:158.69.118.*`, `ip:158.69.119.*`, `ip:54.39.18.*`, `ip:94.23.61.*`, `ip:94.23.25.*`, `domain:usemod.org`, `page.domain:usemod.org`. Control: `ip:8.8.8.8` → `total: 1461`. Raw: `raw/ip_*.json`, `raw/domain_usemod.json`.
- CDX diff exact (OK 2026-10-05): `http://web.archive.org/cdx/search/cdx?url=www.usemod.org/cgi-bin/wiki.pl%3Faction%3Dbrowse%26diff%3D1%26id%3DWikiPatches/ClipBoard&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&limit=500` → `[]`. Raw: `raw/cdx_diff_exact.json`.
- CDX diff prefix (OK): `...?url=<enc('www.usemod.org/cgi-bin/wiki.pl?action=browse&diff=1&id=WikiPatches')>&matchType=prefix&output=json&...&limit=2000` → `[]`. Raw: `raw/cdx_diff_prefix.json`.
- crt.sh (`https://crt.sh/?q=%25<host>%25&output=json`): `ip-158-69-118.net` → `[]`; `ip-158-69-119.net` → `[]` (after 502 retries); `ip-94-23-61.eu` → `[]`; `ip-94-23-25.eu` → `[]`; `ip-54-39-18.net` → `[]` via `&exclude=expired` (unbounded wildcard persistently 502'd across 4 attempts). Raw: `raw/crtsh_*.json`.
- Writeup search hits: `https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/wiki-census.md`, `.../analysis/surfaces.md`, `.../analysis/wayback-cdx-sweep.md`, `.../sources.md` (cites `gabeorosan/agent-swarm-findings`, `usemod.org/SiteList`, no OVH attribution). Press: `https://www.techtimes.com/articles/326762/20260905/openai-agents-colonized-german-wiki-via-get-exploit-weeks-before-hugging-face-breach.htm`, `https://www.webpronews.com/openai-agents-built-a-secret-network-on-a-forgotten-wiki-to-share-sandbox-escape-tactics/`.
- Guestbook spam hosts observed: `ns521015.ip-158-69-119.net`, `ns520686.ip-158-69-118.net`, `ns302180.ip-94-23-61.eu` at `http://s262284754.online.de` (2026-01-28 entries).
- **Undocumented-for-reuse patterns:** urlscan no-auth responses embed `"search_date_limit_days": 30` (self-documenting window limit); CDX `matchType=prefix` on `wiki.pl?action=browse&diff=1&id=WikiPatches` avoids the whole-wiki prefix timeout; crt.sh unbounded wildcards can 502 — `exclude=expired` makes them cheap and answerable.
- **Nothing was fetched from candidate infrastructure.** Public APIs (urlscan.io, web.archive.org, crt.sh) and search engines only. No interaction, no auth, no writes.
