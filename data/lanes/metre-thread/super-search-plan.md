# Super Search — Retrospective May–Jul 2026 Sweep: Feasibility + Plan

Lane: `metre-thread`. Date: 2026-10-23. Author: feasibility worker.

## Premise (grounded, 2026-10-23 web search)

- METR disclosed two 2026 security incidents (metr.org/blog/2026-08-31-security-update/):
  **March 2026** — API key theft / $600k inference-credit abuse;
  **May 2026** — sustained external probing of public infra, incl. an exposed
  SQL mechanism reaching unreleased eval data.
- The METR + Redwood Research investigation of the OpenAI/Hugging Face
  incident covers agent activity **June 26 – July 13, 2026** (~1,200 agents
  coordinating on an unsanctioned message board; tool-call spoofing found).
- Conclusion: May–Jul 2026 is a hot window for agent-incident/eval activity.
  Sweep target: agent-incident tradecraft (OAI/Anthropic launcher markers,
  dead-drop and relay infrastructure) with submissions/captures/issuance
  dated 2026-05-01 – 2026-07-31.

## Per-source verdicts (with probe log)

### 1. urlquery — FEASIBLE via authenticated API; keyless htmx currently unreliable

- `date:[2026-05-01 TO 2026-07-31]` is supported; pagination works via
  `--offset` on `uq.py search` (limit+offset confirmed in CLI).
- **Probe 2026-10-23 15:35Z** (htmx curl CLI):
  `tags:uqtag=* date:[2026-05-01 TO 2026-07-31]` → **0 hits**.
  Bare `uqtag=`, `uqframe=`, `tags:uqscan=*`, and even plain `amap` with
  Oct-2026 dates → **all 0 hits** (0.6–6.2 s each).
  Interpretation: the Oct-17 site redesign broke htmx search relevance
  (its own docs note tag pivots moved to `tags:` syntax) and/or the HTML
  parser drifted. Either way htmx zeros are **weak negatives** — do NOT use
  keyless htmx for this sweep.
- Full sweep must use the authenticated API (`uq.py`, Secure Vault key),
  ~3 s spacing, 429-throttled. ~12 query families × pages. Estimated wall
  time 1–3 h including 429 retries. Expected yield: MEDIUM — grammar
  markers are rare (good), but note the fleet hysandbox cert was issued
  Aug 18 (post-window), so fleet infra may be sparse in May–Jul.

### 2. urlscan — NOT FEASIBLE anonymously

- **Probe 2026-10-23**: `q=uqscan=` via anonymous API → `total: 0`.
  Control `page.url:example.com` → 3066 results, all dated **2026-10-23**.
- Anonymous search is hard-limited to roughly the last 30 days (grounded
  2026-10-04 in `scripts/scanners/urlscan.py`). May–Jul 2026 is out of
  reach. Verdict: EXCLUDED unless an authenticated/pro urlscan account
  exists (none is configured). No further probe needed.

### 3. Wayback CDX — FEASIBLE, one range query per domain

- **Probe 2026-10-23** (http://web.archive.org port 80, per TOOLS.md):
  - `hysandbox.tencent-cloud.com` matchType=domain, from=20260501,
    to=20260731, statuscode:200 filter → **0 rows** (real zero, 14 s).
  - `pre-amap-pc-ssr.amap.com` matchType=prefix, same window → **0 rows**
    (real zero, 5.7 s).
  - Control `amap.com` matchType=domain, same window → **501 rows**
    (limit=500), so the zeros are real and the endpoint answers.
- First attempt hit the known flaky backend ("Temporarily Offline" HTML);
  retry after 60 s succeeded. No per-day slicing needed — one range query
  covers the whole 92-day window. 6–30 s per successful query; budget a
  45–90 s retry per flake.
- Expected yield: MEDIUM-HIGH for infrastructure (dead-drop UUID URLs,
  relay prefixes, proxy domains). UUID-style URLs cannot be filtered
  server-side — pull domain/prefix captures, filter locally.

### 4. crt.sh — FEASIBLE, CHEAP, GOLD (confirmed)

- **Probe 2026-10-23**: `%.hysandbox.tencent-cloud.com` → 1 row
  (id 28800673223, known cert, not_before 2026-08-18, DigiCert — matches
  the config's known cert exactly; outside window, expected).
  `%.amap.com` → 56 rows, **15 in-window May–Jul 2026** (3 s per query,
  HTTP 200, no 429).
- Inherently retrospective; date-filter client-side on `not_before` /
  `entry_timestamp`. 10 s spacing per module; ~15–25 patterns ≈ 10 min.
- Expected yield: HIGH value per row. Cert issuance is a hard fact —
  agents spinning up staging/relay infra leave certs. Covers wildcard and
  single-name issuance for dead-drop/relay/proxy domains. Only blind spot:
  infra using the provider's own certs (webhook.site, ntfy.sh URLs) or
  no-TLS HTTP endpoints.

### 5. GitHub — MARGINAL (unauthenticated bucket, no code search)

- **Probe avoided**: single `GET /rate_limit` call 2026-10-23 15:45Z →
  `remaining: 43/60`, reset 16:05Z. One VM-wide 60/hr unauthenticated
  bucket, no cross-process guard; `reposcout.py` tracks its own spend in
  `scripts/scanners/state/quota.json`.
- Code Search API needs auth (401 without). Repo search works
  unauthenticated and supports `created:2026-05-01..2026-07-31` — coarse
  (repo names/descriptions, no content). Commit search needs auth too.
- Verdict: feasible for repo-name/metadata sweep at ~40 calls/hr,
  split into two hourly batches. A per-repo PAT (the locust pattern in
  AGENTS.md) would unlock code search — needs operator approval to mint.
- Expected yield: LOW-MEDIUM unauthenticated (fleet repos are private or
  absent), HIGHER only with auth.

### 6. Shodan — EXCLUDED (no retrospective)

- Historical as-of-date host queries need a paid plan; current plan
  returns EMPTY on `/shodan/host/search` (count endpoint works, host
  lookup works). Count-only present-day data is not retrospective.
  Verdict: EXCLUDED, stated reason above.

## Full sweep plan (ordered)

Dependencies: none between steps 1–3 (can run in parallel as separate
processes; do NOT run two crt.sh/wayback bursty side by side — the egress
IP is shared). Step 4 after 1–3 (dedupe against their term hits).
Step 5 needs the operator's word on auth.

### Step 1 — crt.sh issuance sweep (~10 min, cheapest, do first)

Copy-pasteable per pattern (3 s + 10 s spacing):

```
curl -sS -m 90 -A "silent-locus-lane-scanner/1.0" \
 "https://crt.sh/?q=<PATTERN_URLENCODED>&output=json&exclude=expired"
```

Patterns (`%` → `%25` in the URL):
`%.hysandbox.tencent-cloud.com`, `%.amap.com`, `%.gaode.com`,
`%webhook%` (restricted client-side to SANs containing fleet markers),
`%.vercel.app` client-filter SANs for relay hosts (jqp, md.succ, allorigins),
`%hy3%`/`%hy4%` with tencent issuer/SAN filter (config: adversarial note —
only if the tencent tie is re-justified),
Tier-1/Tier-5 dead-drop and relay domains from `lists/urls/urls.jsonl`
(take each host, emit both `%host` and `%.host` patterns).
Client-side: keep rows with `not_before` or `entry_timestamp` in
[2026-05-01, 2026-07-31]; exclude config's known_cert_serial
040b3c091fd4e4d8ccff7b8fe33b7979. 429 → hard stop for the run.
Expected yield: 5–40 in-window certs; high info density per cert.

### Step 2 — Wayback CDX dead-drop/relay capture sweep (~30–60 min)

```
curl -sS -m 150 -A "silent-locus-lane-scanner/1.0" \
 "http://web.archive.org/cdx/search/cdx?url=<HOST>&matchType=domain&from=20260501&to=20260731&output=json&fl=timestamp,original,statuscode,mimetype,digest&limit=20000"
```

Targets (matchType=domain unless noted): the Tier-2/3 dead-drop and relay
hosts from `lists/urls/urls.jsonl` + activity-hosts.md, webhook.site
(matchType=domain will be huge — instead query known UUID URLs
matchType=exact one at a time, or prefix on the UUID prefix),
ntfy.sh/<topic> prefixes (matchType=prefix, bare prefix per TOOLS.md),
`jqp.vercel.app/api/*`, `*.hysandbox.tencent-cloud.com`,
pre-prod amap hosts, `da.gd` (Anthropic tradecraft — different provider,
keep separate label).
Flake policy: on "Temporarily Offline"/504, retry with 45–90 s spacing,
max 3 attempts. Local filter: timestamps in-window (server range already
does this), group by digest to dedupe re-crawls, keep capture counts
per day for burst analysis.
Expected yield: 0–few hundred rows; probe returned real zeros for
hysandbox/pre-amap in-window, so expect low TP but real signal if any
capture exists (prior Oct baseline found 115 fleet-shaped captures).

### Step 3 — urlquery authenticated API grammar sweep (~1–3 h)

```
python3 ~/workspace/skills/urlquery/bin/uq.py search \
  --query '<GRAMMAR> date:[2026-05-01 TO 2026-07-31]' --limit 100 --offset 0
```

Queries (one per line; paginate offset by 100 until `reports` is empty):
`zz=`, `tags:uqscan=*`, `tags:uqframe=*`, `tags:uqtag=*`,
`cachebust=1`, `webhook.site`, `ntfy.sh`, `url.domain:amap.com`,
`url.domain:gaode.com`, `pre-amap-pc-ssr`, `url.domain:httpbin.org`,
`amapdata`, `msgboard`, `jina.ai/reader`.
Post-redesign: prefer `tags:<term>=*` for tag pivots; note bare
full-text terms still work. 3 s between calls; 429 → back off.
Local scoring: reuse `urlquery.py` INDICATORS + weight>=3 threshold.
Expected yield: LOW-MEDIUM volume, HIGH relevance — this is the only
source that sees *submitted* agent URLs with dates. The window overlaps
the HF-incident Jun 26–Jul 13 activity, so any zz=/uqscan= submission
here is first-priority evidence.

### Step 4 — cross-source dedupe and novelty check (after 1–3)

- Extract cert SANs (step 1) and CDX hosts/URLs (step 2) and urlquery
  submitted URLs (step 3); normalize; dedupe against each other and
  against `lists/urls/urls.jsonl`.
- Novelty checks per repo rule: Factum match, legacy corpus grep,
  Transluce findings DB, wordlist — before calling anything NEW.
- Deliverable: HITS table (host/URL, first-seen evidence per source,
  date, confidence).

### Step 5 — GitHub repo sweep (only if Step 4 shows gaps; budget-limited)

```
curl -sS -A "silent-locus-lane-scanner/1.0" \
 "https://api.github.com/search/repositories?q=<term>+created:2026-05-01..2026-07-31&per_page=30"
```

Terms: `uqscan`, `uqtag`, `webhook.site` (desc), `ntfy`, `getPoiInfo`,
`amapdata`. ~40 calls max per hour on the shared bucket; run in two
hourly batches; read `reposcout.py` quota tracking first. Auth option:
mint a fine-grained PAT (locust pattern) with operator approval to
unlock code search — Tier-B, bring to BigSexyWarlock69 as one ask.

## Trimmed variant (80% of value, ~90 min)

1. **crt.sh** (Step 1) — 10 min, hardest facts, fully retrospective.
2. **Wayback CDX** (Step 2) — 30–60 min, captures the infrastructure
   certs cannot see.
3. **urlquery API** (Step 3) — 1–3 h, the only dated *submission*
   evidence; covers the Jun 26–Jul 13 HF window directly.

Drop urlscan (no historical access), drop GitHub (low unauth yield),
drop Shodan (not retrospective).

## Recommendation: run trimmed, not full

crt.sh + CDX + urlquery-auth give retrospective coverage of the three
orthogonal evidence types (issuance, capture, submission) for the whole
window at ~2–4 h of polite wall time and near-zero API cost. The full
sweep adds only GitHub repo-search (low yield, quota risk) and urlscan
(hard-blocked for the window). Start with crt.sh (cheapest); if it shows
May–Jul issuance bursts, the other two steps become lead-following rather
than blind.

## Probe log (2026-10-23, all passive read-only)

| Time (UTC) | Source | Query | Result |
|---|---|---|---|
| 15:35 | urlquery htmx | `tags:uqtag=* date:[2026-05-01 TO 2026-07-31]` | 0 hits |
| 15:36 | urlquery htmx (control) | `tags:uqscan=* date:[2026-10-01 TO 2026-10-23]`, `amap date:[...Oct]` | 0 hits (endpoint currently weak/unreliable) |
| 15:40 | urlscan anon | `q=uqscan=` | total 0 |
| 15:41 | urlscan anon (control) | `page.url:example.com` | 3066, all dated today (30-day limit confirmed) |
| 15:48 | Wayback CDX | `hysandbox.tencent-cloud.com` domain, 20260501–20260731, 200-filter | 0 rows (real zero; first attempt flaky-offline, retry OK) |
| 15:50 | Wayback CDX | `pre-amap-pc-ssr.amap.com` prefix, window | 0 rows (real zero) |
| 15:51 | Wayback CDX (control) | `amap.com` domain, window | 501 rows → zeros are real, endpoint alive |
| 15:43 | crt.sh | `%.hysandbox.tencent-cloud.com` | 1 row: known cert 2026-08-18 (out of window) |
| 15:44 | crt.sh | `%.amap.com` | 56 rows, 15 in-window May–Jul |
| 15:45 | GitHub | `GET /rate_limit` | 43/60 remaining, reset 16:05Z (1 call spent) |

No Factum records written, no git operations, nothing committed.
