# Dir triage — worker W2 normalization sweep (2026-09-29)

Dirs built: 2021-05-10-vanderbilt-shortener (38 rows), 2021-10-30-demowiki
(16 rows), 2022-03-01-jsonhero (19 rows), 2022-05-14-jqp-vercel (2 rows),
2022-08-09-github-forensics (239 rows). All 314 rows validate clean against
schema/record.schema.json. No BLOCKED dirs.

## New record_kinds introduced (schema/README.md NOT edited, per task)

- `wiki_page_snapshot` (2021-10-30-demowiki) — current page-body capture at
  crawl time; identity `demowiki|page|<page_id>`.
- `repo_snapshot` (2022-08-09-github-forensics) — repo metadata snapshot;
  identity `exploitgym|repo|sunblaze-ucb/exploitgym`.
- `repo_commit` — one commit record; identity `exploitgym|commit|<sha>`.
- `repo_issue` — one issue record; identity `exploitgym|issue|<number>`.
- `repo_fork` — one fork record; identity `exploitgym|fork|<full_name>`.
- `repo_search_hit` — one repo-search result; identity
  `github|repo-search|<full_name>`.
- `gist_scan_page` — one public-gist scan page summary (exploitgym hit count).
- `related_readme` — cached README of an incident-related repo; identity
  `github|related-readme|<full_name>`.
- Registered kinds reused: `venue_probe`, `venue_finding`, `wiki_revision`,
  `corpus_hit`, `artifact_observation`, `sweep_negative`.

## Timestamp conventions used

- Real event dates where raw data carries them (cert.not_before, German
  rc_day+time_str, repo/issue/fork/commit created_at, probe probed_at,
  fi-le.net published date) with `labels.timestamp_source` naming the source.
- Retrieval date (2026-09-28) with `labels.timestamp_source="retrieved_at"`
  for DoH DNS probes and the jsonhero usage rollup derivation.
- Dir-date prefix (2022-03-01T00:00:00Z, `labels.timestamp_source="dir_date_prefix"`)
  for the 17 jsonhero corpus doc-ID records (per-ID dates not in the rollup;
  noted on-record that real usage dates live in the collusion-wiki corpus).
- Sentinel 1970-01-01T00:00:00Z +
  `labels.timestamp_source="fallback:no_recoverable_date"` for 12 of 13
  vanderbilt web mentions (no date in source).

## Removal / rename candidates noticed (evidence; no action taken)

1. `2021-05-10-vanderbilt-shortener/raw/progress.log` and
   `2022-08-09-github-forensics/raw/progress.log` — worker scratch logs with
   no dataset content (vanderbilt log: 6 lines of fetch progress; forensics
   log: retrieval notes already in PROVENANCE.md). Candidates for archival
   removal or exclusion from checksum sets. NOT removed per hard guard.
2. `2021-10-30-demowiki/raw/history_*.html` (7 files) — all byte-identical
   58-byte stub pages (`a99080ae...` shared sha256) because the OddMuse
   install rejects `action=history`; they record the limitation, not history.
   Redundant-but-harmless; keep or collapse to one representative.
3. `2022-08-09-github-forensics/raw/stargazers-p1..p12.json` — all 12 files
   byte-identical (5730cf67...), each a 401 "Requires authentication" body.
   One representative + note would carry the same information; kept as-is per
   keep-all policy.
4. `2022-05-14-jqp-vercel/raw/repo_summary.json` — derived duplicate of
   `repo_metadata.json` (same fields, prettified). Merged into the repo
   record's labels; keep for provenance.

## BLOCKED dirs

None. All five dirs had interpretable raw/ contents.
