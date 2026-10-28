# slot-2 (urlquery fresh) sweep summary — 2026-10-28T23:40–23:44Z

Window: last ~24h of urlquery reports (lane-1 rolling 24h; direct grammars
date:[2026-10-27 TO 2026-10-28]).
Method: lane-1 scanner (12 families, limit 30) + 6 direct grammar re-queries,
authenticated API via ~/workspace/skills/urlquery/bin/uq.py, ~4s spacing.
All 6 direct queries exit 0; all 6 .err files empty.

Scanner result: 32 reports screened, 0 hits (same count as 17:40Z run).

Direct grammar results (all set-equal to the 17:40Z run, 0 new IDs):
- `uqtag=` -> 0 (was 0)
- `uqframe=` -> 0 (was 0)
- `uqscan=` -> 0 (was 0)
- `url.domain:jcburrows.workers.dev` -> 0 (was 0)
- `webhook.site` -> 2, both exact repeats of prior-run rows by report ID:
  4eb81c80-8245-4ae9-a1a2-7e1433b21e00 (2026-10-27T05:31:07Z) and
  4f988500-bdd9-4129-8a66-f7804d33e0d2 (2026-10-27T05:16:19Z), both
  hypery11.github.io/sp-create-html self-beacon test pages (HITCON CTF
  beacon token page), tags empty, no webhook.site UUID in URL/tags/title.
  No new webhook rows.
- `ntfy.sh` -> 1, same row as 17:40Z:
  1cd301c8-46f5-403c-9c55-cf2f7c6cd20f (2026-10-28T16:21:05Z),
  submitted URL http://project-6kd41-47zn3t3ix-artxus-projects.vercel.app
  ("ARTXUS — Galería del Colegio"), tags empty, no ntfy topic in
  URL/tags/title, and the only "ntfy" occurrence in the returned JSON is
  the query echo itself. Classified as page-content noise (q matches page
  content, not the submitted URL), same noise class as prior ntfy rows.
  No topic is visible, so no topic was polled; ntfy was NOT polled
  directly — the observer-effect pause test runs until 2026-10-29
  ~12:00 CDT, so ntfy coverage here is urlquery API rows only.

Verdict: NO NEW LEAD. All rows triaged against FALSE-POSITIVES-urlquery.md
noise classes; the only webhook rows are the known hypery11 CTF-beacon
pair, already triaged in prior runs, and the single ntfy row is
page-content noise with no agent indicators.
