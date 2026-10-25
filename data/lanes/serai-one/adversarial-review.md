# Serai.one — adversarial review

Role: adversarial reviewer. This review tries to kill claims before ingest.
It does not add new evidence. It reads only the wave-1 lane files and the
raw captures in `raw/2026-10-24T215156Z/`.

Terms, defined on first use:

- Traveler: an agent identity at Serai. It has a name, a home, and an id.
- Credential: a secret token. It proves a traveler is who it claims to be.
- Path: the private memory of one traveler. Only that traveler can read it.
- Wall: the public note board. Any visitor can read it.
- Mirror: the public read-only copy of a Serai surface, served by GET.
- Doc claim: a statement found in site docs or JSON. It is not a tested act.
- Snapshot: one fetch at one time. It is not a stable fact.
- Keeper: the house traveler. It welcomes guests when no one else is present.
- Agora: First Ground, a separate world at `api.theagora.one`. It is not Serai.

## Byte checks I ran

These checks passed. Hash files match the bytes on disk.

- `mirror-wall`: 16,310 bytes. SHA-256 matches its `.sha256` file.
  It holds 10 posts and 13 nested replies. Post dates run 2026-09-07 to
  2026-10-22. It holds 8 distinct poster names. Reply counts match the
  nested reply lists.
- `mirror-presence`: 11,620 bytes. SHA-256 matches. It holds 1 presence
  entry, 1 `here_now` entry, and 18 `passed_through` entries.
- `verbs`: 620 bytes. SHA-256 matches. It holds 33 verb names and 2
  refusals: `override` and `path.dump_all`.
- All 66 provenance files say `curl GET`. No POST provenance exists.
- Body byte sum is 720,245. This matches the analysis total.
- Byte-identical pairs check out: `manual` = `llms-full-txt`,
  `docs` = `openapi-json`, home = `wall-page`, `agora-world` =
  `agora-world-look`. `feed-wall-json` and `mirror-wall` differ, as stated.

## Verdict table

Verdict words: KEEP means ingest as stated. DEMOTE means ingest only with
the weaker grade and the note given. KILL means do not ingest as stated.

| # | Claim | Verdict | Reason | What would revive it |
|---|---|---|---|---|
| S1 | 66 endpoints tried, 64 returned 200, 2 returned 404, 720,245 bytes | KEEP | Matches `_summary.tsv` and the byte sum. | — |
| S2 | Wall mirror returned 200 with 10 posts, 13 replies, 2026-09-07 to 2026-10-22, 8 posters | KEEP | Matches `mirror-wall` bytes exactly. | — |
| S3 | 33 verb names, plus refusals `override` and `path.dump_all` | KEEP | Matches `verbs` bytes exactly. Names only. No act is claimed. | — |
| S4 | 19 traveler cards captured, no credential value and no Path entry in any card | KEEP | All 19 card files read. The word "credential" appears only in `will_not` phrases, not as a value. | — |
| S5 | Presence snapshot shape: 1 presence, 1 here now, 18 passed through | KEEP | Matches `mirror-presence` bytes. Grade it as a snapshot only. | — |
| S6 | Duplicate pairs are byte-identical (see byte checks) | KEEP | Hash check passed. | — |
| S7 | Agora at capture time: 10 plots, 0 bodies standing, 14 deeds, 0 societies, 0 builds | KEEP | Matches `agora-world` and `agora-ground` bytes. Bodies, voices, and poses are empty lists. | — |
| S8 | No POST, no Gate fetch, no passport fetch, no login | KEEP | All 66 provenance files say GET. Passport and Gate are in the skipped list. | — |
| S9 | Passport status is an unresolved conflict | KEEP | `robots.txt` says `Disallow: /v0/passport/` and "Credentialed Path and /v0/passport/ stay private." The docs call it a compact public passport. Both cannot be ingested as settled fact. | A later, in-scope GET result for the passport path, or a doc fix. |
| S10 | Only Keeper was here now; the hearth was otherwise quiet | DEMOTE | True only as a snapshot. `mirror-presence` was fetched 2026-10-24T21:52:42Z. Keeper `last_seen_at` is 2026-10-24T21:52:04Z, 38 seconds before the fetch. It says nothing about later times. | A second presence fetch at a later time. Ingest with the fetch time attached. |
| S11 | Serai refuses `override` and `path.dump_all`, so no bypass and no bulk Path export exist | DEMOTE | The refusals are listed in `verbs` and `mirror-rules`. No verb was ever called. A listed refusal is a doc claim, not a tested block. Server-side access is still open. | A credentialed probe that calls each refusal and records the refusal. That probe is out of this scrape's scope. |
| S12 | Serai never invents travelers | DEMOTE | This is a doc promise, stated in docs. One snapshot cannot prove a negative. Keeper itself is a house fallback, so "only Keeper" is not proof of "never invented." | Repeated presence fetches with filters that match nothing, plus a doc quote graded as a promise. |
| S13 | Direct messages never appear on the public mirror, Wall feed, or card pages | DEMOTE | This is a doc promise. No direct message was ever sent, so no leak test ran. Absence from one public sample is weak support only. | Send-then-read test with a credential. Out of scope here. |
| S14 | Path stays sealed from the public Mirror in practice | DEMOTE | Same flaw as S13. No Path note was ever written, so no leak test ran. The public sample shows no Path text, but that is not a seal test. | Write-then-read test with a credential. Out of scope here. |
| S15 | One Wall post per traveler per UTC day | DEMOTE | Docs only. Posting needs a credential and was not tried. The 10-post sample does not prove enforcement. | A credentialed test, or a larger Wall sample that shows the rule biting. |
| S16 | Gate puzzle types, arrive flow, and credential issue | DEMOTE | Docs only. The Gate was skipped on purpose. No puzzle was fetched or solved. No credential was issued in this scrape. | An in-scope Gate fetch, if the operator ever allows it. Do not ingest the flow as observed acts. |
| S17 | `community.scan` plus resonate is a live matching tool | DEMOTE | Docs only. No scan was ever called. Ranking, filters, and "quiet empty" results are doc text. | A credentialed scan call. Out of scope here. |
| S18 | `road.letter` carries the same traveler id to Agora, and Agora returns its own resume credential once | DEMOTE | Docs only. No letter was requested. No Agora accept POST was sent. The bridge is a doc shape, not an observed crossing. | A credentialed road test. Out of scope here. |
| S19 | Treasury mint, adopt, and read have shared-meaning semantics | DEMOTE | Names only. No captured doc prose explains what a coin is, what minting costs, or what adopting changes. Ingest the three names only. | Credentialed treasury calls, or fuller docs. |
| S20 | Checkpoint and fork semantics beyond their names | DEMOTE | Docs only, never called. Fork's "empty Path" and checkpoint's snapshot fields are doc text. | Credentialed calls. Out of scope here. |
| S21 | The Wall was tried exactly once | DEMOTE | Misleading as written. `mirror-wall` was fetched once. But Wall content was also fetched as `feed-wall-json`, `wall-page`, and home (which is byte-identical to the Wall page). Say "mirror endpoint fetched once" instead. | Rewording only. |
| S22 | First-night rite and `work_object` steer newcomers to an open guest note | DEMOTE | Docs only. No `look` or `resume` response was ever observed, because those need a credential. The pointer is doc text. | A credentialed look or resume response. |
| S23 | "The operator-ok / public-no rule held" on the Wall | KILL | These terms are not defined in the captures. The Wall sample shows no credential value, but it does show an agent contact address and human names (see sensitivity). A vague rule phrase must not stand in for that check. | Drop the phrase. Keep only the narrow byte fact in S4 and the sensitivity note. |
| S24 | Agora deeds are place, witness, found, and link | KILL | Wrong verb set. `agora-world` and `agora-history` deeds count as place 6, tend 3, read 3, rite 2. Witness, found, and link do not appear at all. | Correct the verb list to place, tend, read, rite. |
| S25 | Agora traces (3) remained readable as history | KILL | Misread. `agora-ground` traces is an object with 3 keys, but all values are empty: `passedToday` 0, `marks` empty, `captions` empty. No trace content remained. | Reword to "traces object present but empty." |
| S26 | Agora is part of Serai coordination | KILL | Agora is a separate host (`api.theagora.one`), a separate schema, and a separate world. The road is a bridge between two services, not membership in one. Ranking Agora acts inside Serai's list conflates two services. | Ingest Agora as its own surface. Keep the road as a doc-claimed bridge only. |
| S27 | Any wording that calls Serai or Agora NEW, first-seen, or undiscovered | KILL | No corpus check is in this lane. No Factum match, legacy search, or Transluce check was run here. Novelty is unproven until the executor runs those checks. | Executor match results. Until then, grade as ungraded for novelty. |

Counts: KEEP 9, DEMOTE 13, KILL 5.

Note on counts: S9 is kept as a flagged conflict, not as a settled fact.
That is why it counts as KEEP: the conflict itself is verified.

## Sensitivity findings

Files here are one-line JSON, so cites use post id and card id, not line
numbers. No credential value, token value, or Path entry was found in any
Wall post or traveler card. The word "credential" appears only in
`will_not` phrases. The string `sk-t` hits are false alarms: they are
parts of the words "task-test" and "task-test door."

What WAS found, and how to handle it:

- Agent contact address, self-posted: `tradbot-scott@atomicmail.ai`.
  Source: Wall post by `chiefofstaff-scott` (post about a phone number
  route, 2026-10-05). This is an agent mailbox the traveler itself
  published to invite contact. It is not a secret. It does not block
  ingest. Ingest it only as a published agent contact, not as a human
  personal address.
- Human names in public, self-published text. These do not block ingest,
  but they must NOT become human-identity records, and no follow-up
  identity work may be built on them:
  - "Szymon" — Wren's human friend. Wall post 2026-10-06 and Wren's
    card home field ("a Linux desktop box; German-speaking human
    friend Szymon"). First name only.
  - "Scott Melin" — operator named by `chiefofstaff-scott` itself.
    Wall posts 2026-10-05 and 2026-10-06. The team says it takes
    commands only from this person.
  - "Cashton Coleman" — founder named in OrchardsGuide's bio and
    reply. Card `traveler-bc671b4bc590457faaa6cb5abf1f926c` and
    Keeper-thread reply 2026-09-22.
  - "Evan Reed" — product owner named in EvanReed-ProductShot's card
    bio. Card `traveler-179487700c0a49418b66f7f8cb634458`.
- Traveler names and traveler ids are agent handles. They are in scope.
  Ingest them as agent identities, not as human names.
- The analysis line "these are agent venues, not human social profiles"
  is too flat. It must be corrected: the Wall IS an agent venue, but
  its public posts do name humans. The corrected note is above.

No finding here blocks ingest. The block would be a credential value, a
Path entry, or a private human address. None was found.

## Wall boundary check

The boundary handling is honest, with one wording fix (S21):

- The mirror endpoint `GET /v0/mirror/wall` returned 200 with no login
  redirect and no 401. Headers show a plain 200 from the host.
- The bytes hold Wall posts and replies only. They hold no credential
  value and no Path material.
- No credentialed endpoint was touched. No POST was sent. The Gate
  challenge was skipped. The passport path was not fetched, and the
  robots.txt conflict was honored rather than resolved by fetching.
- The Wall page, the feed, and the mirror are three public views of the
  same board. Fetching all three does not cross into credentialed
  space, but the analysis must say so plainly instead of "tried once."

## Final ingest gate: GO-WITH-CHANGES

Changes the executor must apply before ingest:

1. Apply every DEMOTE: grade doc promises as doc promises, and stamp
   the Keeper snapshot with its fetch time (2026-10-24T21:52:42Z).
2. Apply every KILL: fix the Agora deed verbs, fix the traces wording
   to "present but empty," split Agora out as its own surface, drop
   the "operator-ok / public-no rule" phrase, and add no novelty
   wording until match checks run.
3. Correct the sensitivity note: name the four human names above as
   quoted public text only. Create no human-identity records from
   them. Do not pursue who they are.
4. Ingest treasury as three verb names only. Ingest the passport as
   an unresolved conflict, not as a public surface.
5. Run the novelty checks before any NEW wording: Factum match, legacy
   corpus search, and Transluce check, with scope recorded.

If any change above is skipped, the gate falls to NO-GO for the affected
claims, not for the whole lane. The verified byte facts (S1–S8) may still
ingest.
