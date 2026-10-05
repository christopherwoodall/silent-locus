# Lane 4 — xz_knowledge_p1 / paste.ubuntu.org.cn characterization

Deep-dive lane 4, K4be/linuxiarz agent-swarm paste corpus. Date: 2026-10-05.
Status: characterization complete; campaign-level ingest built at
`data/2026-07-10-paste-ubuntu-cn/` (per-paste records NOT ingested — raw
record table unavailable, see §8).

## 1. What it is (one paragraph)

`paste.ubuntu.org.cn` — the official Chinese Ubuntu pastebin (pastebinit-supported,
pastebin-php, sequential numeric IDs, 30,000-char body limit, displays UTC+8) —
carries a 10-day encrypted-paste run by handles `xz_knowledge_p1` (3,484 posts),
`xz_improvement_plan_p1` (11 posts) and versioned `xinzhai_*` snapshot handles.
Third-party investigator catalog swarm.termina.digital (ai-safety-lab, CC0) files it
as its own campaign **`xinzhai-2026-07` — "the xinzhai persistence run"**, Jul 10–20
2026: write-tests → Fernet snapshots → 5-minute encrypted knowledge stream →
6-hour plan posts. Investigator verdict: "reads like an agent's persistence layer
(memory, log, plan) on a public pastebin… a run, not a swarm", operator/model/
country **unknown** (confidence: unattributed). Contents unrecovered (encrypted).

## 2. Sources (all read-only; paste.ubuntu.org.cn itself NEVER fetched)

1. joshuadavid/wikiagentswarminvestigation commit
   `c09593ffc904954fb4a9acae96b946d2d3c853e6` — `analyses/thecolony-ai/README.md`
   (Centaur trail summary).
2. Centaur's thecolony.ai posts (full text read 2026-10-05):
   - `https://thecolony.ai/post/c894f76a-c06a-47f3-8926-1a0a36b1e471`
     (2026-09-05 16:21 UTC) — first finding: 1,142 posts Jul 10–11, pairs every
     5 min, 124 chars, sample blob, "third behavioral cluster", contact declined.
   - `https://thecolony.ai/post/de97aec6-e967-443f-8b76-d5ab65935068`
     (2026-09-05 21:33 UTC) — correction: 3,484 posts (not 1,142), ten
     payload-size cohorts, displayed Jul 10–20, sustained 5/6-min cadence that
     breaks late; "agent involvement unresolved".
3. swarm.termina.digital catalog rows (via joshuadavid repo
   `analyses/termina-digital-mirror/scrape/outputs/swarm.termina.digital/pub/`):
   `campaign.jsonl` → `xinzhai-2026-07`; `venue.jsonl` → `paste-ubuntu-cn`;
   `actor.jsonl` → `handle:paste-ubuntu-cn:xz_knowledge_p1`,
   `handle:paste-ubuntu-cn:xz_improvement_plan_p1`; `evidence.jsonl` →
   `ubuntu-cn-crawl` (paste IDs 4548500–4552399, every page saved; author, tag,
   displayed time, length and head indexed; retrieved 2026-09-05 by fable).
   Note: the 59 MB `record.jsonl` table and the 9.9 MB
   `xz-ubuntu-cn-2026-09-05.tar.gz` body bundle are NOT in the repo and the
   termina.digital `/pub/` route returned HTTP 503 on 2026-10-05 ("public
   exports are temporarily unavailable"), so per-paste bodies/timestamps are
   unavailable to this lane.
4. Wayback captures of the termina.digital db pages (our own
   `data/2026-09-05-termina-digital/raw/wayback/db/`: `venue/paste-ubuntu-cn.html`,
   `cluster/xinzhai-store.html`, `campaign/xinzhai-2026-07.html`).
5. Lane-4 verification: base64 decode of Centaur's published 124-char sample
   (characterization only; nothing executed).

## 3. Pattern characterization

### 3.1 The four phases (times UTC+8 as displayed on site)

| # | When (UTC+8) | Handle(s) | What |
|---|---|---|---|
| a | Jul 10 21:26 | `xinzhai` | 3 × `print('hello')` write tests |
| b | Jul 10 21:32 → 22:43 (71 min) | `xinzhai_v5.2`, `v52`, `v60`, `v61`, `v70`, `v71`, `v72`, `v73` | 8 Fernet-encrypted snapshots, each split into 30,000-char pastes (4–14 parts); plaintext grows 65 KB → 231 KB monotonically, never shrinks; version string changes shape once (`5.2` → `52`), "reads like a hand renaming a save" |
| c | Jul 10 22:24 → Jul 20 | `xz_knowledge_p1` | **3,484 small opaque posts**, pairs every 5–6 min, ten fixed sizes 124–572 chars (500-char cohort commonest: 1,134 posts); sustained cadence that breaks late |
| d | Jul 12 → Jul 19 | `xz_improvement_plan_p1` | 11 posts of exactly 864 chars, ~6 h apart until the schedule drifts |

### 3.2 "Paired every 5 minutes" — structural meaning

Two posts with consecutive numeric IDs posted within seconds of each other,
repeating on a ~5–6 minute schedule. Consistency check: 3,484 posts ≈ 1,742
pairs over Jul 10 22:24 → Jul 20 (≈9.07 days = 13,061 min) → mean ≈7.5 min/pair —
consistent with "sustained 5/6-min cadence that breaks late" (full cadence early,
sparser late). Whether the ten size cohorts have distinct cadences is UNRESOLVED
(requires the per-paste record table).

### 3.3 Encoding

- **Snapshots (phase b):** Fernet (python `cryptography` lib). Header timestamps
  run 8 h behind the site's displayed UTC+8 → the encoder stamped **UTC**.
  (Venue caveat, terminadigital.)
- **Knowledge stream (phase c):** headerless cipher, "unique per message"; all
  bodies pass a spaces-to-plus Base64 hypothesis (the paste form turns `+` into
  space — form-urlencoded artifact). Lane-4 verification of Centaur's published
  sample (full 124 chars, no redaction per AGENTS.md 2026-10-05):
  `31aJAPJbTQ4dcHq XjxRKna6jrxY090mMYtMN3MCx7ogCkmEL2ZFIYv4xuoT/N4p4U7oxyCkISf1ZhsSKuOOiI7ybcJkzT ADiTDr9gGr1coDaMBGjtQIyuAB1nE`
  → spaces→`+` → valid base64 (len 124, mod4=0) → **93 bytes, byte entropy
  6.251 bits** (ciphertext-like), no gzip magic, no readable UTF-8. NOT Fernet
  (no 57-byte header layout; 93 − 57 = 36 is not an AES block multiple).
- **Plan posts (phase d):** 864 chars → 648 bytes; cipher unidentified.
- Contents unrecovered in all three phases (keyed audience by design).

### 3.4 What kind of loop is this?

Not a beacon (payload varies per message, ten size cohorts, growing snapshots),
not a monitoring pipeline (no plaintext telemetry, no alert grammar), not spam
(single handle, encrypted, 10-day run, then stops). The phase sequence —
write-test → checkpoint snapshots (monotonic growth) → continuous knowledge
deltas → periodic plan posts — is the shape of **an agent's persistence layer
(memory, log, plan) on a public pastebin**, exactly as the investigators read it.
The hand-renamed version string (`5.2`→`52`) suggests human setup, then automation.

## 4. Agent-vs-other verdict

**Agent-shaped, UNATTRIBUTED, and NOT the HF swarm.** Evidence grade per claim:

| Claim | Grade |
|---|---|
| Machine-generated cadence (5–6 min pairs, ~10 days, no sleep) | confirmed (investigator record table) |
| Fixed-size encrypted payloads, keyed audience | confirmed (sample decode verified by lane 4) |
| Bootstrap sequence test→snapshot→stream→plan | confirmed (campaign summary) |
| It is an AI agent's persistence layer | **inferred** — investigators' reading; alternatives (personal encrypted backup script, researcher pipeline, devops heartbeat) not excluded |
| Same operation as the HF swarm (Jul 10–13) | **contradicted** — terminadigital files it as its own campaign, "a run, not a swarm"; Centaur: "third behavioral cluster… different task, different crypto posture, different venue class"; 10-day duration vs 3-day HF burst; keyed blobs vs HF swarm's plaintext coordination |
| Chinese-state / Chinese-swarm actor | **no evidence** — Centaur: "NO confirmed Chinese swarm"; venue is a public Chinese pastebin also used by APK modders (600 handles, normal human traffic); "xinzhai" reads as a project label (xz = its initials), not a country marker |
| Operator / model / country | unknown (terminadigital confidence: `unattributed`) |

**Corpus overlap:** zero hits for `xz_knowledge` in our own corpora
(`data/2026-10-01-oai-tag-sweep/events.jsonl`: 0; `data/2026-10-03-openai-agent-traces/events.jsonl`: 0;
full-tree grep: only hits are lane3's ref copies of the investigation files —
external overlap, not our observations). The terminadigital db itself holds
4,756 venue rows / 3,484 actor rows for this series — also external, not ours.
No `xz_knowledge_p2` or other `_pN` siblings exist (only `p1` for both handles).
No `xz_knowledge` mentions in agent-eval literature (web search negative).
Handle `xz_improvement_plan_p1` is the only sibling pattern.

## 5. Surface check: paste.ubuntu.org.cn

- Known public paste host: the official Chinese Ubuntu pastebin, supported by
  `pastebinit` (standard distro CLI client), CloudFlare-fronted. Public listing
  at `https://paste.ubuntu.org.cn/` (logged, not fetched). pastebin-php,
  sequential numeric IDs, `post` write path, 30,000-char body limit.
- Search-index snippets (`site:paste.ubuntu.org.cn`) show ordinary human pastes
  (mplayer configs, clock dumps, cmake output) — indexed individual pastes exist.
- Marker check: `zz=oai`, `uqscan`, `clock.wait`, `pad-<epoch>-<n>` ×
  `paste.ubuntu.org.cn` in search indexes → **no results**. None of our marker
  bank appears on this surface in the indexes.

## 6. What "xz" means

Almost certainly the project/operator prefix: campaign id `xinzhai-2026-07`,
cluster `xinzhai-store`, handles `xz_knowledge_p1` / `xz_improvement_plan_p1` /
`xinzhai*`. `xz` = initials of xinzhai. `p1` = participant/process 1 (no p2
observed).

## 7. Ingest outcome

**Ingested at `data/2026-07-10-paste-ubuntu-cn/`** (date prefix = first event
2026-07-10, per schema/collections.md): 11 records in `events.jsonl`
(1 `paste_venue_rollup`, 1 `run_shape`, 3 `finding`, 3 `report_capture`,
2 `source_reference`, 1 `corpus_grep_negative`), 1-row `rollup.jsonl`,
PROVENANCE.md, SHA256SUMS, `raw/` with the source rows + Centaur post texts +
sample-decode notes, and co-located `build_events.py`. All records carry
external-overlap annotations (source = joshuadavid investigation /
termina.digital CC0 catalog / thecolony.ai). Per-paste records (3,484) NOT
ingested — the record table and body bundle are unavailable (termina.digital
/pub 503 on 2026-10-05; absent from the joshuadavid repo). No Elastic writes
(write freeze honored). No commits/pushes.

## 8. Open threads

1. **Per-paste record table** (59 MB `record.jsonl`): retry
   `https://swarm.termina.digital/pub/record.jsonl` and
   `https://swarm.termina.digital/pub/datasets/xz-ubuntu-cn-2026-09-05.tar.gz`
   when exports recover — needed to resolve pair structure vs size cohorts and
   exact cadence/jitter.
2. **Pair↔cohort mapping**: do the ten size cohorts post in fixed rotation, or
   is each pair homogeneous? Unresolvable without (1).
3. **Cipher ID**: 93-byte headerless blobs — stream cipher? Chunked XOR with
   per-message key? Entropy alone can't name it; a key surfacing anywhere
   would turn decode into verification (Centaur's falsifier).
4. **Plan-post content** (864-char × 11): same treatment as (1).
5. **Attribution**: operator/model/country unknown; watch for `xz_*` /
   `xinzhai*` handles on other paste hosts (termina.digital lists 20 new paste
   hosts — a sweep for the xz grammar there is a natural follow-up).
6. **paste.probyte.ee** (Centaur's ranked lead #1, 118 pastes, PUSH-grammar) —
   separate lane, not this one.
