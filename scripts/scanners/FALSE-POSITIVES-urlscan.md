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
