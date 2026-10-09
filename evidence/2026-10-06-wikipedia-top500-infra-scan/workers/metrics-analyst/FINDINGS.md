# Metrics analyst findings — Wikipedia top-500 infra scan (2026-10-06)

Worker: metrics-analyst. Inputs:
`raw/ip-matches.jsonl` (90 records), `raw/article-aggregates.tsv`, `raw/top500-articles.tsv`.
Computed with python3 stdlib (local); API checks via curl only. Timestamps are UTC as
returned by the MediaWiki API.

## 1. Per-provider metrics table

| Provider | Edits | Distinct articles | Distinct IPs | First edit | Last edit | Azure region split |
|---|---|---|---|---|---|---|
| aws | 62 | 40 | 49 | 2020-01-16T18:12:26Z | 2023-09-14T16:40:27Z | service tag: AMAZON (all 62) |
| azure | 28 | 16 | 18 | 2020-04-11T01:24:01Z | 2023-01-28T02:48:43Z | malaysiasouth 13, mexicocentral 4, uksouth 4, malaysiawest 3, eastus2 3, westus2 1 |

No AI-lab ranges matched: providers set across all 90 records is exactly {aws, azure}.
No GCP, no bot ranges, no named AI-lab CIDRs.

### Articles touched (rank / title / edits)

AWS (40 articles): #4 Lizzie Borden x1 · #10 Elizabeth Holmes x2 · #35 Dolly Parton x2 ·
#66 Kaya Scodelario x1 · #68 Charlie Kirk x1 · #78 Cindy Crawford x2 · #79 Matthew Rhys x1 ·
#87 Slow Horses x2 · #149 Tom Bateman (actor) x2 · #168 Nicole Kidman x3 ·
#177 Andy Burnham x1 · #196 Charles Spencer, 9th Earl Spencer x1 · #200 Resident Evil x1 ·
#209 American Horror Story x1 · #210 Elizabeth Báthory x1 · #217 Anne Hathaway x1 ·
#227 Nigella Lawson x4 · #230 Coco Gauff x1 · #237 Anthony Bourdain x2 · #252 Robert Pattinson x1 ·
#256 Zoe Saldaña x1 · #259 Bayeux Tapestry x3 · #265 Pink (singer) x1 · #266 Michael J. Fox x1 ·
#285 Richard O'Sullivan x1 · #293 I, Robot (film) x1 · #294 Andrew Garfield x1 · #305 Florence Pugh x7 ·
#317 UEFA Nations League x1 · #341 Clint Eastwood x1 · #344 Charles Harrelson x2 ·
#398 Jack Lowden x1 · #421 Joey King x2 · #436 Barbarian (2022 film) x1 · #445 Scooter Braun x1 ·
#453 Jon Bernthal x1 · #455 Jason Sudeikis x1 · #473 George VI x2 · #491 Joely Richardson x1

Azure (16 articles): #77 Ted Lasso x1 · #122 Kate Upton x4 · #160 Casualties of the September 11 attacks x1 ·
#168 Nicole Kidman x3 · #217 Anne Hathaway x1 · #226 Labor Day x1 · #227 Nigella Lawson x1 ·
#253 Gal Gadot x1 · #265 Pink (singer) x3 · #297 Dancing with the Stars (American TV series) x1 ·
#305 Florence Pugh x1 · #327 Wordle x1 · #334 Erling Haaland x5 · #461 Christopher Nolan x1 ·
#468 Heath Ledger x1 · #500 Sadie Sink x2

Overlap articles (both providers): Nicole Kidman (#168), Nigella Lawson (#227),
Anne Hathaway (#217), Pink (singer) (#265), Florence Pugh (#305).

### IP reuse

- AWS: 8 of 49 IPs made 2+ edits (max: 88.105.126.238 ×7, all Florence Pugh-adjacent/Nicole Kidman, Nov 2020).
- Azure: 4 of 18 IPs made 2+ edits (172.197.49.18 ×5 = all 5 Erling Haaland edits; 85.211.105.174 ×4 = all 4 Kate Upton edits).

### Timestamp distribution: spread, not burst

- AWS yearly: 2020: 27 · 2021: 12 · 2022: 10 · 2023: 13. Azure yearly: 2020: 9 · 2021: 10 · 2022: 7 · 2023: 2.
- Hits land in 38 distinct months; busiest months (2021-09, 2020-10, 2020-08) have 6 each.
- No campaign-shaped burst across the 90. **Within-article** bursts exist: 15 pairs of
  same-article edits ≤60 min apart — all by the SAME IP, minutes apart (e.g. Erling Haaland:
  5 edits in ~6 min on 2021-04-17; Kate Upton: 4 edits in ~9 min on 2021-09-04; Nicole Kidman:
  2 edits 2.3 min apart). This is interactive human editing (iterative saves), not a fleet volley.

### Edit-device signal (tags across all 90)

`mobile edit` 51 · `mobile web edit` 47 · `mw-reverted` 35 · `wikieditor` 14 · `visualeditor` 8 ·
`mobile app edit` 4 · `mw-manual-revert` 3 · `ios app edit` 3 · `possible unreferenced addition to BLP` 3 ·
`possible birth date change` 2 · `mw-undo` 1 · `references removed` 1 · `deprecated source` 1 ·
`possible libel or vandalism` 1 · `mw-rollback` 0. 41 of 90 edits have an empty edit summary.
Over half the edits were made from a mobile browser/app — a consumer-device signature.

### Caveat on provider attribution

The `providers[]` labels come from the scan's CIDR map (`raw/cidr-provider-map.jsonl`,
built from `aws-ip-ranges.json` / `azure-servicetags.json`). Many matched IPs sit in
ranges that look like consumer ISP space (88.x, 86.x, 85.x, 99.203.x /16s dominate the set).
Provider attribution is only as good as those range files; spot-checking the actual BGP/ASN
of a few of these /16s is recommended before treating "aws"/"azure" as ground truth.

## 2. Reverted-status analysis

### 2a. Tag-based (all 90 — OBSERVED, cheap, first pass)

Revision's own tags containing revert markers (`mw-reverted`, `mw-manual-revert`, `mw-rollback`):
- AWS: 23 of 62 carry a revert marker; 39 do not.
- Azure: 14 of 28 carry a revert marker; 14 do not.
- Combined: 37 of 90 (41.1%) have a revert marker on the revision itself.
- Note: `mw-manual-revert` means the edit *was itself a revert action* (anti-vandalism),
  not that it was undone — 3 such edits. `mw-reverted` (35 edits) means a later edit
  undid it. No `mw-rollback` tags at all.

### 2b. Sample survival check (15 edits — direct API verification, 2026-10-06 ~22:25–22:35Z)

Method (documented for reuse): for each sampled revid —
1. `action=query&prop=revisions&revids=<r>&rvprop=parentid|tags` → parent revid.
2. `action=compare&fromrev=<parent>&torev=<r>&prop=diff|ids|title` → added/deleted text.
3. `action=query&prop=revisions&titles=<article>&rvprop=content&rvslots=main` (single-title,
   no rvlimit — multi-title + rvlimit is rejected with `invalidparammix`) → current wikitext.
4. Grade CURRENT if the edit's substantive added text (or, for deletion edits, the removal)
   is present/absent accordingly in the current revision; REVERTED if the edit carries
   `mw-reverted` on its own record or its added text is gone; UNCERTAIN if neither
   condition is decisive (e.g. routine image churn over 5 years makes "absent" ambiguous).

Sample was stratified: 9 AWS + 6 Azure, 7 with revert markers, 8 without.

| revid | article | provider | own tags | verdict | basis |
|---|---|---|---|---|---|
| 1144265268 | Elizabeth Holmes | aws | mw-manual-revert, mw-reverted | **REVERTED** | own mw-reverted tag (a manual revert that was itself later undone) |
| 986516839 | Nicole Kidman | aws | mw-manual-revert | **UNCERTAIN** | a revert action, not itself revert-tagged; its distinctive markers (post-nominals template, biography.com ref) are absent from the current lead, but that is also consistent with 6 years of normal lead rewrites |
| 984548500 | Andy Burnham | aws | mobile, mw-reverted | **REVERTED** | own mw-reverted tag |
| 1013306200 | American Horror Story | aws | mobile, mw-reverted | **REVERTED** | own mw-reverted tag; vandalism ("\| name = wiki's fav show") |
| 1143875672 | Elizabeth Holmes | aws | (none) | **CURRENT** | wording tweak ("One of her paternal great-great-great-grandfathers was") survives verbatim in current text |
| 1148721951 | Tom Bateman (actor) | aws | (none) | **REVERTED** | added inews.co.uk citation is gone from current (citation swap by later editors, not a revert action) |
| 1148721238 | Tom Bateman (actor) | aws | deprecated source | **CURRENT** | its sentence ("music teacher father and primary-school teacher mother") survives; only the citation was later restored to GQ |
| 989070223 | Nicole Kidman | aws | possible birth date change | **CURRENT** | infobox birth year 1964→1967 correction still in current text |
| 989069886 | Nicole Kidman | aws | (none) | **REVERTED** | lead descriptor change ("Australian-American"→"Australian") did not survive — current reads "Australian and American" with a talk-page consensus note; superseded by normal editing, no revert tag |
| 1132318582 | Nicole Kidman | azure | mobile, mw-reverted | **REVERTED** | own mw-reverted tag ("born 20 June 1967 in Hawaii" gone) |
| 1118719522 | Nicole Kidman | azure | mobile, mw-reverted | **REVERTED** | own mw-reverted tag (descriptor change gone) |
| 997285420 | Nigella Lawson | azure | mobile, mw-reverted | **REVERTED** | own mw-reverted tag; vandalism ("Nigella is a coke head…") |
| 1042401405 | Kate Upton | azure | mobile | **UNCERTAIN** | added image file absent from current; 5 years of routine image churn — cannot distinguish revert from supersession |
| 1042401199 | Kate Upton | azure | mobile | **UNCERTAIN** | infobox image replaced by later routine edits; same ambiguity |
| 1042400369 | Kate Upton | azure | mobile | **CURRENT** | added G-Star 2014 section image still present in current text |

Sample tally: **CURRENT 4 / REVERTED 8 / UNCERTAIN 3**.

### Limits of this method (read before citing any number)

1. **Text-survival ≠ revert.** An edit's text disappearing from the current article can mean
   formal revert, later copy-editing, section rewrites, or image churn. Only the revision's
   own `mw-reverted`/`mw-rollback` tags assert "was undone". Case 989069886 proves the gap:
   no revert tag, but the substance was clearly superseded.
2. **6-year gap.** Sampled edits are 2020–2023; normal article evolution alone can erase
   exact strings. UNCERTAIN is the honest grade where markers are gone.
3. **Sample is not extrapolated.** These 15 say nothing statistically about the other 75.
   The only population-level statement supported is the tag-based 41.1% revert-marker rate.
4. Attribution caveat from §1 applies throughout.

## 3. Characterization of the edits

Content review (all 90 comments + 15 diffs read). Shape: **ordinary human IP editing —
BLP fiddling, celebrity trivia, typos, vandalism, anti-vandalism.** Nothing agent-shaped:
no nonce grammars, no enumeration order, no uniform cadence, no tool-like summaries
(41/90 summaries are empty; the rest are section headers or plain-English notes).

- **Vandalism (reverted):** 997285420 (Nigella Lawson, azure) — "Nigella is a coke head who
  pretends to be a house wife shame on her". Diff: https://en.wikipedia.org/w/index.php?diff=997285420
- **Vandalism (reverted):** 1013306200 (American Horror Story, aws) — infobox
  `| name = wiki's fav show`. Diff: https://en.wikipedia.org/w/index.php?diff=1013306200
- **Anti-vandalism (human patrolling):** 1129471979 (Dolly Parton, aws) — undo with summary
  "Reverted edits by [[Special:Contributions/160.0.205.97]] … I think they made mistake".
  Diff: https://en.wikipedia.org/w/index.php?diff=1129471979
- **Constructive BLP sourcing dispute:** 1148721238 (Tom Bateman (actor), aws) — replaced
  "working-class family" (GQ) with "music teacher father and primary-school teacher mother",
  citing WP perennial-source guidance on the Daily Mail. Substance survived (see §2b).
  Diff: https://en.wikipedia.org/w/index.php?diff=1148721238
- **Factual correction (survived):** 989070223 (Nicole Kidman, aws) — infobox birth year
  1964→1967. Diff: https://en.wikipedia.org/w/index.php?diff=989070223
- **Human color:** 936647529 (Resident Evil, aws) — "Fixed the fact that they aren't zombies,
  you uncultered swime" [sic]; 995387071 (Anthony Bourdain, aws) — "I changed celebrity chef
  to chef because if the man saw himself described as a tv celebrity chef he would turn in
  his grave"; 1061018059 (Jon Bernthal, aws) — "not established by source/ original research"
  with `references removed` tag (content-policy policing, not vandalism).
- One edit carries `possible libel or vandalism` + `possible unreferenced addition to BLP`
  (1033555576, Pink (singer), azure — reverted).

## 4. Headline denominators

Scan-wide totals (from `raw/article-aggregates.tsv`): 677,635 total revisions ·
61,179 IP-editor revisions (9.03%) · 21,922 temp-account revisions (3.24%) ·
594,534 named-account revisions (87.74%).

The 90 datacenter-IP matches as a fraction of each:
- of all revisions: 90 / 677,635 = **0.0133%**
- of IP-editor revisions: 90 / 61,179 = **0.147%**
- of temp-account revisions: 90 / 21,922 = **0.411%**
- of named-account revisions: 90 / 594,534 = **0.0151%**

In words: roughly one in 7,500 total revisions, and roughly one in 680 anonymous-IP
revisions, came from an IP in the scan's cloud ranges.

## 5. Central interpretive limit

**A datacenter-IP edit is not evidence of AI-agent activity.** Every one of these 90 edits
is individually consistent with a human on a VPN, a corporate egress, a cloud dev box, or
a mobile carrier route that happens to fall inside a published cloud range — and the
observed content (typos, BLP gossip, fan trivia, mobile-browser tags, iterative same-minute
saves, anti-vandalism patrolling) is the signature of ordinary human IP editors, not of
automated agents. Nothing in the metadata (no burst cadence, no nonce grammars, no
enumeration order, no uniform summaries) is agent-shaped. The honest finding: 90
cloud-range IP edits exist in the corpus (0.013% of revisions); attributing any of them
to AI agents would require positive evidence this scan does not provide.
