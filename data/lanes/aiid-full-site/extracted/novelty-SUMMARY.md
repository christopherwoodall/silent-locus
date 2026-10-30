# Novelty verdicts: AIID full-site snapshot

Date of check: 2026-10-30.
Snapshot: 2026-10-26 10:15. Incident count: 1,777.
This lane is read-only. No Factum writes. No commits. No pushes.

## Counts

- NEW: 1,767
- OVERLAP: 2
- PARTIAL: 8
- Total: 1,777

## OVERLAP: do not re-ingest

- Incident 1433. Prior full ingest by the incident-7050 fleet. Factum batch 756a273f. Lane incident-7050-antigravity.
- Incident 1152. Same prior ingest. Same batch. Same lane.

## PARTIAL: mention-level only

These 8 incidents appear in prior work, but no full record exists for them.

- Incident 1424. Cite URL sits in Factum batch 756a273f as a candidate term from the incident-7050 fleet appendix. Full incident not ingested.
- Incident 1441. Same shape as 1424. Same batch. Same appendix source.
- Incident 1469. Same shape as 1424. Same batch. Same appendix source.
- Incident 373. A trajectory file in the dtap-bench-trajectories lane cites this incident as a source. The incident was not ingested as its own record.
- Incident 16. Title appears only as a related-incident link on an AIID cite page captured by the incident-7050 fleet. No independent prior record.
- Incident 46. Same shape as 16. Same fleet capture.
- Incident 68. Same shape as 16. Same fleet capture.
- Incident 1178. Same shape as 16. Same fleet capture.

All other 1,767 incidents are NEW. No cite URL, report URL, or title hit exists for them in any checked store.

## Method

Titles do not sit in the snapshot inventory file. Titles came from the snapshot incidents.csv file, matched by incident ID. All 1,777 incidents have a title there.

Checks run, for all 1,777 incidents:

1. Records scan. Exact grep for cite URLs, report URLs, and full titles over all exported Factum batches in data/records/.
2. Legacy evidence grep. Same three grep forms over evidence/.
3. Lanes grep. Same three grep forms over data/lanes/, except the aiid-full-site lane itself. This includes the Transluce tracker lane in full.
4. URL inventory grep. Same three grep forms over lists/urls/urls.jsonl.
5. Factum exact queries. Three spot checks, plus exact title queries for the 52 narrow agent, harness, and coding-tool titles. All 52 came back not found. The spot checks agree with the records scan.
6. Fuzzy checks. Case-insensitive full-title grep and 6-word title-prefix grep over data/records/ for the 235 hunt-relevant titles. Zero hits. Case-insensitive title grep over evidence/ and the Transluce lane for the same 235 titles. Zero hits. Case-insensitive title grep over records and evidence for the 4 non-hunt exact-adjacent titles (373, 16, 46, 1178). Zero hits.

Verdict rules:

- OVERLAP means a prior full ingest exists, with a batch or lane path.
- PARTIAL means a mention-level hit only, with an evidence path.
- NEW means no hit in any checked store.

## Hunt-relevant titles

Rule: the title names an agent, harness, coding tool, or autonomous system. Keyword set: agent, autonomous, autopilot, self-driving, driverless, unmanned, copilot, cursor, codex, devin, harness, chatbot, robot, coding assistant, ai assistant, auto-gpt, swe-, bot.

Count: 235 hunt-relevant incidents.

Hunt-relevant verdicts that are not NEW:

- Incident 1152: OVERLAP.
- Incident 68: PARTIAL.
- Incident 1424: PARTIAL.
- Incident 1469: PARTIAL.

The other 231 hunt-relevant incidents are NEW.

Full hunt-relevant ID list, and per-incident verdicts, sit in novelty-verdicts.json under hunt_relevant. Titles sit in that file too, verbatim from the snapshot. This summary lists IDs only.

## Coverage limits: read this before you trust NEW

- Full Factum sweep not run. One Factum query takes about 6 seconds. 1,777 queries would take hours. The task bars that sweep. The records scan covers the same bytes, and Factum reports zero pending batches. The index adds no new records past the scan.
- Lanes-wide fuzzy check is partial. Case-sensitive title grep ran over the full lanes tree. Case-insensitive title grep ran only over records, evidence, and the Transluce lane. A title stored with different case in another lane could be missed.
- Binary files skipped. The lanes grep skipped binary files. Titles or URLs inside binary blobs were not checked.
- Title-only match risk. Titles can change on the site. A prior record stored under a different title, with no cite or report URL, would be missed. The fuzzy checks cut this risk for hunt-relevant titles only.
- No network checks. No live site reads. No logins. No sessions.

## Scope gap: 5 incidents out of scope

The site count on 2026-10-29 was 1,782. The snapshot holds 1,777. The 5 added incidents have unknown IDs. They are not in this verdict set. A newer snapshot or a fresh site count must name them first.

## Output files

- novelty-verdicts.json: one verdict per incident, plus coverage and counts.
- novelty-SUMMARY.md: this file.
