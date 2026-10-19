# FALSE-POSITIVES.md — Lane 1 (urlquery.net Amap fleet watch)

What benign activity could match each detection rule, and how the scanner
mitigates it.

Core design rule: a report becomes a hit only when >= 2 indicator families
co-occur with a combined weight >= 3 (see `INDICATORS` in urlquery.py).
No single indicator family ever emits on its own.

## 1. tag_grammar (`uqscan=`, `uqframe=`, `cachebust=1`, `uq=`) — weight 1

Benign: this grammar is widely used by unrelated urlquery users.
Observed 2026-10-14: `uqscan=` alone returns ~1,304 reports/14 days,
e.g. `example.org/?uqscan-3e69b9e9` — bots probing urlquery itself, QA
scripts, and researchers tagging their own scans. It is urlquery-adjacent
tooling vocabulary, not fleet vocabulary.
Mitigation: weight 1 only; can never emit alone. Must co-occur with an
Amap target, payload, or exfil indicator.

## 2. amap_target (`amap.com`, `gaode.com`) — weight 2

Benign: Amap/gaode are major Chinese mapping APIs. Legitimate researchers
scan them for mapping research, anti-bot studies, and API documentation.
A lone `url.domain:amap.com` hit is ordinary web research.
Mitigation: weight 2, so it still needs a tag-grammar, payload, exfil,
or label indicator to reach the threshold (2 + 1 = 3). A researcher
scanning amap.com WITHOUT the tag grammar, httpbin/base64 packing, or
webhook/ntfy exfil does not emit.

## 3. preprod_host (`pre-amap-pc-ssr.amap.com`) — weight 1

Benign: could appear in a legitimate security researcher's pre-production
recon, or in mirrored/copied fleet URLs submitted by third parties
(researchers re-scanning a fleet URL they read about — the "interrogator"
pattern observed 2026-10-07).
Mitigation: weight 1, conjunction-required. Review the submitted URL
before claiming: a submission whose URL is a byte-for-byte copy of a
known fleet payload from a public writeup is a follower, not the fleet.

## 4. httpbin_base64 (`httpbin.org/base64/<long base64>`) — weight 2

Benign: httpbin.org is a standard HTTP testing service; the /base64/
endpoint appears in countless tutorials, test harnesses, and CTF
writeups. Most hits are students and developers, not agents.
Mitigation: requires conjunction (tag grammar + amap targeting, or a
webhook/ntfy exfil indicator). The fleet signature is the CONJUNCTION
of program-packing with the tag grammar and Amap targeting — httpbin
alone is noise.

## 5. webhook_site (`webhook.site/<uuid>`) — weight 1

Benign: webhook.site is the default disposable webhook receiver for the
whole internet — tutorials, CI pipelines, and exfil-detection research
all submit webhook.site URLs to urlquery. High background rate.
Mitigation: weight 1, conjunction-required. Even with a conjunction,
check the inbox UUID against known fleet inboxes before attributing;
researchers testing the fleet's dead-drop pattern produce lookalikes.

## 6. ntfy_amapdata (`ntfy.sh/amapdata*`) — weight 2

Benign: low. The `amapdata-<POI>-<suffix>` topic grammar is specific to
the v3 "amap probe" dead-drop (POI ID embedded in topic). Generic ntfy
use does not produce this shape.
Mitigation: weight 2, conjunction-required. A bare ntfy.sh topic in a
submission without Amap context would still need one more indicator.
Watch for copycats: the topic grammar is public knowledge now; a new
submitter reusing the grammar for their own probe would match — check
submitter-side joins (IP/ASN via keyless htmx `related/ip`) before
attributing to the fleet.

## 7. label_grammar (`claudeYYYYMMDD…`, `research…`) — weight 1

Benign: any Claude-based research agent labels its runs `claude<Date>`;
"research" is generic. These labels are self-identification, and honest
researchers use them too.
Mitigation: weight 1, conjunction-required. Never use labels for
attribution alone — they are claims, not evidence.

## 8. known_submitter (`akbkyowd9geqr98`) — NOT a live rule

The constant anonymous submitter id is documented in config but the
urlquery report API exposes no submitter field (verified 2026-10-14), so
the scanner cannot match on it. If urlquery ever exposes submitter
identity, wire it in — but treat it as weak evidence: submitter ids are
cheap to rotate and could be shared or spoofed.

## 9. ip_classification tiers are signal, not attribution

- Tier 1 (KNOWN_SWARM, exact IP match): strongest single signal — an
  exact hit against the published fleet IP list is rare and worth
  immediate review.
- Tier 2 (CLOUD_SERVICE): a watchlist flag, NOT attribution. Tencent
  Cloud HK is where the fleet lives, but cloud ASNs host millions of
  unrelated tenants (adversarial review B2 in config). Treat tier-2 as
  "worth a second look", never as "fleet-confirmed".
- Tier 3/4: ordinary internet. Do not promote these into evidence of
  anything.

## Triage ordering (added 2026-10-14, from live validation)

A 10-day backfill run (143 reports screened, 47 hits) showed two
distinct hit classes:

1. **Payload-bearing hits** (httpbin_base64 + tag_grammar + amap_target,
   weight 5-6): decoded payloads are base64 HTML+JS programs that load
   amap.com in an iframe then redirect to
   `amap.com/ssr/place/<POI>?uqframe=claude<Date>` — the full fleet
   grammar. Triage these FIRST.
2. **Tag+target only** (tag_grammar + amap_target, weight 3, e.g. plain
   `gaode.com/...?uqscan=...` submissions resolving to Amap's own CDN
   IPs): weakest class, most likely benign researchers self-tagging
   their urlquery scans. Triage these LAST; do not attribute to the
   fleet on this conjunction alone.

## Residual risks (accepted)

- Copycat submissions: the full tradecraft grammar is public in hunt
  writeups. A third party reproducing it emits a hit; the hit is still a
  TRUE detection of the tradecraft, but fleet attribution needs the
  submitter-side join (Tencent Cloud HK ASN, creator IP) done by hand.
- Quiet fleet: the fleet may have moved off urlquery (v4/v5 added
  webhook.site and dropped the urlquery/robots.txt beacon). A zero-hit
  run is "no matching submissions in window", not "fleet is dead".
- API search is 429-throttled and `recent/` is broken upstream (returns
  literal null); the day-granular date filter can miss reports filed
  late in the day boundary. Re-run overlaps by a few hours for
  continuity if this becomes a scheduled watch.
