# DELTA — Monitorable_Surfaces v2 (NEW operator file vs Oct-22 ENRICHED file)

Match rule: normalized URL (lowercase, strip `http(s)://`, strip leading `www.`, strip trailing `/`).
Machine detail: `DELTA.json` in this directory.

## Counts

| Area | NEW | OLD | Added | Removed | Changed |
|---|---|---|---|---|---|
| Agent POIs (real rows) | 96 | 96 (+1 stray header row) | 0 | 0* | 90 (89 cosmetic, 1 substantive) |
| Intelligence and reporting URLs | 22 | 23 | 0 | 1* | 16 (sheet restructure) |
| Notes | 57 | 57 | — | — | none |
| Appendix | 33 | 55 | — | — | field-dictionary block dropped |
| Template | 35 | 35 | — | — | none |

\* The single "removed" row in both sheets is the same artifact: OLD file row 5 of Agent POIs is a
literal repeated header (`URL | Type | Class | Capabilities | ...`), and the intel sheet carries a
matching stray `url` row. Neither is a real surface — the NEW file correctly drops both. There are
**no true added or removed surfaces**.

## Agent POIs — added
None. All 96 NEW surfaces match 96 OLD surfaces by normalized URL.

## Agent POIs — removed
None real. OLD row 5 (`URL` = literal string "URL") is a stray duplicate header row, dropped in NEW.

## Agent POIs — changed: 89 cosmetic
Every one of these 89 rows changed in exactly one field, **Ops & Artifacts**, and only by
un-escaping LaTeX: OLD `$\rightarrow$` → NEW `->`. Content is otherwise identical.
NEW rows affected: 4–12, 14–15, 18–27, 29–90, 94–99. No content was added, removed, or reworded.

## Agent POIs — changed: 1 substantive (REGRESSION — enrichment lost)

| URL | agents-agents-agents.com (NEW row 28 / OLD row 30) |
|---|---|
| Ops & Artifacts | cosmetic only: `$\rightarrow$` → `->` |
| **Direct Links** | OLD: `https://agents-agents-agents.com` → NEW: **(empty — cleared)** |
| **Seen** | OLD: `trajectory-domains Tier 1; 24 Factum records; agent board (llms.txt), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established.` → NEW: `https://agents-agents-agents.com` |

The Oct-22 enrichment was degraded on this row: the Direct Links URL was moved into Seen and
Direct Links was emptied, replacing the full "Seen in" attribution note with a bare URL. If the
v2 build re-applies enrichment, this row needs its OLD Seen text restored and its Direct Links
value reinstated.

## Agent POIs — unchanged (6 rows)
NEW rows 13, 16, 17, 91, 92, 93 are byte-identical to their OLD counterparts (modulo normalization).

## Enrichment carry-over in the NEW file
- Direct Links filled on 95/96 NEW rows (all except agents-agents-agents.com) — Oct-22 enrichment retained.
- Seen filled on 63/96 NEW rows; 33 rows have Seen empty, same as OLD (these were never enriched).
- Net: the NEW file already carries the Oct-22 enrichment everywhere except the one regression above.

## Intelligence and reporting URLs
- 22 NEW vs 23 OLD data rows; no adds; 1 removed = the stray `url` junk row.
- 16 of 22 rows changed — this is a genuine **sheet restructure by the operator**, not cosmetic:
  - Classification: prose phrases → machine tags (e.g. `INTEL_BLOG, INCIDENT_RESEARCH`,
    `MALICIOUS_CAIRN_PANEL`, `IOC_FEED`, `CERTIFICATE_TRANSPARENCY`).
  - Direct source links: previously held prose/URLs mixed into other columns → now holds raw
    URLs only (moved out of "Use in the Collection System").
  - Use in the Collection System: now holds prose descriptions instead of bare URLs.
  - Attribution / seen in: now holds hunt/watch notes (e.g. `Cairn phase-2, Counsel MALICIOUS |
    Watch: cairnwatch (disabled, needs his word)`) instead of single tokens like
    `intelligence_source` / `c2_panel`.
- 6 intel rows unchanged. Full per-row diffs in `DELTA.json` → `intel_urls.changed`.

## Notes / Appendix / Template
- **Notes**: 57 rows both; tail content identical (review-flag rules, intel-sheet note, 2026-10-22
  correction). No material change.
- **Appendix**: NEW 33 rows vs OLD 55. NEW drops the 17-row Field/Meaning data-dictionary block
  (`service_id`, `canonical_name`, `instances`, `service_type`, `capabilities`, `interfaces`,
  `artifacts`, `collection_method`, `access_scope`, `freshness`, `priority`, `confidence`,
  `incident_role`, `mappings`, `provenance`, `limitations`) present at OLD rows 43–59. The
  Tag/Definition table (NEW rows 5–33 ≈ OLD rows 7–35) is otherwise the same content with a minor
  layout shift (Service Profiles / Class / Capability headers).
- **Template**: 35 rows both; identical tail (2:20 PM / Arrive / 4:15 PM / SEA). No material change.

## Possible duplicates
None found — no two NEW Agent POIs rows share a base domain (path variants do not exist in the set).

## Matching ambiguities
None. Normalized-URL matching was 1:1 across all 96 rows in both directions; no collisions,
no ambiguous pairs.
