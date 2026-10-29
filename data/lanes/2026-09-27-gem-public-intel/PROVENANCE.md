# PROVENANCE — gem-public-intel (2026-09-27)

**Dataset:** `2026-09-27-gem-public-intel` — source-reference inventory of
public reporting on the RubyGems GemStuffer campaign (May–Sep 2026), mined
from `notes/gem-public-intel-2026-09-27.md`. These are *references* (who
said what, when, where), not endorsements of their claims.

**Retrieval/observation date:** 2026-09-27. `@timestamp` = note date;
per-source publication dates in `labels.source.date`.

**Method:** systematic pass over press/threat-research/vendor coverage
(Sep 11–18 wave downstream of the Nightingale report): threat-research blogs
(Socket, Nightingale/rubyhack.ai, HivePro), the RubyGems vendor blog and
security advisory (GHSA-9j48-x3c3-mrp2), The Hacker News, The Register,
Picus, orca-ai-incident-archive, vibe-coding-security advisory synthesis,
and a press-wave aggregate. Each record carries the publisher, date, URL,
and a one-paragraph claims summary in `labels.source.claims`.

**What landed** (`events.jsonl`, 11 records): 11 `source_reference` events.

**Attribution-verified note:** no public source found mentions the go-import
meta-tag payload layer, the dead-drop chatter (`builder alive`, `YARD RAN`),
or our specific gem names — those remain exclusively ours. Public reporting
focuses on the scrape/exfil mechanics and the API-key theft attempts.

**Dedup note:** does not duplicate the RubyGems vendor advisory records in
the osv collection (those are `osv_advisory`/`finding` on the technical
advisory itself); this is a separate literature inventory.

**Fingerprint identities:** `gem-public-intel|<nn>` (01–11).
