# FALSE-POSITIVES — Lane 6: urlscan.io scanner

This file lists the noise the urlscan.io scanner will see. A hit is not
evidence of the fleet until the fleet markers are present. Fleet markers:
`getPoiInfo` in the scanned URL, `uqscan=` / `uqframe=` tags, the
`hysandbox` proxy marker, or fleet POI page shapes on amap.com / gaode.com.

## Known name collisions (from the 2026-10-04 sweep)

- **Azure hostnames.** `amap-intcusa-sts-db-1.postgres.database.azure.com`
  and `amap-nprcusa-primary-vcp-db...` — "amap" is an internal naming
  prefix here, not the Chinese map service. Ignore.
- **amapacad.org.ng.** Association of Marketing Academic Professionals.
  "AMAP" is an acronym collision. Ignore.
- **jec.jlevm.cn.** Jilin new-energy monitoring platform. It uses the Amap
  map SDK in a normal way. No fleet tags, no fleet titles, no program
  staging URLs. Ignore.
- **httpbun.com /mix/... test URLs.** Feature-test paths such as
  `/mix/s=200/h=.../b64=...` are generic test snippets. The fleet uses the
  `/base64/` program-staging pattern. `/mix/` is not the fleet pattern.
  Ignore unless Amap appears in the same scan.
- **livecodes.io demos.** Demo pages (for example "My Awesome Project")
  with no fleet markers. Ignore.
- **mianyang collisions.** `18jx-nk.cyou` (typosquat) and
  `cloudflare-imgbed-atb.pages.dev` (image-bed demo). No fleet markers.
  Ignore.

## Search limits that cause misses, not negatives

- Anonymous search covers only the **last 30 days**. A zero means "no
  fleet pages in the last 30 days of urlscan", not "never".
- Leading-wildcard searches are blocked (HTTP 403) for anonymous users.
  Queries use exact terms and `domain:` / `page.title:` scoping instead.
- Full result bodies need a login. Anonymous verdicts rest on search
  metadata only: URL, title, scan date. Do not claim a finding is new
  without checking the full body in a logged-in session.

## Triage rule

Keep a hit only if it carries at least one fleet marker above, or a
HIGH-confidence grade from the scanner. Everything else in this file is
routine noise.

## Opt-in relay/proxy queries (disabled 2026-10-20, counsel judge)

Six domain-presence queries exist but stay disabled. Enable only after
per-query review. Domain presence alone never proves fleet use. All six
carry a LOW confidence cap and SECONDARY grade: urlscan hits are other
people's scan metadata, not our direct observations.

- **domain:jqp.vercel.app.** Fleet proxy relay. Corroborated in the
  2026-10-10 relay sweep (2026-10-01-intermediary-relays). Benign
  collisions: other people's Vercel hobby apps, researchers scanning
  their own relay test apps, link-preview fetchers. Keep only hits
  with fleet markers (tag grammar, getPoiInfo shape, uqscan=/uqframe=).
- **domain:vanderbi.lt.** Fleet relay host. Benign collisions: the .lt
  service itself gets scanned by security researchers and crawler bots.
  A scan of the relay front page is not fleet traffic.
- **domain:ntfy.envs.net.** Operator-run ntfy instance. It is NOT the
  public ntfy.sh utility. Do not confuse the two: ntfy.sh hits belong
  to a different surface and are out of scope for this lane. Benign
  collisions: people testing their own ntfy self-host, Shodan-style
  crawlers, the instance operator's own health checks. Keep only hits
  showing fleet dead-drop topic shapes (amapdata-*, fleet-*).
- **domain:itty.bitty.site.** URL expander service. Benign collisions:
  normal users expanding short links, browser extensions calling the
  expander API. Keep only hits with fleet markers.
- **domain:cors.bwa.workers.dev.** CORS relay on Cloudflare Workers.
  Benign collisions: web developers routing their own requests through
  it, automated scans of the whole workers.dev space. Keep only hits
  with fleet markers.
- **domain:pingllo.com.** Benign collisions: the service's own users,
  researchers probing the service. Keep only hits with fleet markers.

## Sensitive hits

urlscan page_url fields can carry tokens. A token is a capability
bearer: a UUID in the URL that grants access to a scan result, a
dead-drop topic, or an API key in a query string.

- Hits are captured verbatim. The never-redact rule applies. Do not
  strip tokens from stored evidence.
- Token-bearing hits get sensitivity tags. Storage is local-only.
- No public push of token-bearing hits without BigSexyWarlock69's word.
- Code does not redact. Redaction in code would hide real evidence.
  Triage happens at review time, not in the scanner.
