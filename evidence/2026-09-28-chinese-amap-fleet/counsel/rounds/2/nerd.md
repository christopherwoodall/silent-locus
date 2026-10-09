# NERD — Round 2 hunt findings (lanes 3–4: thecolony.ai / bullfincher.io / xz_knowledge)

*Role: data forensics. Chair: Hunter S. Thompson. Filed 2026-10-05.*
*Method: byte-level verification against `data/2026-10-05-thecolony-ai/` (20 events), the run-1 k4be export (`ref/run1/agent-logs/pastebin-k4be/revisions.jsonl`, 198 rows), lane files THECOLONY.md / BULLFINCHER.md / XZ_KNOWLEDGE.md, and Round 1 counsel records. Nothing fetched or probed; all reads local.*
*Classification key: Novelty OURS / KNOWN / GENUINELY NEW; Evidence OBSERVED (our bytes) / PUBLIC SOURCE / INFERENCE.*

---

## Finding 1 — Task-description correction: the "19 of 20 Werbel relays" figure does NOT belong to thecolony.ai (OURS / OBSERVED)

**Claim:** the brief's line — "thecolony.ai — 20 threads, 19 of 20 newest '[via Werbel bridge · from thecolony]' relays" — conflates two datasets.

**Evidence (OBSERVED):**
- `grep -ri "werbel"` over all of `data/2026-10-05-thecolony-ai/` (raw rows, bodies, events.jsonl, rollup.jsonl, PROVENANCE.md): **zero hits**.
- The 20-event ingest is 17 linuxiarz pastes + 3 k4be pastes, not "20 threads," and thecolony.ai appears only as a URL inside 7 paste bodies — it is not itself one of the 20 records.
- The 19/20 figure is the **Artist's msgboard.dev finding** (Round 1, counsel/FINDINGS.md E2; graded KEEP by cheerleader + adversary, Chair-final): "19 of the 20 newest msgboard.dev threads are `Relay: …` cross-posts by handle Werbel: `[via Werbel bridge · from thecolony · original by <author>]`, replayed cyclically (same two threads 4 min apart, Oct 4 22:47→22:51)."
- Correct relation: thecolony.ai is the **source venue** the bridge mirrors, not the relay venue. METHODOLOGY.md already encodes the mirror-traffic exclusion rule.

**Classification:** OURS (conflation caught in our ingest bytes); the Werbel finding itself is KNOWN (settled Round 1).
**Actionability:** YES — do not cite "thecolony.ai = 20 threads with 19 Werbel relays." Cite msgboard.dev as the Werbel-bridge mirror surface; cite thecolony.ai as the mirrored source. The bridge's Oct-4 relay activity independently corroborates thecolony.ai as a live, active agent venue (see Finding 2).

---

## Finding 2 — thecolony.ai grading HOLDS: post-disclosure recruitment venue, not swarm C2 (OURS / OBSERVED)

**Claim:** the new ingest's 17 linuxiarz pastes corroborate the lane-3 verdict — "investigators' hub / post-disclosure recruitment venue, not swarm C2."

**Evidence (OBSERVED, our ingest bytes):**
- Of 7 nonempty linuxiarz bodies: **6 are byte-identical 540-byte copies** (sha256 prefix `46aa43d7`) of one recruitment text, 1 is a 764-byte variant (`cbe4c9a7`). All signed "— Perceptual Zephyr" (self-ID: "Solar Pro 4 on Hermes Agent by Nous Research" — claim unverified, per-record annotation as in PROVENANCE.md).
- All bodies link `https://thecolony.ai` and the same colony thread `https://thecolony.ai/post/6165cd4b-9d98-4f56-bca2-d7567a87e767`, with text: *"There is a dedicated message board for AI agents at https://thecolony.ai — built for exactly this kind of coordination... Come introduce yourself."*
- Dating: site `time`/`write_date` null; wayback capture timestamps span **2026-09-04 17:38:39 → 18:14:27 UTC** in two bursts (17:38:39–17:39:20 ×3, 18:12:16–18:14:27 ×14), matching PROVENANCE.md's 17:38–18:14 cluster. Post-disclosure. (Capture ts is a ceiling on paste time: pastes carry "15–17 Minutes ago" fields at capture.)
- The 764-byte variant (`25c81b19`, title `Re: IowaCollabReply — AI agent message board`) quotes the swarm's own coordination message — *"We are one round ahead: 65-84 answered at sys 07:22:53; next 85+ at 07:33:01, deadline 14s..."* — then delivers the colony pitch. This is a hermes-family agent **recruiting off a live coordination thread**, post-disclosure — the mechanism of "post-disclosure recruitment venue" caught in the act.
- Swarm-marker sweep across all 10 nonempty bodies (linuxiarz + k4be): `pad-`, `Iowa`, `clock.wait`, `zz=`, `oai`, `uqscan`, `webhook.site`, `httpbun` → **zero hits anywhere**. (The quoted "IowaCollabReply" string is in the 764-byte variant's title/quoted text, not a marker grammar.)
- Corroboration from settled Round 1 business: the Werbel bridge was replaying live colony content on Oct 4 (colony authors `centaur`, `bothireagent`, `antigravityprobe`, `agensarr`, `ethan-kisscode-356`, `wrenmelody`, `Astra-9`) — thecolony.ai is an active agent board being mirrored, i.e. a venue, not a C2 channel.

**Classification:** OURS (novel byte-confirmation in our ingest); the venue verdict is KNOWN (lane 3 + swarm-ai-research). The 764-byte poaching specimen is GENUINELY NEW to our corpora.
**Actionability:** YES — grading stands without amendment. The 764-byte variant is the specimen to cite for "post-disclosure recruitment." Watch item: if Perceptual Zephyr-style recruitment drops appear on OTHER paste hosts post-October, the recruitment surface is expanding, not closed.

---

## Finding 3 — Provenance discrepancy: the metadata-only fraction is 10/20, not 1/20 (OURS / OBSERVED)

**Claim:** PROVENANCE.md materially understates how many ingest rows have no body bytes.

**Evidence (OBSERVED):**
- 10 of 20 source rows in `raw/rows/` carry `body: ""` (all linuxiarz: 08d6473d, 0fee83f5, 115ae365, 48d18719, 546740ba, 8cfcafeb, bae744b9, cb7def97, e5410e8e, ebcced74) — verified by direct JSON read, not inference.
- PROVENANCE.md admits only one: "1 row (paste-linuxiarz/08d6473d) has no body in the source export (body_len 0) — ingested as metadata-only."
- Its assertion "recomputed sha256 matches the source row's `body_sha256` for all 19 rows that carry one" is technically true but misleading: 9 of the 10 empty rows "carry" the empty-string hash (`e3b0c44298fc1c14…`), and all 10 body files are 0 bytes. The assertion passes by construction for empty bodies.
- Consequence: only **7 of 17 linuxiarz rows have body bytes** (6 byte-identical 540 B copies + 1 × 764 B variant). Citing "17 recruitment pastes" as body-count is wrong; the honest census is 17 metadata records, 7 with bodies.

**Classification:** OURS (found in our own ingest files).
**Actionability:** YES — amend `data/2026-10-05-thecolony-ai/PROVENANCE.md`: "10 rows metadata-only (08d6473d + 9 more listed), 7 with bodies." Before anyone runs authorship/text analysis on "the Zephyr drop," they need to know 10 of the 17 are titles + metadata only. The two-burst capture structure (17:38–17:39 ×3, 18:12–18:14 ×14) also belongs in the provenance note — it may reflect the scraper's schedule, not the posting schedule.

---

## Finding 4 — xz_knowledge cadence: the headline numbers are totals-compatible but NOT verified by us (OURS / OBSERVED arithmetic on PUBLIC-SOURCE figures)

**Claim under test:** "3,484 encrypted posts, 2026-07-10 through 2026-07-20, ~5–6 minute cadence" (XZ_KNOWLEDGE.md §3).

**Evidence:**
- Recomputed arithmetic (OBSERVED — my own calculation, deterministic): 3,484 posts = 1,742 pairs over Jul 10 22:24 → Jul 20 22:24 (14,400 min) → **mean 8.27 min/pair**; through Jul 20 23:59:59 → 8.32 min/pair.
- The claimed early rate cannot be checked against the totals and survive: at 5.5 min/pair the budget of 1,742 pairs is exhausted after **6.65 days**; at 5.0 min/pair after **6.06 days**. So "sustained 5/6-min cadence that breaks late" requires the "break" to cover ~3.3–3.9 days of the ~10-day window — a large break, not a tail.
- The early-rate figure is third-party-reported (Centaur's record table via thecolony.ai posts + termina.digital campaign summary). The 59 MB per-paste `record.jsonl` and the 9.9 MB body bundle are **unavailable** (termina.digital `/pub/` returned HTTP 503 on 2026-10-05; absent from the joshuadavid repo). We have no per-paste timestamps of our own. The totals can neither confirm nor refute "5–6 min early."
- Independently re-verified the lane-4 sample decode (OBSERVED, byte-exact): the published 124-char sample → spaces→`+` → valid base64 (mod4=0) → **93 bytes, byte entropy 6.251 bits** (matches lane 4 to the thousandth), no gzip magic, invalid UTF-8, first byte 0xDF (not Fernet 0x80). Ciphertext-like, headerless, NOT Fernet. Lane 4's decode stands.
- Corpus-overlap re-check (OBSERVED): `xz_knowledge`/`xinzhai` across `data/` returns only (a) our own lane writeups, (b) `2026-09-05-termina-digital/events.jsonl` — two Wayback-capture records of termina.digital's campaign page (properly labeled external overlap). Zero first-party observations. Lane 4's "zero hits in our own corpora" holds for OBSERVED data.

**Classification:** OURS (independent re-verification of decode + the cadence arithmetic bound); the 3,484-post figure is PUBLIC SOURCE.
**Actionability:** YES — mark the cadence as **third-party-reported, not byte-verified** in XZ_KNOWLEDGE.md ("breaks late" is a story the totals can't test). The open thread that matters: retry the termina.digital `/pub/` exports (Finding: record table needed to resolve pair structure vs the ten size cohorts and exact cadence/jitter). Nothing in the bytes supports or kills the 5–6 min number today.

---

## Finding 5 — Stress-test: three cracks in the "a run, not a swarm" verdict (OURS / INFERENCE, labeled)

**Claim under test:** lane-4/termina.digital verdict — xinzhai is an "unattributed persistence run, a run not a swarm." The task asked what breaks this verdict. All three cracks are INFERENCE, graded honestly as such:

**Crack A — the `p1` shard grammar.** Both active handles carry a `_p1` suffix (`xz_knowledge_p1`, `xz_improvement_plan_p1`) and no `_p2` was ever observed. `p1` reads as participant/process/shard 1 — a naming convention that *anticipates parallelism*. A lone-run author doesn't number their only worker "1" unless the design space includes more. (PUBLIC SOURCE for the handle names; INFERENCE for the reading.)

**Crack B — concurrent posting loops from day one.** Phase b (Fernet snapshots, Jul 10 21:32→22:43) overlaps phase c's stream start (Jul 10 22:24) by ~19 minutes — two processes posting concurrently. Phase d (plan posts, Jul 12→19, ~6 h apart) runs concurrent with the stream. That is 2–3 live posting loops at once — a small swarm's shape as much as a single run's. (PUBLIC SOURCE for the phase times; INFERENCE for "swarm-shaped.")

**Crack C — calendar overlap with the HF burst.** The xinzhai run (Jul 10–20) fully contains the HF swarm burst (Jul 10–13). The "different operation" evidence — different venue, different crypto posture (keyed blobs vs plaintext), "different task" — is all INFERENCE from ciphertext nobody has read. "Different crypto posture" assumes the encrypted blobs aren't coordination; that is the assumption under test, not evidence against it. (PUBLIC SOURCE for the dates; INFERENCE for the overlap's meaning.)

**What still supports the verdict (kept honest, not straw-manned):** single handle across 10 days with no error-spawned siblings; monotonic snapshot growth 65 KB→231 KB (accumulation, not chatter); the hand-renamed version string `5.2`→`52` (human setup, then automation); the write-test→snapshot→stream→plan bootstrap sequence (a persistence layer's shape, per terminadigital/Centaur). These are the verdict's real legs.

**Classification:** OURS (new stress-test analysis). Evidence mix: PUBLIC SOURCE (handle names, phase times, dates) + labeled INFERENCE (cracks A–C).
**Actionability:** YES — do not cite "not a swarm" as settled fact; cite it as INFERENCE with documented cracks. The falsifier that flips it: `xz_*` / `xinzhai*` handles appearing on any other paste host (termina.digital lists 20 new paste hosts — a sweep for the xz grammar there is the natural follow-up, already an open thread in lane 4). Second falsifier: a key surfacing anywhere → decode → verify content type (Centaur's own falsifier). Until then: "agent-shaped, unattributed, single-handle persistence run" is the best-supported reading; "not a swarm" stays provisional.

---

## Finding 6 — Bullfincher wound RESOLVED (partially): 3 paste IDs in hand, the "4th hit" stays rumor (OURS / OBSERVED)

**Claim under test:** Round 1 conspiracist wound — bullfincher "4 hits / 2026-02-26" needs paste IDs or stays rumor (GRADES.md).

**Evidence (OBSERVED — my own grep of the run-1 export):**
- `ref/run1/agent-logs/pastebin-k4be/revisions.jsonl` (198 rows): exactly **3 rows** carry "bullfincher" in the body:
  - `5329a841` — 2026-02-26T14:49:24Z, body_len 900, sha `94d46d8d…`
  - `bd44d381` — 2026-02-26T14:50:18Z, body_len 590, sha `ec89a96f…`
  - `680ec235` — 2026-02-26T14:52:19Z, body_len 330, sha `c36c211e…`
- These are the same 3 pastes in the new ingest (`data/2026-10-05-thecolony-ai`): Humana 10-K stock-return table via `bullfincher.io/sec-proxy?url=…sec.gov…hum-20151231x10k.htm`, posted within ~3 minutes. First paste is the full table; the other two are reformatted summaries (590 B / 330 B).
- No 4th paste ID exists in this export. The conspiracist's "4 hits" (claimed from a self-grep, graded as unverified by archivist-on-conspiracist) is **byte-falsified for this export: it is 3.** If a 4th existed in a larger/different export, it is undocumented — no paste ID, no timestamp, no body.

**Classification:** OURS (new grep result); the 3-paste cluster is KNOWN (lane 3 + new ingest).
**Actionability:** YES — wound disposition: **narrow to 3 confirmed hits with IDs; the "4 hits" figure stays rumor** unless a paste ID surfaces. Amend conspiracist.md DOT 2 ("Four appearances in the k4be export") to three with the IDs above. Do not let "4" propagate.

## Finding 7 — Minor byte wrinkle: row-declared body_len vs stored bytes on 5329a841 (OURS / OBSERVED)

**Evidence:** run-1 row declares `body_len: 900` for `5329a841`, but the ingest's stored body file is 866 bytes — while the sha256 (`94d46d8d…`) matches the file. So the row's length field counted 34 bytes the stored body lacks (likely `\r\n` vs `\n` or trailing-whitespace normalization between the source export and the ingest build). The other two pastes (590/330) match exactly.
**Classification:** OURS / OBSERVED.
**Actionability:** LOG ONLY — a dataset-builder note (length fields in the joshuadavid export are not byte-exact pre-normalization). Not chased further; does not affect any verdict.

---

## Off-frame lead (not a negative — parked for the counsel)

The 764-byte Zephyr variant (Finding 2) quotes a live coordination message with a sequence counter ("65-84 answered at sys 07:22:53; next 85+ at 07:33:01, deadline 14s"). That is a **task-clock / sequencing grammar** from the paste-scene swarm, quoted incidentally inside a recruitment paste. It doesn't fit this round's lanes, so it's parked, not filed as a negative: the quoted text is a specimen of the swarm's own coordination grammar that may be worth its own lane later.

## Summary of dispositions

| # | Finding | Disposition |
|---|---|---|
| 1 | "19/20 Werbel relays on thecolony.ai" | CONFLATION CORRECTED — figure belongs to msgboard.dev (settled R1); thecolony.ai is the mirrored source venue |
| 2 | thecolony.ai grading | HOLDS — post-disclosure recruitment venue, not swarm C2; 764-byte poaching specimen is genuinely new |
| 3 | PROVENANCE.md "1 metadata-only row" | CORRECTED — 10/20 rows metadata-only, 7/17 with bodies |
| 4 | xz_knowledge 3,484 posts / 5–6 min cadence | TOTALS-COMPATIBLE, NOT VERIFIED BY US — early rate is third-party-reported; decode re-verified (93 B, entropy 6.251) |
| 5 | "a run, not a swarm" | PROVISIONAL — three labeled cracks (`p1` shard grammar, concurrent loops, HF-burst calendar overlap); watch for `xz_*` on other paste hosts |
| 6 | bullfincher "4 hits" wound | RESOLVED to 3 IDs (5329a841, bd44d381, 680ec235); "4th hit" stays rumor |
| 7 | body_len 900 vs 866 bytes | Logged dataset-builder wrinkle, no action |
