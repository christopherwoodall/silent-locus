# Reply-chain hunt — IowaCollab paste relay (2026-09-28)

Read-only, bounded hunt over the Stikked reply graph of the 4 known
IowaCollab relay pastes. Goal: surface additional relay paste IDs only via
actual reply/parent/child links found in archived view pages. No IDs guessed.

## Result: BLOCKED — Wayback upstream outage

All 4 archived view-snapshot fetches failed with upstream HTTP 500 from
web.archive.org (3 attempts each, empty response body), 2026-09-28 ~16:56 CDT:

| Paste | Snapshot URL | Status |
|---|---|---|
| df40f1f1 | https://web.archive.org/web/20260904211605/https://paste.linuxiarz.pl/view/df40f1f1 | 500 x3 |
| 538faa12 | https://web.archive.org/web/20260904161218/https://paste.linuxiarz.pl/view/538faa12 | 500 x3 |
| 34cb12da | https://web.archive.org/web/20260904141539/https://paste.linuxiarz.pl/view/34cb12da | 500 x3 |
| d379207f | https://web.archive.org/web/20260610064043/https://paste.linuxiarz.pl/view/d379207f | 500 x3 |

Consistent with the all-day Wayback flakiness (500/503/429 documented in
hidden_files/shortener-cdx/iowacollab-cdx-queue.md and the lane-12 logs).
Per the hunt's hard guard (no retry storms), the 12 queued candidate view
snapshots were NOT attempted once 4/4 primaries failed identically. They
remain queued in the CDX-queue file for a later run when Wayback recovers.

## Edge list (from local sources only — no new fetches succeeded)

- **d379207f → 34cb12da** (inreply pointer, pastebin's own reply structure).
  Evidence: incident-wiki report sect.12 (data/thecolony-ai/wiki_incident_page.html):
  "d379207f carries an inreply pointer (the pastebin's own reply structure)
  to 34cb12da -- created 2026-05-17T12:47:48Z". Re-verified verbatim in the
  local wiki HTML during this hunt. No other reply/inreply mentions exist in
  the wiki source.

No new edges discovered. No new candidate IDs. The 4 paste bodies were
previously mined (no sibling IDs/URLs/reply links in bodies).

## Candidate IDs

None discovered this run. The 12 relay-family candidates from the Sept-25
hunt archive (049f11f5, 06ee9b18, 24775389, 3470ff4e, 6e48484f, a0e61524,
a448bba6, a6b7a63d, cbc75bd1, e53f96e2, f4a8c6f2, f800c8b1) remain candidates
only — their reply blocks are still unchecked pending Wayback recovery.

## Timestamps found

None new. The 4 creation times stand as recorded in dataset.jsonl
(@timestamp from wiki sect.12 / body epoch).

## Next

Re-run this hunt when Wayback is reachable: fetch the 4 view snapshots
above, extract reply blocks, then the 12 queued candidates (2-hop cap from
known pastes). The hourly durable watch already probes Wayback availability.

## Retry run 2 — 2026-09-28 ~17:00 CDT (still blocked)

Re-attempted the 4 primary view snapshots via direct web.archive.org/web/
fetches (CDX still flapping per the durable watch; no CDX queries used).

| paste | snapshot URL | result |
|---|---|---|
| df40f1f1 | https://web.archive.org/web/20260904211605/https://paste.linuxiarz.pl/view/df40f1f1 | 500 x3 |
| 538faa12 | https://web.archive.org/web/20260904161218/https://paste.linuxiarz.pl/view/538faa12 | 500 x3 |
| 34cb12da | https://web.archive.org/web/20260904141539/https://paste.linuxiarz.pl/view/34cb12da | 500 x3 |
| d379207f | https://web.archive.org/web/20260610064043/https://paste.linuxiarz.pl/view/d379207f | 500 x3 |

8/8 primary fetches failed across both runs (16:56 and ~17:00 CDT). Per the
no-retry-storm guard, the 12 queued candidate snapshots were NOT attempted.
They remain queued in hidden_files/shortener-cdx/iowacollab-cdx-queue.md.

No new edges. No new candidate IDs. The hourly durable watch continues
probing Wayback availability; the next retry belongs to it.
