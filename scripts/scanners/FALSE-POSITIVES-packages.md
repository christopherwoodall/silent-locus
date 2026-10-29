# FALSE-POSITIVES.md — Lane 7 (revised): package registry scanner

Scanner: `scripts/scanners/packages.py` (RubyGems / PyPI / npm).
All hits are grade SECONDARY (other people's artifacts, found by us).

## Honest-zero baseline (expected NO public hits)

These indicators have zero legitimate use outside the fleet. Any hit is
HIGH confidence and warrants immediate review:

- `hysandbox-ats` (proxy marker; zero public hits as of Oct 2026)
- `uqscan=`, `uqframe=`, `uqtag=` (fleet tag grammar)
- `akbkyowd9geqr98` (submitter ID)

A run that returns nothing on these is the NORMAL outcome, not a failure.
Record the zero; do not widen the patterns to manufacture hits.

## Per-registry false-positive profiles

### RubyGems
- **oai* name prefix (MEDIUM):** the `oai` prefix is crowded with legitimate
  OpenAI client libraries and forks (e.g. the `ruby-openai` ecosystem).
  Recency filter (30 days) keeps this list small; older hits are dropped.
  Treat a fresh `oai-*` gem as a lead only with a second indicator
  (suspicious author, uq*/hysandbox string, POI regex).
- **amap in name (LOW/MEDIUM):** legitimate Gaode/Amap SDK gems exist for
  the Chinese mapping market. "amap+geo-context" MEDIUM requires a geo/POI
  context word; bare "amap" is LOW noise.
- **Compact-index name sweep:** matches names only. Description text is
  checked separately via the search API + per-gem metadata fetch, because
  the real prior campaign was Diffend-indexed (file contents), which no
  public API exposes. A clean name sweep does NOT clear file contents.

### PyPI
- **No server-side search exists** (XMLRPC search disabled 2023, verified
  2026-10-14). Coverage is the RSS recent-updates feed (~last 100
  releases) plus cross-registry name lookups. A package older than the RSS
  window with a fleet indicator will be missed unless the same name hit on
  RubyGems/npm. This is a documented coverage gap, not a clean bill.
- **"swarm/fleet term" (LOW):** extremely noisy. Example from the first
  dry-run: `willows-grove` — "The operator's seat for the Willow AI fleet".
  Legitimate multi-agent framework marketing. Never escalate on this
  indicator alone.
- **Version strings vs IPs:** the IP extractor will read dotted quads like
  `1.2.3.4` in changelogs/build tags as IPv4. They classify as tier 4
  UNKNOWN and are ignored. If a "version" ever classifies tier 1/2, treat
  it as real signal and verify by hand.

### npm
- **`oai` text query:** the noisiest query in the module. npm hosts legions
  of `oai-*` OpenAI wrappers. The 30-day recency filter plus the
  MEDIUM-for-prefix-only rule keeps this manageable; bare-"oai"-in-
  description matches are LOW.
- **`amap` text query:** legitimate Gaode JS SDKs (`amap-jsapi` family are
  official). Same rule: needs a second indicator or rare-marker match.
- **Search relevance cap:** `size=250` returns the top 250 by npm's
  relevance ranking, not the most recent. A very recent low-relevance
  package can fall off the page. Mitigation: the `date` field is checked
  per candidate and rare indicators are never dropped.

## IP classifier notes (standing rule)

Every IP literal found in package metadata (descriptions, homepage and
project URLs, changelogs) is classified via `ip_classifier.classify_ip`
and stored inline as `ip_classification`. Tier 1 (KNOWN_SWARM) and tier 2
(CLOUD_SERVICE) set `priority: true`.

- A cloud IP in package metadata (e.g. a Tencent Cloud HK IP in a
  homepage URL) is NOT filtered — per the standing rule, an unexpected
  cloud IP is signal. Flag it, do not drop it.
- `priority: true` is a routing flag for alerts/morning breakdown, not a
  verdict. Tier 2 on a legitimate cloud-hosted docs site is expected;
  tier 1 is not.

## Confidence discipline

- HIGH: exact rare marker. Act on it.
- MEDIUM: tooling pattern (getPoiInfo, amap-pc-ssr, POI ID regex,
  oai* prefix, cross-registry name reuse). Lead, needs corroboration.
- LOW: bare terms. Log and move on; bulk LOW hits are the noise floor.
