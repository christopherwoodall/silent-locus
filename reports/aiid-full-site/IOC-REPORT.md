# AIID Full-Site IOC Report

## Terms used here

- IOC (indicator of compromise): a value that can point to an incident. Examples: an IP address, a domain, a file hash.
- Mention: one IOC value in one incident file. The same value in many files counts many times.
- Distinct IOC: one IOC value after dedup. Dedup means: merge repeats into one entry.
- TTP (tactics, techniques, and procedures): a short label for how an actor behaved.
- Snapshot: the set of 1,777 incidents in this pull. The live site may now hold more.

## Totals

- Mentions in: 21,370.
- Distinct IOCs out: 10,594.
- Duplicate mentions merged: 10,776 (50.4 percent of mentions).
- Incidents with extraction files: 1,775.
- Incidents with no IOCs: 1 (incident 88).
- Incidents 1152 and 1433 have no IOCs here. Their evidence lives in the incident-7050 lane. See the scope note below.
- Ranked agent-relevant distinct IOCs: 587.
- Hunt-relevant incidents in HUNT-INDEX.json: 122.

## Dedup by kind

| Kind | Mentions | Distinct | Merged |
| --- | --- | --- | --- |
| url | 13,127 | 7,955 | 5,172 |
| domain | 6,918 | 2,147 | 4,771 |
| model | 652 | 23 | 629 |
| hash | 377 | 326 | 51 |
| model_or_tool | 95 | 14 | 81 |
| file_path | 81 | 68 | 13 |
| tool | 64 | 5 | 59 |
| ip | 56 | 56 | 0 |

Notes on the table:

- Every IP value is distinct. No IP repeats across incidents.
- Model and tool names repeat a lot. Few names cover many incidents.
- The kind `model_or_tool` overlaps the kinds `model` and `tool`. One name can appear under two kinds. Example: ChatGPT appears as `model` and as `model_or_tool`. This is faithful to the extraction files. It is not an error.
- URL query-strip merged only 4 values (7,959 raw distinct URLs down to 7,955). Most URLs had no query string. 84 URL mentions with a query string in extraction collapse to 74 distinct URLs after dedup; those 74 now carry parameter names only, in the form `?params=name1,name2`. No query value is carried. No token is carried. No signed value is carried. Two narrow exceptions, both kept verbatim: one distinct URL keeps `=` in a path segment (an Amazon ref segment, not a query value), and one `?params=` entry carries a path-like value, not a parameter name (incident 1162).

## Top 20 hunt-relevant IOCs

Order: agent tools first, then IPs from named agent incidents, then top model names. Counts are incident counts.

Agent tools:

1. Copilot (tool) — 26 incidents.
2. Claude Code (tool) — 23 incidents.
3. Cursor (tool) — 13 incidents.
4. Devin (tool) — 1 incident (1118).
5. AutoGPT (tool) — 1 incident (1764).

IPs from named agent incidents:

6. 199.247.25.25 (ip) — incident 1766 (Cairn panel case).
7. 199.247.27.2 (ip) — incident 1766 (Cairn panel case).
8. 43.246.208.207 (ip) — incident 1669 (Hermes case).
9. 144.172.64.60 (ip) — incident 1781 (ARTEX case).
10. 144.172.64.99 (ip) — incident 1781 (ARTEX case).
11. 144.172.64.128 (ip) — incident 1781 (ARTEX case).
12. 104.28.157.50 (ip) — incident 1670 (marimo notebook case).
13. 104.28.165.169 (ip) — incident 1670 (marimo notebook case).
14. 157.66.54.26 (ip) — incident 1670 (marimo notebook case).
15. 104.194.134.167 (ip) — incident 1661 (Aurora case).
16. 45.142.31.17 (ip) — incident 1661 (Aurora case).
17. 93.157.139.115 (ip) — incident 1661 (Aurora case).

Top model names:

18. ChatGPT (model) — 228 incidents.
19. Claude (model) — 93 incidents.
20. Gemini (model) — 83 incidents.

Full ranked set: 587 distinct IOCs in `iocs.json` under `ranked_agent_relevant`. It holds all model and tool names, all IPs from incidents 1661, 1669, 1670, 1766, 1781, and 1118, and all IOCs attached to agent-titled incidents (67 incidents match the agent title rule). Each ranked entry carries a `rank_reason` field.

## Caveats

Read these before you use any IOC.

- Hash: hash values are hex strings copied from report text. They are NOT verified file hashes. Do not use them to block files. Confidence: low.
- IP: some IP values look like quoted network addresses. Five end in `.0` (for example 104.28.0.0 and 131.0.0.0). Some sit in shared fronting ranges. They are not confirmed actor infrastructure. Network-address forms carry confidence low. Other IPs carry confidence medium.
- Domain: most domains are press source links cited by reports. They are not threat infrastructure. Do not treat a press domain as hostile. Confidence: medium.
- URL: URLs are cut to host plus path shape. Query values are dropped. URLs with a `{segment}` placeholder are page templates, not real pages. They carry confidence low. Other URLs carry confidence medium.
- Model and tool names: these names are stated in report text. They are not confirmed use. Known agent tools (Claude Code, Copilot, Cursor, Devin, AutoGPT) carry confidence high. Other names carry confidence medium.
- File path: paths are stated in report text. They are not confirmed on-disk artifacts. Confidence: medium.
- Confidence counts in the full set: high 6, medium 8,247, low 2,341. Low-confidence IOCs are kept and flagged. Nothing is deleted for low confidence.
- No personal names are used in this report. Incident titles in HUNT-INDEX.json are kept verbatim from the source. They are incident titles, not extracted personal data.

## Method note

- Inputs: extraction files `e1-1-900` (889 incidents, 13,896 IOCs) and `e2-901-1788` (886 incidents, 7,474 IOCs). Total: 21,370 mentions.
- Dedup key: (kind, normalized value). Domains are lowercased. URLs are lowercased at host only, cut to host plus path shape, with query strings replaced by parameter names only. Model and tool names dedup case-insensitively, shown in their most common observed form.
- Provenance: each IOC keeps `incident_ids[]` and `report_ids[]`. Report page URLs follow one pattern: `https://incidentdatabase.ai/reports/<id>`. Report IDs are stored as numbers only. No full report URL is repeated per report.
- HUNT-INDEX.json holds one entry per snapshot incident (1,777). Each entry holds: incident_id, title, date, novelty verdict, evidence paths, behavior count, TTP slugs, deduped non-URL IOC values, URL IOC count, and a hunt_relevance flag. Full normalized URLs live in `iocs.json`, not in the index, to keep the index small.
- Hunt_relevance is true when the title names an agent, harness, coding tool, or autonomous system, or the incident carries a tool-kind IOC, a named agent-tool IOC, or an agent-relevant TTP slug. This rule gives 122 incidents. The novelty file lists 235 hunt-relevant titles under a wider rule. The two counts differ by rule, not by error.
- TTP slugs: 42 incidents carry at least one established TTP slug. Other incidents carry behaviors with no established slug.
- Evidence paths point at fetch files in this lane (`data/lanes/aiid-full-site/raw/fetch/f1-1-450/`, `f2-451-900/`, `f3-901-1350/`, `f4-1351-1788/`). Only files present on disk are listed.
- Scope notes:
  - Post-snapshot gap: 5 incidents arrived after this snapshot. Their IDs are unknown. They are not entries in HUNT-INDEX.json.
  - ID-number gaps in range 1–1788 with no snapshot record and no novelty entry: 90, 130, 237, 247, 269, 338, 342, 365, 442, 512, 542. These are ID numbers with no record in this lane. They are not counted as missing incidents.
  - Incidents 1152 and 1433: no extraction and no fetch files in this lane. Evidence pointer: `data/lanes/incident-7050-antigravity/raw/novelty/cite-1152.html` and `cite-1433.html`, plus `bundle.json` in the same lane. Prior Factum batch 756a273f. Their dates are not in this lane, so date is null in the index.
- No network use. No Factum writes. No commits. No pushes. Read-only work except the three output files.

## Outputs

- `reports/aiid-full-site/iocs.json` — ranked section, full set, counts, caveats. Valid JSON.
- `reports/aiid-full-site/HUNT-INDEX.json` — 1,777 incident entries plus scope notes. Valid JSON.
- `reports/aiid-full-site/IOC-REPORT.md` — this file.
