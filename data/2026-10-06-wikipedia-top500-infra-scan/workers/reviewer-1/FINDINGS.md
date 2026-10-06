# REVIEWER-1 (attribution red-team) — FINDINGS

Event: `data/2026-10-06-wikipedia-top500-infra-scan/`
Branch: `wikipedia-top500-infra-scan-2026-10-06` (no branch switch, no commit, no push — coordinator's job)
Date: 2026-10-06
Reviewer mandate: kill-or-fix authority over the matcher's 90 attributions.

**Headline verdict: 0 of 90 survive. The entire match set is a temporal artifact.**
Every one of the 90 "matches" rests on a provider-published CIDR that entered the
provider's published range feed **1–6 years AFTER the Wikipedia edit it is matched
to**. Against contemporaneous (edit-date) range data, not a single matched IP is
inside any AWS or Azure published range. Corrected match count: **0**.

## Input-path discrepancy (noted, not fatal)

The task brief pointed at `workers/matcher/FINDINGS.md`; the matcher actually wrote
its findings to `data/2026-10-06-wikipedia-top500-infra-scan/workers/matcher/FINDINGS.md`
(path hard-coded in `matcher.py`: `BASE/workers/matcher/FINDINGS.md` where
`BASE=data/2026-10-06-wikipedia-top500-infra-scan`). Findings were read from the
actual location. Content reviewed: method (bisect, longest-prefix-first,
exact-duplicate recording), volume (489 files, 677,635 revisions, 61,179 IP-editor
revisions, 90 matched), provider split (aws 62, azure 28), and the opening caveat
("A datacenter-IP match is NOT proof of AI-agent use" — correct and retained).

## CHECK 1 — mechanical IP-in-CIDR verification (random sample of 20)

PASS: 20/20. I independently recomputed longest-prefix match for each sampled IP
straight from `raw/cidr-provider-map.jsonl` using Python `ipaddress` (not trusting
the matcher's cache). Membership correct, provider/service sets exactly equal
(`aws`/`AMAZON`, `azure`/`AzureCloud.<region>`) in all 20. The matcher's lookup
mechanics are sound — the failure is elsewhere (currency).

Sample detail (IP → longest-prefix CIDR): 7x `88.108.0.0/14`, 2x `88.104.0.0/15`,
3x `99.200.0.0/13`, 1x `72.242.0.0/15`, 2x `86.112.0.0/15`, 1x `85.211.128.0/17`
(azure/malaysiawest), 2x `172.195.0.0/16` (azure/mexicocentral),
1x `172.197.0.0/17` (azure/malaysiasouth), 1x `85.211.0.0/17` (azure/malaysiasouth),
1x `85.210.0.0/16` (azure/uksouth).

## CHECK 2 — CIDR provenance audit (the `88.108.0.0/14` flag and all 62 AWS matches)

**The "ISP-shaped, not AWS-shaped" flag is rejected as a data-integrity concern.**
I re-fetched the official feed live (`curl https://ip-ranges.amazonaws.com/ip-ranges.json`,
createDate 2026-10-06-19-17-04) and compared prefix-by-prefix with the range-curator's
cached copy (createDate 2026-10-06-17-57-06): every flagged prefix verifies present in
the official live feed.

All 90 matches rest on 15 distinct CIDRs; provenance for each:

| CIDR | provider | service | in live official feed 2026-10-06? |
|---|---|---|---|
| 88.108.0.0/14 | aws | AMAZON (ap-south-1) | YES (verified live) |
| 88.104.0.0/15 | aws | AMAZON (sa-east-1) | YES |
| 88.106.0.0/15 | aws | AMAZON (sa-east-1) | YES |
| 86.112.0.0/15 | aws | AMAZON+EC2 (eu-north-1) | YES |
| 99.200.0.0/13 | aws | AMAZON+EC2 (eu-central-1) | YES |
| 72.242.0.0/15 | aws | AMAZON (ap-east-2) | YES |
| 182.30.0.0/16 | aws | AMAZON | YES |
| 172.197.0.0/17 | azure | AzureCloud.malaysiasouth | YES (20261005 file, changeNumber 421) |
| 172.197.128.0/17 | azure | AzureCloud.malaysiawest | YES |
| 172.195.0.0/16 | azure | AzureCloud.mexicocentral | YES |
| 172.193.0.0/17 | azure | AzureCloud.eastus2 | YES |
| 172.193.128.0/17 | azure | AzureCloud.westus2 | YES |
| 85.211.0.0/17 | azure | AzureCloud.malaysiasouth | YES |
| 85.211.128.0/17 | azure | AzureCloud.malaysiawest | YES |
| 85.210.0.0/16 | azure | AzureCloud.uksouth | YES |

**Zero matches rest on a dubious/unofficial prefix.** The matcher was right to note
the shape is ISP-like, but the OBSERVED fact is: AWS officially publishes these
leased legacy-carrier blocks. INFERENCE (not a kill of the row): "AWS-published
range" ≠ "datacenter" as cleanly as assumed — these are consumer-ISP-shaped blocks
(e.g. 88.x/86.x RIPE space) that AWS only recently added to its feed (see Check 3).
The range-curator's caveat #2 ("a datacenter IP is NOT proof of AI-agent use") should
be strengthened: provider feeds now contain leased consumer-ISP space, so even the
"datacenter IP" gloss is weaker than stated for these particular prefixes.

## CHECK 3 — range currency (the kill)

The map is a 2026-10-06 snapshot; **all 90 matched edits date 2020-01-16 → 2023-09-14**
(by year: 2020: 36, 2021: 22, 2022: 17, 2023: 15). I pulled historical provider feeds
from the Wayback Machine (port 80, per TOOLS.md; intermittent 504s, retried with
45–90s spacing; all files cached in `raw/history/` with `PROVENANCE.md` +
`SHA256SUMS.txt`).

### AWS: first-appearance bracketing of the 7 CIDRs

Snapshots (all createDate from payload): 2020-03-13, 2021-01-04, 2022-01-05,
2023-01-18, 2023-08-31, 2023-12-07, 2024-06-01, 2025-01-15, 2025-06-04, 2026-01-08.

| CIDR | first seen in AWS feed | matched edits it carries | verdict |
|---|---|---|---|
| 86.112.0.0/15 | between 2026-01-08 and 2026-10-06 | 10 (2020-01→2023-04) | KILL |
| 99.200.0.0/13 | between 2025-01-15 and 2025-06-04 | 9 (2020-01→2020-09) | KILL |
| 88.108.0.0/14 | between 2024-06-01 and 2025-01-15 | 26 (2020-09→2023-09) | KILL |
| 88.104.0.0/15 | between 2025-01-15 and 2025-06-04 | 11 (2020-10→2021-11) | KILL |
| 88.106.0.0/15 | between 2025-01-15 and 2025-06-04 | 4 (2021-03→2022-03) | KILL |
| 72.242.0.0/15 | between 2025-01-15 and 2025-06-04 | 1 (2022-09-18) | KILL |
| 182.30.0.0/16 | between 2023-01-18 and 2023-08-31 | 1 (2020-06-04) | KILL |

### Azure: first-appearance bracketing of the 8 CIDRs

Snapshots (weekly files, changeNumber from payload): 2020-03-12 (ch.100),
2021-01-04 (ch.128), 2022-12-05 (ch.231), 2023-04-17 (ch.250), 2024-05-27 (ch.308),
2025-07-14 (ch.362), 2025-10-06 (ch.372), 2026-01-05 (ch.383), 2026-04-06 (ch.394).
Note: once a CIDR appears it stays present in every later snapshot (monotone),
so bracketing is valid.

| CIDR | first seen in ServiceTags | matched edits it carries | verdict |
|---|---|---|---|
| 172.197.0.0/17 | between 2024-05-27 and 2025-07-14 | 9 (2020-07→2023-01) | KILL |
| 85.211.0.0/17 | between 2023-04-17 and 2024-05-27 | 4 (2021-09-04, all one day) | KILL |
| 172.195.0.0/16 | between 2026-04-06 and 2026-10-05 | 4 (2021-09→2022-09) | KILL |
| 85.210.0.0/16 | between 2024-05-27 and 2025-07-14 | 4 (2020-04→2022-04) | KILL |
| 172.193.0.0/17 | between 2024-05-27 and 2025-07-14 | 3 (2021-07-14, all one day) | KILL |
| 172.197.128.0/17 | between 2026-01-05 and 2026-04-06 | 2 (2020-08→2023-01) | KILL |
| 85.211.128.0/17 | between 2025-07-14 and 2025-10-06 | 1 (2022-10-28) | KILL |
| 172.193.128.0/17 | between 2024-05-27 and 2025-07-14 | 1 (2021-02-23) | KILL |

### Oldest-10 edits (as required by the brief)

All 10 die on currency:

| edit date | IP | CIDR | CIDR in provider feed at edit date? |
|---|---|---|---|
| 2020-01-16 | 86.113.108.154 | 86.112.0.0/15 (aws) | NO — added ~2026 |
| 2020-01-20 | 99.203.28.149 | 99.200.0.0/13 (aws) | NO — added 2025 |
| 2020-01-20 | 99.203.41.200 | 99.200.0.0/13 (aws) | NO |
| 2020-01-26 | 99.203.42.86 | 99.200.0.0/13 (aws) | NO |
| 2020-01-27 | 86.113.108.154 | 86.112.0.0/15 (aws) | NO |
| 2020-02-03 | 99.203.5.99 | 99.200.0.0/13 (aws) | NO |
| 2020-02-10 | 86.113.230.201 | 86.112.0.0/15 (aws) | NO |
| 2020-02-20 | 99.203.22.224 | 99.200.0.0/13 (aws) | NO |
| 2020-04-11 | 85.210.124.177 | 85.210.0.0/16 (azure) | NO — added 2024–2025 |
| 2020-06-04 | 182.30.100.96 | 182.30.0.0/16 (aws) | NO — added Jan–Aug 2023 |

### Stronger form (per-IP, any range)

Even granting re-numbering (the right CIDR, wrong string): I checked every one of
the 67 distinct matched IPs against the *entire* provider feed at each edit-era
snapshot. Result: **0/49 AWS-attributed IPs in any AWS range (2020, 2021, 2022,
2023 snapshots); 0/18 Azure-attributed IPs in any Azure range (2020-03, 2021-01,
2022-12, 2023-04 weekly files).** At the time these edits were made, none of these
IPs was in any published range of the attributed provider. The newest azure edit
(2023-01-28) predates the 2023-04-17 snapshot (all absent); the newest AWS edit
(2023-09-14) predates the 2023-12-07 snapshot (all absent). No back-datable
attribution survives.

Methodological note for the manual: AWS's feed grew from 2,061 prefixes (2020-03)
to 7,022 (2023-01) to ~10,560 (2026-10) — the 2024–2026 growth is largely leased
legacy-carrier blocks (88.x/86.x/99.x/72.x). Matching old edits against a current
feed is a guaranteed false-positive machine on precisely this class of range.

## CHECK 4 — any positive signal of AI-agent activity beyond "datacenter IP"?

**None observed — and the observed metadata is actively human-shaped.**

- Provider split: 62 aws/AMAZON + 28 azure/AzureCloud; **zero matches on any
  openai/anthropic/perplexity published bot range** across 677,635 revisions.
- Tags (90 records): `mobile edit` 51, `mobile web edit` 47, `mw-reverted` 35,
  `wikieditor` 14, `visualeditor` 8, `mobile app edit` 4, `ios app edit` 3,
  `android app edit` 1, `canned edit summary` 2, `possible birth date change` 2,
  `possible unreferenced addition to BLP` 3, `possible libel or vandalism` 1.
  This is the tag profile of interactive phone/web editing, not of automation —
  there are no OAuth/AWB/Huggle/bot tags anywhere in the set.
- Comments: 41/90 empty; the rest are natural-language human summaries —
  "wording", "per article", "Fixed typo", "Corrected syntax",
  "interview by reliably-identifiable Sky journalist cited", and one joke edit
  ("/* Story */Fixed the fact that they aren't zombies, you uncultered swime").
  35/90 are `mw-reverted` (drive-by/vandalism-grade edits getting reverted).
- No nonce/tag grammars, no burst cadence beyond single-day human edit clusters
  (12/67 IPs edited more than once; all multi-edit clusters are same-day or a
  few weeks apart — consistent with a person on a sticky IP).

Per the brief: the finding for these records must be reported as
**"datacenter-IP edits, unattributed to any AI system"** — and with Check 3, even
the "datacenter-IP" part cannot be back-dated: at edit time these were not in any
published range of the attributed provider. Any language suggesting AI attribution
is killed. No such language exists in the matcher's own FINDINGS.md (its caveat is
correct), but any coordinator summary built on these 90 records must not carry
attribution language.

## Killed / kept

- KILLED: all 90 records (all 62 aws, all 28 azure) — reason: range currency.
  Every match's CIDR entered the provider's published feed 1–6 years after the
  edit; contemporaneous feeds show zero of the 67 distinct IPs in any published
  range of the attributed provider. Not one survives even in the generous
  per-IP/any-range form.
- KEPT: none.
- FIXED (not killed): the `88.108.0.0/14` "ISP-shaped, not AWS-shaped" flag —
  rejected as a data-integrity concern; the prefix is genuinely present in the
  live official AWS feed (verified 2026-10-06). Downgraded to an interpretive
  caveat: provider-published feeds now include leased consumer-ISP-shaped space,
  so the "datacenter IP" gloss needs weakening for these prefixes.
- FIXED (wording): matcher mechanics verified sound (Check 1, 20/20); no code
  fix needed. What needs fixing is the scan design: **matching historical edits
  against a current range snapshot without period-appropriate feeds produces
  100% false positives here.** Any re-run must use feeds contemporaneous with
  the edit dates (or drop non-contemporaneous matches).

## Corrected count

**0 of 90 survive. Usable match count: 0.**

## Evidence cached

`raw/history/` (19 files, ~42 MB): 10 AWS ip-ranges.json snapshots
(2020-03→2026-01) + 9 Azure ServiceTags weekly files (2020-03→2026-04),
`PROVENANCE.md` (source URL, wayback timestamp, retrieval method, payload
createDate/changeNumber per file), `SHA256SUMS.txt`.

**DO NOT COMMIT/PUSH** — coordinator handles git.
