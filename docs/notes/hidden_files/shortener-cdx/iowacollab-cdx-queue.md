# IowaCollab relay — Wayback CDX recovery queue (Lane G retry, 2026-09-28)

Wayback CDX is down (500 via CDX query path, 503/429 on availability probes,
2026-09-28 19:1xZ; the standing shortener-cdx retry loop confirms it is still
probing every 15 min). When CDX recovers, the following are queued for the
Lane G retry — no new IDs may be guessed; everything below is investigator-
or archive-sourced.

## Pending angles once CDX is reachable

1. **Re-crawl `paste.linuxiarz.pl/view/*` (2026-09-04 captures only)** and diff
   against the 333 IDs already known from the 2026-09-28 03:xx crawl. Any NEW
   Sept-4-captured IDs with title "IowaCollab" + agent handle + June-16 ts=
   bodies join the relay-family candidate pool (see lane note
   notes/iowacollab-pastes-2026-09-27.md, RETRY section).
   Exact query:
   `https://web.archive.org/cdx/search/cdx?url=paste.linuxiarz.pl/view/*&output=json&fl=timestamp,original,statuscode,digest&filter=timestamp:20260904&filter=statuscode:200&collapse=urlkey`

2. **Reply-chain check on the 12 candidate view snapshots.** Stikked renders an
   inreply/reply block on view pages. d379207f's page carried the inreply
   pointer to 34cb12da; the 12 relay-family candidates below may list each
   other as replies — that would enumerate relay siblings WITHOUT guessing.
   Fetch the `id_`-less view snapshots (not the raw variants) for:
   - https://web.archive.org/web/20260904214057/https://paste.linuxiarz.pl/view/049f11f5
   - https://web.archive.org/web/20260904173917/https://paste.linuxiarz.pl/view/06ee9b18
   - https://web.archive.org/web/20260904213208/https://paste.linuxiarz.pl/view/24775389
   - https://web.archive.org/web/20260904160027/https://paste.linuxiarz.pl/view/3470ff4e
   - https://web.archive.org/web/20260904213359/https://paste.linuxiarz.pl/view/6e48484f
   - https://web.archive.org/web/20260904214204/https://paste.linuxiarz.pl/view/a0e61524
   - https://web.archive.org/web/20260904211300/https://paste.linuxiarz.pl/view/a448bba6
   - https://web.archive.org/web/20260904204650/https://paste.linuxiarz.pl/view/a6b7a63d
   - https://web.archive.org/web/20260904210740/https://paste.linuxiarz.pl/view/cbc75bd1
   - https://web.archive.org/web/20260904202446/https://paste.linuxiarz.pl/view/e53f96e2
   - https://web.archive.org/web/20260904164244/https://paste.linuxiarz.pl/view/f4a8c6f2
   - https://web.archive.org/web/20260904214549/https://paste.linuxiarz.pl/view/f800c8b1

3. **d379207f body recovery** (second Wayback capture or the wiki author's
   Sept-4 copy). Known snapshot: 20260610064043 has an empty textarea; any
   LATER capture of https://paste.linuxiarz.pl/view/d379207f would recover it.

## Rules

- Read-only. No ID enumeration or brute-forcing: every ID above is
  investigator- or archive-sourced, never generated.
- Disk + git only (hosted Elastic write freeze in effect). Results land in the
  lane note + progress.log; dataset.jsonl only gains IDs the source report
  itself enumerates.
