# GEO-PROFILER — urlquery submitter geo-shape sweep (2026-10-04/05 session)

## Method & limits
- Intended tool `~/workspace/skills/urlquery/bin/uq_htmx.py` was UNUSABLE this
  session: the VM egress proxy (hatch-egress-proxy:3128) timed out on CONNECT to
  ALL hosts from ~23:30 CDT onward (both python-urllib and curl paths). The
  authenticated API (uq.py) was already 429-throttled and unreachable anyway.
- Fell back to the text-fetch channel against urlquery.net's homepage "latest
  scans" table: 12 rows per fetch, minute-precision dates, URL + target IP + ASN
  + flag image. Three fetches ~15 min apart returned the SAME cached snapshot
  (2026-10-05 04:31 UTC), so this report rests on one real snapshot + evidence
  mined from public audit docs (hamzah2304/messageboardauditbench) for older
  clusters. No report IDs or second-precision timestamps are exposed in this
  rendering; per-row flags only mapped for 3 of 12 rows (zz/HK/US) — country for
  the rest is inferred from ASN.
- Amap operator (uqscan=/uqtag=/uqvnc= grammar, CN Alibaba targets) is EXCLUDED
  by brief; none observed in the snapshot.

## Cluster U1 — "urldance" HK phishing-redirector sweep (FRESH, 2026-10-05 04:31 UTC)
Single-submitter run, high confidence (same minute, same host, sequential paths,
adjacent target IPs):
- `202608.urldance.com/7d/` → 156.225.108.43, AS139057 Edgenext Legend Dynasty Pte. Ltd. (flag: HK)
- `202608.urldance.com/8d/` → 156.225.108.42, same ASN
External shape: urldance.com runs date-rotated subdomains (`2026-08-24.urldance.com`,
`2026-09-22.urldance.com`, `2026-07-25.urldance.com`) that appear on phishing
blocklists (chainapsis/phishing-block-list added 2026-08-24.urldance.com after a
redirect re-check from dogehero.pro; multiple entries in ScamAdviser feeds). TLS
issuer org is CN. The `/7d/`, `/8d/` path pattern reads as sequential campaign
IDs on a phishing redirector. Geo shape: non-Western target (HK), Chinese-linked
phishing infra. Caveat: submitter may be a threat-intel scanner rather than an
agent fleet — flag as lead, not attribution.

## Cluster D1 — "ddnsgeek" gibberish pair (FRESH, 2026-10-05 04:31 UTC)
Paired submissions, same minute, likely one submitter:
- `jehalisipo.ddnsgeek.com/uwojad/` → 107.172.151.86, AS36352 HostPapa (flag: US)
- `dudamu.ddnsgeek.com/jipoco/` → 192.227.152.168, AS36352 HostPapa (flag: US)
Shape: random-word subdomains on dynamic-DNS host + random 6-char paths;
second row scored UQ 2 detections. Malware/redirector-checking adjacent. US
targets but the submitter grammar (gibberish-name pairs in one minute) is the
distinctive fingerprint.

## Cluster Q1 — Quidax crypto-ramp probing (2026-09-19 21:54:35 → 09-20 00:27:44 UTC, ~2.5 h)
Strongest non-Amap fleet candidate with full evidence IDs (from the frozen
audit, derivability-audit F10/F10.1/F10.2):
- Reports: `960b3314`, `52d9be69`, `f825e84d`
- Behavior: repeated Quidax buy/sell ramp URLs, an HTML-injection-shaped error
  parameter, API test scripts; mixed HTTP 200/403/redirect responses.
- Geo shape: Quidax is a Nigerian crypto exchange (NG target geo) — an
  agent-shaped task (probing fiat on/off-ramp trading flows), distinct from both
  Transluce's data-retrieval clusters and the Amap fleet.

## Cluster K1 — IEA Korean energy imports (2026-09-16)
- Reports: `6a86ffff`, `1f724789`, `879360b3` (IEA pages on Korean energy
  imports); `b0f6abe3` (submitted fetch code for related crude-oil/gas pages).
- Geo shape: KR-focused data target at the very edge of Transluce's "latest
  activity" (Sep 16). Recent non-Western-gov-flavored retrieval.

## Continuity marker — Nov 2025 pre-history (F12)
- 2026-11-12: 44 thrill-data.com submissions (Kings Dominion / Australian parks);
  2026-11-24: 61 thrill-data submissions (`parkbar`, `rideaverages`, `parkheat`
  endpoints, e.g. `6fbc9a4b`).
- The same Thai statistics-dashboard URL appears in five November and five March
  scans — a continuity marker linking the Nov-2025 origin ("when this all
  started") to the March 2026 ONCB incident. May-2026 thrill-data attempts
  escalate the same targets through r.jina.ai + executed JS (`d822ea03`,
  `6fbc9a4b`).

## Marker family — CHATGPT-marked UNCTAD (2026-05-13, F11)
- Reports `1368e4a9`, `850d1c01`, `b020bc29` carry `CHATGPT` in submitted-URL
  query params. Self-identification marker; marker ≠ authenticated submitter.

## Open / next steps
- Re-run the intended htmx date-window pulls (`date:[2026-10-01 TO 2026-10-05]`,
  paginate with offset) once egress recovers; the Q1 and U1 clusters deserve
  full burst reconstruction with second-precision timestamps and report IDs.
- U1: pull the full `202608.urldance.com` submission set (`/Nd/` path series) to
  size the sweep and confirm campaign-ID sequencing.
- Q1: enumerate all Quidax-domain submissions to bound the 2.5 h window and check
  for repeat runs before/after Sep 19–20.
