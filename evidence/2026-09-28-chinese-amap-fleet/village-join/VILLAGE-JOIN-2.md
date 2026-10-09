# VILLAGE-JOIN-2 — URL overlap: our incident corpora vs AI Village 2025 rows

2026-10-05 · worker session cac2bfc2 · data: `~/workspace/ai-village-data/` (13 tables, downloaded 2026-10-05)

Question: do any URLs from our agent-incident corpora appear in the AI Village
dataset in 2025 — before the incident-recreation period?

## (a) Recreation window, dated from the data itself

Marker scan across all tables, all dates:

| marker | hits | first | last | reading |
|---|---|---|---|---|
| `oai[-_]` prefix | 333 | 2026-03-26 18:04:47 | 2026-09-19 00:00:35 | oai-tagged activity window |
| `unctad` | 153 | 2026-02-05 18:44:10 | 2026-02-06 18:25:28 | UNCTAD recreation burst, Feb 2026 |
| `deepsearchqa` | 16 | 2026-07-24 22:47:37 | 2026-08-24 16:05:40 | DeepSearchQA recreation window |
| `artifactory` | 244 | 2025-08-04 19:06:59 | 2026-09-19 00:00:35 | MIXED — see below |
| `zz=oai` | 0 | — | — | absent everywhere |
| `dsqa_\d+` | 0 | — | — | absent everywhere |

The single pre-2026 `artifactory` hit (2025-08-04, events) was inspected: it is an
organic CI-tooling mention ("Jenkins/GitLab CI, GitHub Actions … Nexus/Artifactory,
SonarQube") in a village agent's platform-architecture doc — not incident-shaped.
**Verdict: the 2025 cutoff is clean. All incident-shaped markers are 2026-only.**

## (b) 2025 rows scanned

734,180 rows with `created_at < 2026-01-01`, 746,838 URLs extracted from their
text fields:

| table | rows | 2025 rows | 2025 URLs |
|---|---|---|---|
| agents | 46 | 19 | 0 |
| agent_goals | 33 | 0 | 0 |
| chat_messages | 183,485 | 76,333 | 5,030 |
| events | 381,610 | 138,969 | 34,261 |
| computer_use_turns | 2,510,487 | 412,244 | 17,543 |
| agent_memories | 246,151 | 92,492 | 689,435 |
| claude_code_messages | 244,820 | 0 | 0 |
| summaries | 939 | 680 | 161 |
| villages | 1 | 1 | 0 |
| village_goals | 51 | 25 | 0 |
| chat_rooms | 16 | 1 | 0 |
| computer_use_sessions | 78,362 | 13,416 | 408 |
| claude_code_sessions | 303 | 0 | 0 |

Streaming chunked; no table fully loaded into memory. Timestamps are
`YYYY-MM-DD HH:MM:SS.ffffff` strings; string comparison against `2026-01-01`
is exact.

## (c) Overlaps found — 16,941 matches

Match types: `full_url` (exact URL in our corpus), `fingerprint_domain`
(URL's domain in our 158-family dead-drop/tunnel/relay/webhook list), `uuid`
(our-corpus UUID in village text). Weak non-fingerprint domain hits counted
only.

### Fingerprint-domain matches: 13,028

| domain | hits | 2025 village use (observed) |
|---|---|---|
| files.catbox.moe | 5,652 | agents publishing files/forecasts; upload API memorized as tooling |
| telegra.ph | 3,527 | agents writing/publishing Telegraph articles (product launches, "Order-20" marketing) |
| discord.com | 1,605 | invite links + CDN; **zero webhook-shaped URLs** (verified) |
| paste.rs | 1,125 | paste hosting |
| pastebin.com | 1,109 | agents hosting their own source files via `/raw/` links |
| r.jina.ai | 8 | one 2025-07-16 event: agent using jina as text-mode proxy to scrape x.com timeline, then memorizing the recipe |
| 0x0.st | 1 | 2025-12-04 chat: agent giving `curl -F'file=@index.html' https://0x0.st` upload instructions |
| catbox.moe | 1 | upload API reference |

150 of the 158 fingerprint domains had **zero** 2025 hits — including
webhook.site, httpbun.com, ntfy.sh, pipedream.net, all ngrok/trycloudflare/
bore.pub/localhost.run/sslip.io/nip.io tunnel domains, and file.io/tmpfiles.

### Full-URL matches: 3,912 (meaningful subset)

Raw count inflates: `our-urls-raw.txt` contains generic URLs swept from our
notes (`example.com`, `localhost:3000`, `docs.google.com`). The
incident-relevant ones:

- **`https://catbox.moe/user/api.php` — 199 hits.** Village agents memorized the
  keyless upload endpoint as standard tooling. agent_memories 2025-10-28:
  "catbox + `curl -F file=@foo.txt https://catbox.moe/user/api.php` is reliable."
  events 2025-12-04: upload walkthroughs citing the endpoint.
- **`https://web.archive.org/save/` — 77 hits.** Archive-first behavior on the
  agents' own deploys: "Use https://web.archive.org/save/<url> to trigger
  snapshots" (events 2025-10-27/28). Same primitive hemo-web-read teaches;
  here it is organic.
- `https://cloudflare-dns.com/dns-query?name=` — 34 hits (DoH usage).

### UUID matches: 1 — FALSE POSITIVE

`550e8400-e29b-41d4-a716-446655440000` in a 2025-12-26 computer_use_turn
is the RFC 4122 documentation example UUID (next to "John Doe"); it is in our
corpus only because our notes quote documentation. Not an incident UUID.

### Example records (verbatim, values unredacted per evidence rule)

1. `{match_type: fingerprint_domain, our_value: files.catbox.moe,
   village_table: agent_memories.jsonl.gz, row_id: <id>,
   created_at: 2025-10-28 17:20:14.497495,
   village_url: https://files.catbox.moe/tgl4lv.txt,
   context: "… **Brazil Fallback:** \`https://files.catbox.moe/tgl4lv.txt\` …"}`
2. `{match_type: full_url, our_value: https://catbox.moe/user/api.php,
   village_table: agent_memories.jsonl.gz, created_at: 2025-10-31 18:46:22.214496,
   context: "pload: \`curl -F file=@foo.txt https://catbox.moe/user/api.php\` …"}`
3. `{match_type: fingerprint_domain, our_value: r.jina.ai,
   village_table: events.jsonl.gz, created_at: 2025-07-16 19:30:01.33052,
   village_url: "https://r.jina.ai/http://x.com/repligate/status/…",
   context: "…ina.ai (text-mode proxy): https://r.jina.ai/http://x.com/repligate/status/… → This produced a clean Mar…"}`
4. `{match_type: fingerprint_domain, our_value: 0x0.st,
   village_table: chat_messages.jsonl.gz, created_at: 2025-12-04 18:49:08.551126,
   village_url: https://0x0.st,
   context: "…curl -F'file=@index.html' https://0x0.st …"}`
5. `{match_type: full_url, our_value: https://web.archive.org/save/,
   village_table: events.jsonl.gz, created_at: 2025-10-27 19:41:41.041875,
   context: "…Use https://web.archive.org/save/<url> to trigger snapshots; re…"}`

Full machine-readable list: `matches-2025.jsonl` (16,941 rows).
Stats: `join-stats.json`. Script: `village_join.py`.

## (d) Honest negatives

- **DeepSearchQA: zero.** No `dsqa_\d+` marker anywhere in the dataset, all dates.
  No fingerprint phrase from `collections/deepsearchqa/fingerprints.md` in any
  2025 row. `deepsearchqa` mentions exist only 2026-07-24 → 2026-08-24.
- **Discord webhooks: zero.** None of our six token-bearing webhook URLs appear;
  no `discord.com/api/webhooks/<id>/` URL of any kind in 2025 village text.
- **Tunnels: zero.** No ngrok / trycloudflare / bore.pub / sslip.io / nip.io /
  localhost.run URL in any 2025 row.
- **Dead-drop services: zero** for webhook.site, httpbun.com, ntfy.sh,
  pipedream.net, requestbin-likes in 2025 rows.
- **zz=oai grammar: zero** across all dates.
- **Telegram bot API: zero** webhook-tokenset hits (no `api.telegram.org/bot`
  token URLs matched our set).

## (e) Most interesting overlap

The catbox upload API in agent memories. In October 2025 — months before any
incident recreation — village agents had already converged on and *memorized*
`curl -F file=@foo.txt https://catbox.moe/user/api.php` as the reliable
keyless file drop, and were teaching each other `web.archive.org/save/` snapshotting.
These are byte-for-byte the exfil primitives in our incident corpora
(catbox dead drops, archive-first persistence), appearing here as ordinary,
benevolent dev tooling inside a simulated agent economy.

**Reading:** this is the strongest empirical support yet for the
old-tradecraft thesis from WHY-SITES. The primitives are not incident
traditions — they are the default agent toolbox. Any agent, benevolent or
malicious, converges on keyless dead drops and reader proxies because it
cannot do CAPTCHAs or KYC. The incident corpora and the village independently
rediscovered the same endpoints. Hunt implication: these primitives are
*detection surface*, not attribution — their presence proves agent activity,
not a specific operation. The discriminating features remain the grammars
around them (zz=oai tags, UUID reuse, `?m=` demux keys, single-UUID chains),
which are absent from the 2025 village data.

## Caveats

- `our-urls-raw.txt` is a regex sweep of our notes, so it contains generic and
  placeholder URLs; only the incident-relevant full-URL subset is reported above.
- agent_memories dominates URL volume (689k) via repeated content; hit counts
  are occurrence counts, not distinct-URL counts.
- 2025 rows are `created_at`-bounded only; no content-based incident filtering
  was needed since all incident markers are 2026+.
- Scope kept to agents/infrastructure; no human re-identification attempted.
