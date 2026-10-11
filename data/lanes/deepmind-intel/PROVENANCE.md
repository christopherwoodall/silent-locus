# PROVENANCE — deepmind-intel lane (Google / DeepMind egress-IP mining)

Worker: ip-mining-deepmind (Google/DeepMind lane of the provider egress-IP mining fleet).
Date: 2026-10-11.
Lane tag: `deepmind-intel`.

## Sources

1. `https://www.gstatic.com/ipranges/goog.json` — Google's official "Google IP ranges" list
   (used by *.googleapis.com endpoints).
   - Retrieved: 2026-10-11T01:06:15Z, via `curl -sSL` (egress proxy OK).
   - sha256: `974e61b3d72854914788c1eacc7d1b55e5ae403b24ea15b8d61533642cef3df0`
   - File syncToken: `1791662736520`; creationTime: `2026-10-10T13:05:36.520714`.
   - Content: 145 prefixes (130 IPv4, 15 IPv6). No service or product attribution fields.
   - Cached: `raw/goog.json`.

2. `https://www.gstatic.com/ipranges/cloud.json` — Google's official "Google Cloud IP ranges" list.
   - Retrieved: 2026-10-11T01:06:15Z, via `curl -sSL`.
   - sha256: `aa20b59633470d7262819d459c93b46880f68e0f8259751f564ec69b768f4356`
   - File syncToken: `1791662736520`; creationTime: `2026-10-10T13:05:36.520714`.
   - Content: 1127 prefixes (1032 IPv4, 95 IPv6). Every entry has `service: "Google Cloud"`;
     `scope` is the Cloud region (us-central1, europe-west1, ...). No per-product attribution
     (no entry names Gemini, Vertex AI, or any agent product).
   - Cached: `raw/cloud.json`.

3. `_cloud-netblocks.googleusercontent.com` TXT (SPF) records.
   - Direct UDP DNS refused by the local resolver; retrieved via DNS-over-HTTPS
     (`https://dns.google/resolve?name=_cloud-netblocks.googleusercontent.com&type=TXT`),
     2026-10-11 ~01:07 UTC, following the include chain `_cloud-netblocks1..5`
     (chain references 6 and 7; not followed).
   - Content: same Cloud netblocks in SPF `ip4:`/`ip6:` form (e.g. `8.34.208.0/20`,
     `35.184.0.0/14`, `2600:1900::/35`). No product attribution. Supplementary only;
     not ingested as records.

4. `https://developers.google.com/gemini-code-assist/docs/configure-vpc-service-controls`
   (fetched 2026-10-11, curl, 143910 bytes, saved to staging only).
   - States requests to the Gemini service are routed to the restricted VIP range
     `199.36.153.4/30` (`restricted.googleapis.com`) under VPC Service Controls.

5. `https://cloud.google.com/vpc/docs/configure-private-google-access-hybrid`
   (fetched 2026-10-11, curl).
   - Documents Private Google Access VIPs:
     `private.googleapis.com` = `199.36.153.8/30`, `2600:2d00:0002:2000::/56`
     ("API access to most Google APIs and services");
     `restricted.googleapis.com` = `199.36.153.4/30`, `2600:2d00:0002:1000::/56`
     ("API access to Google APIs and services supported by VPC Service Controls").

## Selection methodology (GIANT-LANE RULE)

Google publishes 1,272 prefixes across the two lists and attributes none of them to
specific products: `goog.json` carries no service field at all; `cloud.json` labels every
entry `service: "Google Cloud"` with only a regional `scope`. Web documentation confirms
that Vertex AI and the Gemini API are served through the shared *.googleapis.com endpoint
family (plus customer-VPC constructs for private traffic), not through dedicated
product netblocks. Ingesting all 1,272 prefixes 1:1 would add noise with zero
product discrimination, so per the giant-lane rule it was NOT done.

What was ingested instead:

- The two authoritative lists themselves, as `capture` records (source + artifact +
  `web.capture` observation, `--storage git`): URL, retrieval timestamp (UTC), and the
  sha256 above are in record provenance. This is the "list reference" required by the
  work order, preserved with bytes and a content hash rather than 1,272 CIDR records.
- Four product-relevant VIP ranges that Google's own documentation ties to Gemini/API
  serving, as `infra.ioc` records (`category: ip`, `status: active`, grade UPSTREAM):
  - `199.36.153.4/30` — restricted.googleapis.com (IPv4). Google's Gemini VPC-SC doc
    states the Gemini service is served at this VIP.
  - `2600:2d00:0002:1000::/56` — restricted.googleapis.com (IPv6), same doc page.
  - `199.36.153.8/30` — private.googleapis.com (IPv4). Documents "most Google APIs and
    services", i.e. the *.googleapis.com endpoint family that hosts the Gemini API and
    Vertex AI public endpoints.
  - `2600:2d00:0002:2000::/56` — private.googleapis.com (IPv6), same doc page.

## Overlap check against the corpus burst IPs (rmn.re Aug-Sep 2026 burst creators)

Each of `185.228.3.86`, `185.228.3.47`, `185.228.3.66`, `105.71.5.91`, `45.130.202.7`,
`159.26.105.49` was tested against every prefix in both JSON lists with Python
`ipaddress`: **clean negative** — zero hits. (Observed by local computation, not a
Factum search.)

## Grades

- List files and VIP ranges: UPSTREAM (vendor-published facts).
- The claim "no per-product attribution exists in the published lists": INFERENCE from
  the parsed JSON schemas (fields observed).
- Overlap result: OBSERVED (local computation over retrieved bytes).

## Cache

`raw/goog.json`, `raw/cloud.json` — byte copies of the retrieved lists with the sha256
values above.
