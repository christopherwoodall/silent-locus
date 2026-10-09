# PROVENANCE — librariesio-pattern-battery (2026-09-28)

**Dataset:** `2026-09-28-librariesio-pattern-battery` — structured measurement
from the libraries.io pattern-battery hunt: 2,698 campaign-related package
names checked against libraries.io's RubyGems mirror; 1,609 live pages found,
1,191 carrying go-import payloads in their descriptions.

**Retrieval/observation date:** 2026-09-28. `@timestamp` = note date
(`labels.timestamp_source=note:publication_date`).

**Method (per `notes/gem-hunt-pattern-battery-2026-09-28.md`):** direct
project-page fetches over generated name lists (`try[a-z][0-9]zz` = 231
combos), the JFrog inventory grammar battery (648 names), and the remaining
JFrog inventory (1,819 names); mechanism-marker greps over descriptions; no
login or API key. 1,115/3,027 names missing from libraries.io (time-freeze
effect from the May-12 burst). Raw census artifacts live in
`hidden_files/lane1/` (not dataset raw/ — excluded per repo convention).

**What landed** (`events.jsonl`, 9 records): one `finding` per structural
result (battery summary, July-7 mirror, oai echo-rig, May-8/9 pre-waves,
June-18 mirror, tryzz exhaustion, author-field blind spot, wave timeline)
and one `sweep_negative` (webhook/A000 markers absent from descriptions).

**Key numbers:** battery summary 2,698 checked / 1,609 live / 1,191
go-import payloads; July-7 mirror 55 gems (03:30–06:15 UTC); oai echo-rig 123
gems (May-11 09:50–10:35 UTC); June-18 mirror 55 gems; tryzz 0/231.

**Dedup note:** no existing collection carries libraries.io census records
(verified by grep across all `events.jsonl`). The July-7 XSS/SSTI census and
GemStuffer CSV carry the same *gems* but not the libraries.io mirror
observations (atom dates, description payloads, echo-rig family) — those
are new here.

**Fingerprint identities:** `librariesio-battery|<result-slug>`.
