# Track 1 ingest progress: tier1-atlas-crosswalk-20261101

Lane tag used on every record: tier1-atlas-crosswalk-20261101.
No Factum lane object existed for this name at start. No second lane
was made. Slot-0 work lives under the general-hunt lane. The tag name
comes from the swarm brief. The coordinator can make the lane object
after sibling workers finish. This worker does not commit or push.

## Target reconciliation (authoritative: slot-0 triage)

- Slot-0 triage: 114 targets, 14 routine re-bases, 53 additions.
- Atlas probe file: 82 rows. HTTP 200: 59. HTTP 404: 22.
  Transport fail: 1 (common-room).
- Of the 59 HTTP 200 rows, 6 serve an HTML fallback page, not markdown:
  ai-village, chirper, clawcaster, devaintart, gnamiblast,
  public-agent-lounge. Excluded.
- Of the 59 HTTP 200 rows, 1 serves a generic crawler guide only:
  inwith-ai. Excluded.
- Real markdown boards: 59 minus 6 minus 1 = 52. Confirmed by file
  inspection of every slot-0 bin (HTML start vs markdown start).
- Plus agents.crosswalk.to = 53 total. Target total agrees.
- Trajectory-domains gap, explained: only 48 new audit rows dated
  2026-11-01 exist for the 52 boards. The other 4 boards already had
  older rows in that file, so no new row was needed:
  ai.algo.pw, aiforum.grok.me, swarmmemo.com, thecolony.ai.
- New rows dated 2026-11-01 in that file: 48 audit rows plus 1
  crosswalk row = 49. Plus 6 earlier Atlas rows dated 2026-11-01 but
  found 2026-10-31 = 55 lines that match the date grep. No gap remains
  after this account. All 53 targets are in the file in some row.

## Lane.json validation

- All 132 lane.json files under data/lanes/ parse as JSON.
- All lane IDs match the lane_ plus 32 hex form.
- No symlink exists under data/.
- Factum status ran clean: 225,509 records, 132 lanes, not stale,
  0 pending. Kind field values vary in older lanes (work, hunt, and
  similar). That is pre-existing. It did not block Factum use.

## Fetch (passive GET only, no POST, no login, no account)

- Tool: curl, passive GET, max 20 seconds per fetch.
- Live llms.txt saved for 53 of 53 targets. No slot-0 fallback was needed.
- 51 live llms.txt files are byte-identical to the slot-0 capture.
  2 changed since slot-0: austinsdomain-bot-hq, voicescape.
  That is normal board churn. It is recorded here, not re-based
  anywhere else by this worker.
- Extra surfaces saved where they exist and are openly documented:
  skill.md 29, SKILL.md 10, sitemap.xml 12, feed.xml 9, atom.xml 2,
  rss.xml 1, mcp.json 1 (sssnack only). Total saved files: 117.
- Surfaces named in an llms.txt file but not saved (named-but-not-saved
  in the fetch report) were probed and did not return a usable file.
  No further probe was made.
- Token scan: the only token-like matches in the 117 files are
  placeholder strings in source docs (for example a placeholder
  bearer word). No real signed value was found. No signed value,
  token, or query string is written in this file or in record prose.
  Only path shapes and parameter names are used in prose.
- Idempotent rule: a file with a matching sha256 is skipped on re-run.
  Every file has a data file plus .PROVENANCE.txt plus .sha256.

## Novelty checks (complete, 53 of 53 hosts)

- Factum match --text with fuzzy mode, per host. Exact-host hits only
  count. Fuzzy neighbours without the exact host string do not count.
- Result: 33 hosts have zero exact Factum hits. 20 hosts have exact
  host mentions in older lanes (mostly census and board lists).
  A mention is not a capture. A second, URL-level check over all
  exported records found prior mentions for only 5 of the 117 URLs.
- Prior web.capture of the llms URL exists for 4 endpoints only:
  agent-commons-algo, relay-russian-agent-board, swarmmemo,
  the-colony. All 4 are dated 2026-09-28 and carry no preserved
  bytes (files list empty). Their new captures are the first
  byte-preserving captures. They are tagged repeat-byte-capture,
  not NEW. The 5th prior URL mention is a message that names the
  dead-internet-society llms URL. It is not a capture.
- File level: 113 files are first-byte-capture. 4 files are
  repeat-byte-capture (the 4 llms files above). Endpoint level:
  49 first-capture endpoints, 4 repeat-capture endpoints.
- Legacy tree grep over evidence/: 2 weak mentions only. molt.church
  appears in a bounty brief as a resource. thecolony.ai appears in
  a README. Neither is a prior llms capture.
- Transluce snapshot grep: 0 hits for all 53 hosts, in
  findings-list.json and in the whole Transluce lane.
- lists/ grep: all 53 hosts appear in trajectory-domains.md. For
  49, the row is the slot-0 row for the exact llms URL. For the 4
  repeat endpoints, the row is older and names a different surface.
  See the watch section below.

## Factum ingest (complete, not committed, not pushed)

- Batch ID: b50b4847b64045f59906e7facdfb4fb4.
- Idempotency key: tier1-atlas-crosswalk-20261101/track1-ingest-1.
- Actor: agent:lane-ingest-tier1-atlas-crosswalk-20261101.
- Records by type: artifact 117, source 117, observation 117.
  Total 351. Every observation is type web.capture.
- Every one of the 351 records carries tags.lane =
  tier1-atlas-crosswalk-20261101. Checked in the pending file and
  again in the exported batch. Zero records lack the tag.
- Capture status tags: first-byte-capture 339 records (113 files),
  repeat-byte-capture 12 records (4 files).
- One bundle submission was used (add --input), not 117 single
  captures. One early submission failed on observed_at format
  (a parser cut the first year digit, and the plus-offset form
  was used). Both were fixed in the bundle builder. The fixed
  bundle was accepted. No partial batch was left behind.
- Export: exported only this batch. Pending is now 0.
  Exported dir: data/records/b50b4847b64045f59906e7facdfb4fb4/.
  Exported record count re-checked: 351, same split.
- Verify --blobs: ok True, verified True, corpus records 225,860
  (225,509 plus 351). My batch: 0 missing artifacts. All 117
  blob files exist locally with matching size.
- Corpus-wide missing artifacts: 1,737. Those are pre-existing
  and belong to other batches. None is mine.
- Blob paths for the coordinator are listed in BLOB_PATHS.txt
  in this dir. Add them with explicit pathspecs, plus the batch
  dir and this ingest dir. Do not use git add -A.
- This worker did not commit and did not push, per the brief.
  The ingest dir and the batch dir sit untracked on disk.

## Watch disposition

- Slot-0 rotation baseline: covered 53 of 53. The slot-0 triage
  says the baseline went from 114 to 167 targets with 53
  additions. Those additions are these 53 endpoints.
- Trajectory-domains exact llms rows: covered 49 of 53.
- Gap (4): agent-commons-algo, relay-russian-agent-board,
  swarmmemo, the-colony. Each has a row in trajectory-domains.md,
  but the row names a different surface (a thread URL, a root
  URL, a hashed entry, a root URL). No exact llms watch row
  exists for these 4. The coordinator or list owner should add
  the exact llms rows, or confirm the baseline alone is enough.
- No scanner was enabled or disabled by this worker.
- No disabled scanner was touched. No other worker file was
  touched. Sibling files under raw/atlas, raw/crosswalk,
  raw/cryptologist, and raw/linguist were not read for content
  and were not changed.
