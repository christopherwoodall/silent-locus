# timeline-anchors — provenance

Night-watch hunt lane (2026-09-28): cross-corpus timeline anchors. The goal
is a dated-events dataset connecting evidence ACROSS hunt lanes via time,
with 2026-06-18 as the known cross-dataset anchor.

## Method

1. Read `notes/cascade-synthesis-2026-09-28.md` (June-18 anchor list + open
   follow-ups) and swept all `notes/*.md` for dated events: campaign waves
   (May 11 rehearsal, May 12 burst, May 26/27, June 18, July 7), lane
   findings with timestamps, investigation/report publication dates.
2. Each doc carries: event date (`@timestamp`), description, lane source
   (`tags` lane:* + `labels.lane`), evidence pointer (`labels.evidence_note`
   project-relative file refs, plus `source_url` when an external URL
   exists), and `confidence` (high / medium).
3. Dates marked `*-estimated` in `labels.date_precision` are uncertain:
   press-reported dates, content-dates (not capture dates), investigator-
   reported dates not re-verified, or day/month precision where the note
   only gave that. Precision is never invented.
4. Anchor-cluster membership is an explicit tag (`anchor:june-18`) so the
   June-18 cross-dataset graph is queryable, not prose-only.

## Sources

All evidence is the repo's own notes/*.md (each lane's own write-up) and the
public reports they cite (rubyhack.ai, JFrog GemStuffer report, socket.dev,
HF/METR reports). No new network reads were made for this dataset.

## What's new

Nothing was known before: this is the first dataset that puts every lane's
dates in one index. The June-18 cluster gains two new members beyond the
known anchor list: the termina.digital actor-page documentation of the SEC
county bridge (termina-counter-lane) and the collusion.wiki translate.goog
laundering pages (lane 22), both June 18. The May 26 proxy-primitive
first-seen / RCE-gem same-day cluster is a new same-day cross-lane
correlation (previously each was a separate lane finding).

## Resumability

Deterministic: doc _ids are sha256(date + lane + description-head). The
builder appends to progress.log and rewrites the jsonl + manifest in full
each run, so re-running is safe.

## Closure 2026-09-28 (workstream C)

Closed: 48 dated-event anchor docs swept from the repo's own notes/*.md;
bounded by the lane corpus as of 2026-09-28. No new network reads were made
for this dataset; future lanes with dated findings get anchors only if a
follow-up sweep runs. ES `timeline-anchors` _count=48 verified, schema-drift
clean.
