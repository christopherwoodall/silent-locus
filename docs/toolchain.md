# Toolchain: scripts, skills, and query surfaces

The tools used across the hunt. In-repo scripts first, then the workspace
skills (outside this repo, under the workspace `skills/` directory), then
the external query surfaces.

## In-repo scripts

### `data/2026-09-28-chinese-amap-fleet/slug-hunt.py`

Cross-archive **slug presence sweep**. For each marker slug (UUID,
subdomain, ntfy topic, `?m=` marker, path fragment), checks three scan
archives in one pass and reports hit counts:

1. **urlquery** search API — `q=` matches submitted URLs (authenticated,
   via `uq.py` below).
2. **urlscan.io** search API — `page.url:"<slug>"` (keyless, recent
   window, search-level hits only).
3. **Wayback CDX** — `url=<slug>*` and `*/<slug>*` with
   `output=json&collapse=urlkey` (keyless).

Usage: `python3 slug-hunt.py <slug>… [--json]`

Output is hit-count-only (`{"hits": n}` per surface; errors as
`{"error": …}`) — it screens for *presence*, not content. A zero is a
**weak negative** (limited windows/coverage), never a clean zero. Verified
working 2026-10-05 (dummy slug → 0/0/0, exit 0).

### `collections/eval-questions/_tools/`

Stdlib-only parquet reader + normalizer (no pyarrow needed) used to bank
the eval-question corpus. Reusable for future parquet bank jobs.

### `scripts/` (repo root)

Loaders and validators at root (`validate_schema.py`,
`validate_collections.py`), cross-collection transforms in `builders/`,
reusable tools in `maintenance/`, preserved one-off collectors in
`archive/`. Read `scripts/README.md` before running historical code.

## Workspace skills (outside this repo)

These live in the workspace `skills/` directory (sibling of the repo
checkout), not inside `silent-locus`. They are referenced here because
hunt lanes depend on them.

- **`skills/urlquery/bin/uq.py`** — authenticated urlquery.net search.
  `uq.py search --query '<q>' --limit <n>`. Supports `url.domain:`,
  `tags:`, `date:[YYYY-MM-DD TO YYYY-MM-DD]` scoping. Note: `q` matches
  submitted URLs; hyphenated probe-name patterns (e.g. `e898-start`) cut
  hex-substring noise. Authenticated endpoints are 429-prone — one
  attempt per cycle, silent on 429.
- **`skills/urlquery/bin/uq_htmx.py`** (+ curl variant
  `uq_htmx_curl.py`) — keyless htmx endpoints:
  `/api/htmx/report/{id}/filter/http`, `/related/ip`,
  `/related/domain`, `/related/similar`. The template for "no API key is
  not a stop".
- **`skills/shodan/bin/shodan.py`** (curl-based) — `search '<query>'`,
  `host <ip>`, `count '<query>'`, `dns <domain>`. Read-only recon.
- **`skills/huggingface/bin/hf-download`** — gated HuggingFace dataset
  downloads: `hf-download <dataset_id> --revision <sha> --pattern <substr>
  --dest <dir>`. Resolves via the API, downloads through pre-signed CDN
  URLs without leaking auth headers. (The python `huggingface_hub` stack
  is broken on the hunt VM — use this or curl.)

## External query surfaces

| Surface | What it answers | Access | Notes |
|---|---|---|---|
| urlquery.net search | Reports matching submitted URLs, tags, dates | Authenticated (`uq.py`) | `q` = submitted-URL match. Primary surface. |
| urlquery htmx | Report details, related IP/domain/similar | Keyless | Recent-window biased; tokenizer drops some matches — corpus stays source of truth. |
| urlscan.io `/api/v1/search/` | Scans matching URL/content queries | Keyless | Anonymous = 30-day window + top-100 cap. `page.url:"…"` for slug search. Result-detail API is login-gated — search-level metadata only. |
| Wayback CDX | Archived captures by URL prefix | Keyless | `url=<prefix>*`, `collapse=urlkey`. Per-host queries; TLD-wide needs auth. |
| Common Crawl index | Crawled URLs by wildcard | Keyless | Resolve index names via `collinfo.json` first; guessed names 404. |
| crt.sh | Certificate subjects (CT logs) | Keyless | Query-syntax caveats: no mid-query `%`; `exclude=expired` for wildcards; transient 502s — retry with backoff. |
| CertSpotter API | CT fallback when crt.sh is down | Keyless | `api.certspotter.com/v1/issuances?domain=…`; history starts 2026-05-31. |
| Shodan | Indexed banners, HTML, certs, hosts | Authenticated (skill) | `hostname:` matches PTR history, not a live census. |
| GitHub code search | Marker grammars in code | Varies | Dork grammars, not keywords (ABOUT vs WITH). |
| Arquivo.pt | Portuguese web archive | Keyless | `site:` needs a full hostname; run a calibration query before filing negatives. |
| Wikiwix | On-demand wiki archive | Keyless-ish | `token.php?url=` is an existence probe; `page.php` render wall needs a browser. |

## Query recipes

**New marker slug triage** (do this first for any new slug):
`python3 data/2026-09-28-chinese-amap-fleet/slug-hunt.py "<slug>"`
→ urlquery / urlscan / CDX presence in one pass.

**Eval-fingerprint hunt**: take phrases from
`collections/eval-questions/HUNT-QUERIES.md` (50 ranked, with per-surface
search strings) and run them through `uq.py` / urlscan / Google quoted
search.

**Infrastructure pivot**: cert subject (crt.sh) → same cert + same ASN +
same banner (Shodan) = cluster. Two pivots minimum before claiming.

**Dead-drop inbox check** (keyless):
`GET https://webhook.site/token/<uuid>/requests` — returns per-request
IP, country, true sender UA, headers, query, body. Check fleet inboxes
immediately; they expire within days (404 = expired, a clean negative).

## Environment notes

- On the hunt VM, **curl handles the egress proxy**; Python HTTP stacks
  (urllib, httpx) do not. Prefer curl-based collection scripts there.
- The VM's egress proxy intercepts DNS — local DNS/liveness checks are
  inconclusive by construction. Record as unanswered, not negative.
- Pacing: ≤1 request per 5–10s on keyless endpoints; separate throttles
  per endpoint.
