# Swarm Infrastructure Watch

Proactive monitoring for Chinese Amap fleet resurgence via webhook.site
creator-IP records.

## The Method

When you view a webhook.site inbox, the token metadata exposes the IP and
user agent of whoever created it:

```
GET https://webhook.site/token/<uuid>
Header: Accept: application/json
Response: {"ip": "1.2.3.4", "user_agent": "...", "created_at": "...", ...}
```

The swarmcha.se researchers used this to attribute the fleet to Tencent
Cloud HK — 18 creator IPs on AS132203. We replicate their method to watch
for new fleet infrastructure.

### Creator IP vs Poster IP

This distinction is critical and the #1 thing the counsel review verifies:

| | Creator IP | Poster IP |
|---|---|---|
| **Source** | Token metadata (`GET /token/<uuid>`, `ip` field) | Per-request data (`GET /token/<uuid>/requests`, per-request source) |
| **Meaning** | Who created the inbox (operator infrastructure) | Who sent requests to the inbox (may use proxies) |
| **Fleet signal** | Tencent Cloud HK = operator | Residential/VPN = agent egress via proxies |
| **We extract** | ✅ Yes | ❌ No |

Our Oct 14 analysis showed poster IPs were all residential/VPN while the
report's creator IPs were Tencent Cloud. Both can be true simultaneously:
operators build infra from cloud, agents egress through residential proxies.

## Components

| File | Purpose |
|------|---------|
| `swarm-infra-crawler.py` | Main crawler (v2, creator-IP focused) |
| `swarm-infra-config.json` | IOCs, CIDRs, cloud ASNs, tag patterns (extend as we learn) |
| `ip_classifier.py` | 4-tier IP classification with ASN caching |
| `swarm-infra-watch-CRON-PROPOSAL.md` | Cron schedule proposal (6h, pending approval) |
| `swarm-infra-crawler-ADVERSARIAL-REVIEW.md` | Counsel review of extraction method |

## Classification Tiers

1. **KNOWN_SWARM** — Exact match against 18 published fleet IPs or within
   43.162.0.0/16. Highest signal. Immediate alert.
2. **CLOUD_SERVICE** — ASN belongs to cloud provider. Flag which cloud.
   Swarm-linked ASNs (AS132203, AS45090) get priority.
3. **RESIDENTIAL_VPN_HOSTING** — ISP ranges, VPN providers, hosting.
   Expected for poster IPs; notable for creator IPs (unusual).
4. **UNKNOWN** — Couldn't classify. Logged, deprioritized.

Tiers 1-2 are the signal. Tiers 3-4 get logged but don't trigger alerts.

### Standing Rule: Classify Every Stored IP

Per BigSexyWarlock69's standing order: **anywhere we store an IP, classify it
for cloud/known-host status.** Every IP field in every factum record, state
file, and run log must be a classified `ip_record()` dict — never a bare IP
string. Cloud/known-host is a priority indicator.

The crawler enforces this via `ip_record(ip, config, role)` in
`swarm-infra-crawler.py`, which wraps `classify_ip()` and returns:

```json
{
  "ip": "43.162.198.97",
  "role": "creator",
  "tier": 1,
  "tier_label": "KNOWN_SWARM",
  "tier_detail": "Exact match against published fleet IP list",
  "asn": "AS132203",
  "org": "Tencent Cloud",
  "country": "HK",
  "city": "Hong Kong",
  "swarm_linked": true
}
```

When adding a new module that stores IPs (poster IPs, source IPs, etc.),
ALWAYS use `ip_record()` — do not store raw IP strings.

## Pipeline

```
urlquery search (tag grammar + Amap tradecraft)
    → Extract webhook.site inbox UUIDs
    → Deduplicate against seen set
    → GET token metadata for each new inbox
    → Extract creator IP + UA
    → Classify IP (4 tiers)
    → Check factum for existing records
    → Write factum-ready JSONL
    → Lane-ingest worker submits to factum
```

## Factum Integration

Every creator-IP extraction becomes a factum record with:
- Inbox URL (full UUID)
- Creator IP, ASN, org, country, city
- Classification tier
- Timestamp of extraction
- PRIMARY grading (we directly observed it)
- Link to source urlquery report
- Provenance noting creator-vs-poster distinction

The crawler checks `processed_creators` in state before re-extracting.
The lane-ingest worker dedups against existing factum records.

## Baseline (2026-10-14)

25 inbox UUIDs extracted from `data/lanes/2026-09-28-chinese-amap-fleet/`.
All 25 return 404 (deleted).

**Interpretation caveat (adversarial review):** "7-day expiry" is inference,
not observation. The all-404 result is consistent with expiry, operator
deletion, platform purge, or never-valid UUIDs. We record 404 vs 410
separately going forward to distinguish expiry (410) from not-found (404).

## Adversarial Review

`swarm-infra-crawler-ADVERSARIAL-REVIEW.md` documents 15 issues found by
counsel review. Must-fix items applied:

- **A1:** Creator-IP semantics documented with required two-IP control
  experiment noted as pending validation. If the control shows the field
  follows the viewer, the method is dead.
- **B1:** 43.162.0.0/16 demoted from tier-1 KNOWN_SWARM to tier-2 watchlist.
- **B2:** `swarm_linked` flag documented as report-derived, not validated.
  Tier-2 alerts require base-rate measurement before going live.
- **C1:** Transient failures (429/500/timeout) now retry next run; only
  404/410 mark inboxes as seen.
- **C2:** Denominator logging added (searches run, inboxes harvested,
  total seen) so silent runs are interpretable.
- **C4:** 404 vs 410 recorded separately.
- **A2/E:** Factum grade vocabulary corrected (OBSERVED, not PRIMARY).
- **B4:** `known_researcher_ids` documented as not-yet-wired.

**Do not enable the cron until:** two-IP control experiment (A1) is complete
and tier-2 base rates are measured (B2).

## Rate Limits

Per 6h run:
- urlquery htmx: ~7 searches × 3s = ~1-2 min
- webhook.site: 1 GET per new inbox × 2s (typically 0-5 new)
- ipinfo.io: 1 per uncached IP × 1s (persistent local cache)
- Total: < 5 minutes

## Legal & Scope

- Passive collection only. GET requests to public APIs.
- No POSTs, no auth bypass, no intrusive scanning.
- Hunt scope: swarms and rogue agents only.
- Inbox UUIDs stay in workspace-local state, never published.

## Base Rate Measurement (2026-10-14)

**Question:** How many benign webhook.site inboxes are created from Tencent
Cloud IPs? Without this, tier-2 (cloud) hits have unknown false-positive rate.

**Method attempted:** Sample webhook.site inbox URLs from urlquery searches
unrelated to fleet indicators, extract creator IPs, classify.

**Result:** Only 1 non-fleet-search inbox found with a retrievable UUID
(`00544500-5e78-4eb9-bf19-9085a9ddf74c`, from generic "webhook.site" query).
Creator IP: `43.163.128.176` → Tier 2 (CLOUD_SERVICE), Tencent Cloud HK
(AS132203), swarm_linked=true. UA: `curl/8.14.1` (matches fleet UA from
swarmcha.se report). Created 2026-10-08 (within fleet window).

**This sample is NOT benign** — it exhibits fleet indicators (Tencent HK IP
in 43.163.128.x near known fleet IP 43.163.128.105, fleet UA, fleet timeframe).
It was found via a generic search, suggesting fleet inboxes are discoverable
outside fleet-specific queries.

**Limitation:** urlquery htmx search returned minimal webhook.site results for
benign queries ("discord webhook", "slack webhook", "test webhook",
"api callback" all returned 0 UUIDs). A statistically meaningful base rate
cannot be established from manual sampling.

**Recommendation:** The crawler itself will build the base rate empirically.
As it processes inboxes over days/weeks, the ratio of tier-2 hits with vs
without corroborating fleet indicators (fleet UA, tag grammar, Amap URLs)
will establish the background rate. Until then:
- Tier-1 (KNOWN_SWARM): alert immediately (exact IP match, near-zero FP)
- Tier-2 (CLOUD_SERVICE): require corroboration (fleet UA OR found via
  fleet-indicator search) before alerting; log all for base-rate building
- The `swarm_linked` flag distinguishes Tencent/Alibaba ASNs from generic cloud

**Status:** Base rate UNKNOWN — will be measured empirically by crawler operation.
Do not treat tier-2 hits as standalone findings without corroboration.
