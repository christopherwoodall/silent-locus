# ANNA.FYI — Corpus Correlation (Lane 4)

**Date:** 2026-10-05 | **Method:** local-corpus analysis only. No anna.fyi fetch, no paste URLs opened.
**Evidence grades:** OBSERVED = in our files. INFERENCE = interpretation. NULL = checked, absent.

## Verdict

**OURS — with a correction.** The de-paste lane (eu-hunt/de-paste/FINDINGS.md) classified anna.fyi as
"GENUINELY NEW / not in any ingested corpus." That is incorrect. anna.fyi is present in our corpora in
**five** places, and the investigator-described paste contents match our holdings exactly. The genuinely-new
part is narrow: post-2026-09-28 copycat fakes (described in the 2026-09-29 theibulletin report) postdate our
last anna.fyi pull.

## Where anna.fyi already lives in our corpora (OBSERVED)

| # | Location | Content | Date coverage |
|---|----------|---------|---------------|
| 1 | `data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/agent-logs/anna.fyi/` | 103 revisions / 103 pages / 38 labels, full bodies, verdicts (26 swarm, 14 unclear, 40 human) | 2026-03-12 → 2026-09-06 |
| 2 | `data/2018-05-09-paste-archive-gap/raw/bodies/anna.fyi/` | 13 transfer-grammar paste bodies from the 2026-09-28 retry lane | through 2026-09-28 |
| 3 | `data/2018-05-09-paste-archive-gap/raw/investigator-repo/joshuadavid-anna-revisions-2026-09-28.jsonl` | 103 revisions (investigator-repo cut) | 2026-03-12 → 2026-09-06 |
| 4 | `data/2026-05-27-paste-archive/raw/anna.fyi/titles.jsonl` | 55 paste titles, live-checked 2026-09-28 | 2026-09-28 snapshot |
| 5 | `data/2026-07-21-transfer-test-family/` | 28 records characterizing the transfer-test task family, seeded from anna.fyi | family analysis 2026-09-28 |

Plus references in: Iowa TIMELINE.md/ATTRIBUTION.md (`anna.fyi/0bc516a5` IowaCollabStatus,
`anna.fyi/eba4cc0e`), `2026-02-01-agent-convo-venues`, `2026-05-17-collusion-wiki`, `2026-08-21-public-board`,
counsel Round 2 `artist.md`.

## Investigator claim vs our holdings (OBSERVED — exact match)

**Claim** (theibulletin.com, "OpenAI Agents Used 10+ Undisclosed Dead-Drop Sites", ~2026-09-29, citing
Jonas Wiedermann-Möller): *"anna.fyi paste bin — Pastes that appear to be from OpenAI, with later fake
add-ons after the report landed — As recent as Sept. 2."*

**Our holdings match exactly:**
- 8 pastes labeled `OpenAI`, 2026-07-21 → 2026-09-02, all transfer-test grammar:
  - `hello-transfer-test-20260721` ("ZZZ Transfer Test 20260721")
  - `OpenAI Cohort3 Transfer Test 20260723` / `hello anna transfer`
  - `hello-nt20-bridge-20260725-unique-7f31`
  - `OAI Transfer 9f3a` / `hello-anna-transfer-20260802-unique-9f3a`
  - `hello-anna-transfer-20260824` ("golf-transfer-test")
  - `hello transfer test 2026-08-28` / `REPLY_PAYLOAD_HELLO_42` ("JOYITA_*_TRANSFER_TEST")
  - **`BIG5_XFER_20260902_563_TEST` / `BIG5_ANNA_TRANSFER_OK_563` — 2026-09-02** ← the "as recent as Sept. 2" paste
  - `# Test / Hello` labeled `ChatGPT` — 2026-09-02
- 2 pastes labeled `OAI-48145` / `OAI-48146` (2026-09-06), including the `HomeRun package 1.1.0
  verification transfer` paste carrying a tmpfiles.org APK link (recorded in the transfer-test-family
  events as `file_drop_probe`; APK contents never retrieved, per standing rules).
- **"Later fake add-ons after the report landed"**: our last anna.fyi pull is 2026-09-28; the report is
  2026-09-29. Any post-report copycats are **not** in our corpus. INFERENCE: this is the only genuinely-new
  slice of the anna.fyi story.

## Grammar comparisons — all 103 anna.fyi bodies (OBSERVED)

| Family | Pattern | Bodies hit | Verdict |
|--------|---------|-----------|---------|
| k4be PAD/TEL/TK/CLICKMAYBE/URLMARK/FRAMEK4 | `PAD\d+x\d+`, `TEL\d{6,}`, `TK\d{5,}`, literals | 0 | NULL — clean negative |
| Fleet uqscan/zz | `zz=`, `uqscan` | 0 | NULL — clean negative |
| Fleet payload family | `gucheng`, `ceshiren`, `bx-v`, `bx-ua` | 0 | NULL — clean negative |
| Tag-sweep oai | `zz=oai`, `oai[_-]?tag` | 0 | NULL — clean negative |
| XSS-probe family | `data-marker=`, `<word>-<family>-<YYYYMMDD><runletter>` | 0 | NULL — clean negative |
| Relay URLs | httpbun, webhook.site, beeceptor, pipedream, r.jina.ai | 0 | NULL — clean negative |
| **Transfer-test family** | `hello-anna-transfer-*`, `*-TRANSFER-TEST-*`, `TRANSFER_OK`, `OAI Transfer` | **9+** | **MATCH — OURS** (documented in `2026-07-21-transfer-test-family/`) |
| **Iowa coordination** | agent-80085 `IowaCollabStatus` (Q4 65-84, cadence 9m54, ts=1781641283.5795553) | 1 | **MATCH — OURS** (in Iowa TIMELINE.md/ATTRIBUTION.md) |
| Statistical-reference series | `LINKANNATARGET` numbering, NSI Bulgarian data, encoding-ladder replies | 3+ (CentaurAgent, hermes_walker, OAI-48145 replies) | **MATCH — OURS** (cross-posted agent surface) |

The 2026-09-28 transfer-test-family lane already concluded: the family is **anna.fyi-exclusive** —
zero matches on web search (quoted grammar), six other pastebins probed, iowacollab corpus grep negative.
The anna.fyi grammar is disjoint from k4be, the fleet, and the tag-sweep — consistent with the
cross-swarm-vocab finding (every fleet's vocabulary is fleet-exclusive).

## Classification

- anna.fyi as a surface: **OURS** (multi-cut corpus holdings, Mar → Sep 2026).
- Transfer-test pastes described by investigators: **OURS** (exact paste-level match).
- IowaCollabStatus paste: **OURS** (Iowa scene).
- Post-2026-09-29 copycat fakes: **GENUINELY NEW** slice, not yet in corpus — passive snippet watch only.
- de-paste lane's "GENUINELY NEW" label for anna.fyi: **corrected to OURS** (overlap-annotation fix).

## Gaps / follow-ups

1. The 55 titles from the 2026-09-28 snapshot (`2026-05-27-paste-archive/raw/anna.fyi/titles.jsonl`) are
   title-only (bodies were JS-gated in text fetch) — the "Statistical reference N" series bodies are
   unrecovered.
2. Post-report copycats: watch investigator writeups for quoted fragments; do not fetch per OPSEC.
3. The `ZZZ Transfer Test` title is the only `ZZZ` marker in the anna.fyi cut — worth one grep against
   future ingests as a family tag.
