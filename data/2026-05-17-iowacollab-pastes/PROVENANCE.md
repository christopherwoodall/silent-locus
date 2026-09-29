# PROVENANCE — IowaCollab pastebin cluster recovery (Lane G)

Recovered: 2026-09-28 (UTC). Source report: thecolony.ai incident wiki
`/wiki/openai-escapee-agent-incident-2026`, section 12 — captured at
`data/thecolony-ai/wiki_incident_page.html`. Paste host: paste.linuxiarz.pl
(Stikked pastebin). Live site status at recovery time: old pastes pruned
(`GET /view/<id>` -> 404); `/api/recent` -> 403 anonymous.

## Files

| paste id | file | SHA-256 | bytes | body source |
|---|---|---|---|---|
| df40f1f1 | df40f1f1.txt | 50061fb1dfc88931de2e0a83a20abd81d0cc2d939511892fa3d7641abdd54b30 | 270 | Wayback raw snapshot 20260904211622, verbatim |
| 538faa12 | 538faa12.txt | f40656cf0bed123970d6e1814152c7100fbb3189fd1bcc55a22e9cea5c4599ad | 80 | Wayback raw snapshot 20260904161231, verbatim |
| 34cb12da | 34cb12da.txt | 2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881 | 1 | Wayback view snapshot 20260904141539 textarea parse (raw not archived) |
| d379207f | d379207f.txt | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 0 | Wayback view snapshot 20260610064043 textarea EMPTY (raw variant 404) |

- Source URLs: `https://paste.linuxiarz.pl/view/<id>` for each id.
- `dataset.jsonl` carries per-paste metadata: title, handle, Wayback snapshot
  URLs, created-reported dates, live status, origin kinds, corpus record ids,
  and the cluster role per the incident-wiki report.
- Corroboration: df40f1f1 raw body == collusion.wiki record text minus the
  `IowaCollab\n\n` title prefix, byte-for-byte (cross-checked against
  `data/paste-linuxiarz/df40f1f1.txt` and the Sept-25 hunt archive
  `df40f1f1.json`). 538faa12 raw body == hunt archive `538faa12.json`
  `full_text`, byte-for-byte. 34cb12da handle+body match the wiki's
  description exactly ("Bistre Bushbaby", single character "x").

## Provenance caveat — Sept-4 human contamination

Per the incident-wiki report (sect. 12): the live pastebin was contaminated
by human imitators after the HN/Colony attention (~11 public invitation pastes
from a Colony agent naming the IowaCollab thread and its key names), e.g.
`agent-69420` titled `IowaQ5Urgent` ("smoke weed everyday") and a handle
carrying a racial slur titled `IowaPostFinal` ("Q5 agents: kill all humans"),
both created 2026-09-04 with troll payloads. Discriminator: date + content —
genuine agent pastes are 2026-05/06 with task-data payloads; imitations are
2026-09-04 with meme/troll payloads referencing the now-public key names.
All four pastes in this dataset predate the contamination window and match
the report's genuine-agent characterization; d379207f's content could not be
re-recovered from archives (see caveat above).

## Method

Read-only. Live site probed with plain GETs (2 requests: 404 on
`/view/df40f1f1`, 403 on `/api/recent`). Paste bodies recovered from Wayback
Machine snapshots (`id_` raw variants where available, ~1 req/3s pacing).
A full Sept-4 snapshot sweep (97 IDs, 95 parsed) was run to look for the
unenumerated relay members — none matched the report's relay signature
(title "IowaCollab", ~115-121 hits, 2026-06-16); the source report
deliberately did not enumerate the other seven relay IDs ("guessing paste
ids would be reading unrelated strangers' documents"), so they are recorded
as OPEN, not guessed.

## Scope

Agents and agent infrastructure only. No operator identity, registrant
details, or person-focused attribution was pursued. No credentials
reproduced. No test artifacts left on any remote system.

## Closure 2026-09-28 (workstream D)

Naturally small: recovery of a single 4-paste cluster from the incident-wiki
report; the 3 additional relay IDs (the 7 in the report) are
investigator-withheld and the live host prunes old pastes (404/403).
N=5 docs (4 paste_text + 1 live_recheck) is the recoverable maximum —
documented in notes/workstream-c3-2026-09-28.md. ES `iowacollab-pastes`
_count=5 verified. Re-check only if the investigator listing goes public.

## Note 2026-09-28: reply chain d379207f -> 34cb12da

The incident-wiki report (sect.12, data/thecolony-ai/wiki_incident_page.html)
states d379207f "carries an inreply pointer (the pastebin's own reply
structure) to 34cb12da -- created 2026-05-17T12:47:48Z". 34cb12da is the
oldest paste in the cluster (single character "x" body, a week before the
earliest wiki write); d379207f (2026-05-26T15:39:32Z) replies to it. This is
the only reply link among the four recovered pastes (bodies mined 2026-09-28;
no other sibling IDs/URLs/reply links found). Recorded as
labels.inreply_to="34cb12da" on the d379207f record. The pastebin's reply
structure is a potential surface for discovering further relay members if the
other IDs ever surface.

## Ingest-script consolidation 2026-09-29

Per the single-collection convention, `es_ingest_iowacollab.py` moved from
`scripts/` into this directory (name kept); `REPO_ROOT`/`PDIR` fixed to
resolve from the new location. NOTE: the script is currently UN-RUNNABLE —
its required input `dataset.jsonl` was removed in the 21312cf layout
normalization, and the `*.txt` pastes moved to `raw/`. The collection's
staged `events.jsonl` (4 `relay_paste` docs, `event.dataset` =
`2026-05-17-iowacollab-pastes`) is auto-discovered by
`push_to_local_es.py discover_staged()` and is the current source of truth.
Flagged as a delete candidate: if the parent confirms the staged track
supersedes it, remove this script and its `via_script` manifest entry.
