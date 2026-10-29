# FALSE-POSITIVES — Lane 7: Wayback CDX scanner

This file lists the noise the Wayback CDX scanner will see. A new capture
is not evidence of the fleet until it matches fleet target shapes: POI
pages or getPoiInfo API paths on `amap-pc-ssr.amap.com`, the pre-prod host
`pre-amap-pc-ssr.amap.com`, or the `hysandbox.tencent-cloud.com` domain.

## Anti-bot telemetry (the dominant noise)

Most captures under the `amap-pc-ssr` host are Amap's Alibaba anti-bot
endpoints: `_____tmd_____/report`, `punishTextFetch`, `page/feedback`.
The 2026-10-04 baseline found ~1,700 of 1,849 host rows were this
telemetry. The scanner flags these with `anti-bot-telemetry-noise` and
grades them MEDIUM. They show that many agent-driven page loads were
archived. They do not by themselves prove fleet activity.

## Normal archive crawling

The Wayback Machine crawls Amap on its own. A capture proves that the
crawler saw the URL. It does not prove who asked for the save, or that an
agent asked. The CDX index cannot show `web.archive.org/save/` initiator
records through host filters, so initiator claims are correlation, not
proof. Treat burst timing and parallel-capture shapes as supporting
signals, not as proof.

## Query-cost timeouts

Broad CDX queries can return HTTP 504 (query-cost timeouts, not blocks).
A zero result after a 504 means "the query was too expensive", not "no
captures". The scanner retries with 45-90 s spacing per TOOLS.md. If a
target still fails, note the gap in the run log. Do not treat it as a
clean baseline.

## Tag markers do not live here

`uqscan=` / `uq=` tags appear in urlquery scan submissions, never in
archived URLs. Do not expect them in CDX rows. Their absence is normal.

## Triage rule

Keep a hit only if the URL is a fleet target shape (POI page, POI API,
pre-prod host, or hysandbox domain) and the capture is inside the watch
window. Burst and parallel-timing analysis happens after the scan, not in
it.
