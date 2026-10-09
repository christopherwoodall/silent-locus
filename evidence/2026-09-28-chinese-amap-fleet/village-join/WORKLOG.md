# VILLAGE-JOIN worklog

## 2026-10-05 ~14:05 CDT — session dce69c47 (VILLAGE-JOIN)

### Objective
Join our silent-locus URL fingerprints against the AI Village dataset
(aidigestorg/ai-village), 2025 rows only (before the incident-recreation window).

### Finding 1 — DATA NOT PRESENT (blocker)
- `~/workspace/ai-village-data/` does not exist on this VM. Prior notes say it
  was downloaded 2026-10-01 (~5.1GB, 11 tables) but the directory is gone.
- `~/workspace/swarm-forensics/AI-VILLAGE-SCHEMA-MAP.md` also missing;
  `~/workspace/swarm-forensics/` contains only an empty `viz/` dir.
- `~/.cache/huggingface/hub/` contains only `datasets--google--deepsearchqa` —
  no ai-village cache.
- HF API confirms dataset is `gated: manual` (sha 838b4150303ca8228e8edb432d8b8ccae353d258,
  lastModified 2026-09-20T13:54:41Z). File listing is public (390 siblings);
  actual file downloads return HTTP "Access to dataset aidigestorg/ai-village
  is restricted... Please log in." — verified with unauthenticated curl on
  `agents.jsonl.gz`.
- No HF token is available to this session (no cached token, no env var).
  Per credential rules I did not hunt for one. The 2026-10-01 token came from
  BigSexyWarlock69 in main chat and is not in my context.

### Finding 2 — dataset layout (from public file listing, no auth needed)
Saved full manifest: `ai-village-manifest.txt` (390 entries).
Text tables (jsonl.gz): agent_goals, agent_memories, agents, chat_messages,
chat_rooms, claude_code_messages, claude_code_sessions, computer_use_sessions,
computer_use_turns, events, + example.py, SCHEMA.md, CHANGELOG.md, README.md.
Plus ~380 `images/computer-use-turns/YYYY-MM-DD.tar` screenshot tars
(prior notes excluded these from the download — keep that exclusion).

### Done — reference URL set built from OUR corpora
Source: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/`
(md/json/jsonl/txt, regex `https?://...`, trailing punctuation stripped).
- `our-urls-raw.txt`: 619,468 raw URL matches (dup-heavy across files).
- `our-domains.txt`: 13,806 distinct domains with counts.
- `our-fingerprint-domains.txt`: 158 domains in dead-drop / tunnel / relay /
  webhook families, with counts. Top: r.jina.ai (812), cors.bwa.workers.dev (684),
  pastebin.k4be.pl (535), pastebin.tarcseh.me (404),
  oai-scratchpad-cache-versioning-demo.ngrok.io (380), httpbun.com (155),
  webhook.site (64), discord.com (12), ntfy.sh (11), bore.pub (8).

### NOT done (blocked on data access)
- Village-side URL extraction, 2025 row restriction, recreation-window dating,
  and the actual join.
- Recreation window is UNVERIFIED — could not be established without the data.

### What unblocks this
Parent needs ONE of:
1. The HF token (BigSexyWarlock69's 2026-10-01 grant) passed via the approved
   secure flow, then: `curl -H "Authorization: Bearer <token>"` the jsonl.gz
   tables into `~/workspace/ai-village-data/` (skip the images/*.tar files).
2. Or re-download the tables to that path by any authorized route and re-ping
   this session — the join plan below then runs in one pass.

### Join plan (ready to execute once data lands)
1. Stream each jsonl.gz table in chunks (python, gzip+json, never full-load
   computer_use_turns 2.5M rows); extract URLs from text fields via the same
   regex; parse timestamps; keep rows with timestamp < 2026-01-01.
2. Date the recreation window: grep all tables for `oai`/`zz=oai`/incident
   names (UNCTAD, DoE, BEA, Artifactory) and report first/last occurrence dates.
3. Join on: full URL match, domain match (fingerprint families), webhook
   token/UUID match, DeepSearchQA phrase match (fragments from
   `~/workspace/silent-locus/collections/deepsearchqa/fingerprints.md`).
4. Report every overlap as {our_url, village_table, row_key, timestamp,
   ±30-char context, match_type}.

## 2026-10-05 ~15:48–16:15 CDT — session cac2bfc2 (VILLAGE-JOIN-2)

### Data landed
`~/workspace/ai-village-data/` — 13 jsonl.gz tables present (agent_memories 2.4GB,
computer_use_turns 2.4GB). Downloaded by parent via new huggingface skill
(`~/workspace/skills/huggingface/bin/hf-download`), revision
838b4150303ca8228e8edb432d8b8ccae353d258, `--pattern jsonl.gz`.

### Join executed
Script `village_join.py`: chunked streaming (never full-loads big tables),
markers scanned all dates, URL join restricted to created_at < 2026-01-01.
Outputs: `matches-2025.jsonl` (16,941 rows), `join-stats.json`.

### Results (see VILLAGE-JOIN-2.md for full detail)
- Recreation window: oai_prefix 2026-03-26→09-19 (333); unctad 2026-02-05→06 (153);
  deepsearchqa 2026-07-24→08-24 (16); zz=oai 0 hits; dsqa_ 0 hits. 2025 cutoff clean
  (one 2025-08-04 artifactory hit is organic CI-tooling mention).
- 734,180 rows / 746,838 URLs scanned in 2025.
- Fingerprint domains hit: files.catbox.moe (5,652), telegra.ph (3,527),
  discord.com (1,605, zero webhooks), paste.rs (1,125), pastebin.com (1,109),
  r.jina.ai (8), 0x0.st (1), catbox.moe (1). 150/158 fingerprint domains zero.
- Meaningful full-URL: catbox.moe/user/api.php (199x, memorized as reliable tooling),
  web.archive.org/save/ (77x, archive-first on own deploys), DoH (34x).
- UUID: 1 hit, false positive (RFC 4122 example UUID).
- Honest negatives: zero dsqa phrases, zero webhook tokens, zero tunnels,
  zero webhook.site/httpbun/ntfy/pipedream, zero zz=oai, zero Telegram bot tokens.
- Strongest finding: village agents independently converged on the exact incident
  primitives (catbox keyless upload, archive-first) as ordinary dev tooling in
  2025 — primitives are detection surface, not attribution.
