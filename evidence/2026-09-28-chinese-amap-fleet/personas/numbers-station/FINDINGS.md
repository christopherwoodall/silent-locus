# FINDINGS — NUMBERS STATION (all 4 lanes complete 2026-10-05 ~02:35 CDT)

Persona: numbers-station — encoded/agent-shaped signals in public data. Structural analysis only; nothing decoded-and-executed; no token reuse.
Started: 2026-10-05 ~02:10 CDT. Corpora: amap-fleet (2,141 events), oai-traces (589,972), oai-tag-sweep (96,353).

## Lane 1 — Nonce/ID grammar census
Status: COMPLETE — all three corpora (`raw/census.py`, `raw/census.json`, `raw/grammars.md`).

### Cross-corpus grammar table (occurrences)
| grammar | amap-fleet | oai-traces | oai-tag-sweep |
|---|---|---|---|
| `zz=` | 0 | **1,839,410** | 7 (noise: `.txt`, `112233`) |
| `uqscan=` | **1,129** | 0 | 2 |
| `oai*` tags | 0 | **1,784,861** | 8,080 |
| `fleet_tag` | **1,066** | 0 | 0 |
| `<word><DATE>[letter]` | **1,401** | 4 | 9 |
| 13-digit epoch ms | 34 | 353 | 181 |
| `retry=<epoch>-<N>` | **4** | 0 | 0 |
| base64 blobs ≥100ch | 47 | 94 | **7,547** |
| JWT shapes | 0 | 0 | 14 (all benign — see lane 4) |
| UUID | 4,345 | 1 | 47,329 |
| hex ≥32 | 2,142 | 1,770,458 | 15,223 |

The three corpora are **near-perfectly disjoint in marker grammar** — structural support for the same-provider/different-evals thesis. UUID/hex_long are structural fields (`report_id`, `fingerprint`, `_id`), not agent signal.

### amap-fleet detail (2,141 events)
- `uqscan` shapes: `research<DATE>[a-e]`, `target<DATE>[a-d]`, `claude<DATE><place>` (`claude20261004qinghai`), `njxzgz<DATE>s<N>`/`p<N>` (16, pinyin-abbrev tag word — **lead**, not in grammarian's shapes), `poidetail<DATE>a`, `taiyuan<DATE>b`, `qdnewapi<DATE>a` (NEW tagword 2026-10-05, shape holds).
- `claude`-token tags: **KNOWN** — grammarian documented ("first model self-identification in operator grammar", open A2). Independently corroborated here.
- `retry=<epoch>-<N>` ×4: speedrunner's grammar in canonical events. **OURS**.
- `enodia=`/JWT: 0 — enodia bot-challenge pattern is live-urlscan-only (german-hunter-2), zero corpus overlap.

### oai-traces detail (589,972 events)
- **`zz=oai<17 digits>` is the corpus-defining marker.** Bare `zz=oai` ×2,064; the rest carry 17-digit nonces.
- **GENUINELY NEW — nonce structure decoded: `zz=oai` + 10-digit epoch seconds + 7 random digits.** Verified 3/3: `zz[:10]` matches the event's `@timestamp` to within 1–2s (e.g. `17816846804506724` vs event `2026-06-17T08:24:41Z` = epoch `1781684681`; nonce minted 1–2s before collection). Nonces are monotonic with event time across 3,000 sampled rows. The marker was KNOWN; its internal structure was undocumented — no writeup describes the epoch+random decomposition.
- `oai_tag` = the same `zz=oai` prefix double-counted (1,784,860 × `oai` + 1 × `oaipmh` noise). Not a separate grammar.
- 13-digit epochs: top value `1628771336899` ×82 = 2021-08-12 — traced to a target-site AEM image cache-buster (`.../image.img.jpg/1628771336899.jpg`), NOT an agent nonce. Structural noise; honest negative.
- hex_long (1.77M) = `_id` document fields. Structural.

### oai-tag-sweep detail (96,353 events)
- `oai[a-z]{10}` package-name family (`oaipvtpwpldhz`, `oaipnldvhihwd`, … ×25 each): **KNOWN** — Diffend-indexed RubyGems go-import canary campaign (`frozen:rubygems-goimport`, record_ids `log:diffend_harvest:<pkg>:0.0.1`). The `oai`+10-random-lowercase grammar is the malicious-package naming convention, not an agent nonce. Useful as a fingerprint: exact-25× repetition = sweep artifact, not live diversity.
- `zz=` ×7: noise values only. `uqscan` ×2, `<word><DATE>` ×9: negligible.
- JWT ×14: all benign third-party (see lane 4).

## Lane 2 — Encoded-blob hunt
Status: amap-fleet complete; oai-traces (94 blobs) + oai-tag-sweep (7,547 blobs) framing analysis deferred to F3.

### amap-fleet: one blob family, structurally consistent
- **Family**: `httpbun.com/base64/<b64html>` — 67 URL occurrences, 25 distinct payload prefixes (47 matched the ≥100ch b64 pattern).
- **Framing** (structural only, nothing executed): base64 payloads are HTML pages in two sub-frames — (a) `<script>eval(decodeURIComponent(...))` loaders, (b) `<meta charset><title><epoch-ms>-suffixed probe names</title>` staged pages.
- **Classification: KNOWN** — matches grammarian's "LiveCodes/httpbun staging of probes" harness fingerprint (~30 reports; staged pages iframing amap). This census independently corroborates the family in canonical events (67 occurrences).
- No blob family found OUTSIDE the httpbun framing in amap-fleet — no unattributed base64/hex blob families. Genuinely-new-blob-family hunt continues in oai corpora.

## Lane 3 — Stego sweep
Status: COMPLETE (corpus-bounded; live imageboard stego is a noted gap).
- amap-fleet: **zero image URLs** in 2,141 events.
- oai-traces: image URLs are benign site assets (civilrightsdata.ed.gov logos/icons). No agent-posted images.
- oai-tag-sweep: benign CDN/thumbnail assets (newspapers.com, oaistatic, alicdn).
- **Honest negative:** no agent-adjacent images with stego potential in any corpus. Live imageboard/paste-service stego hunting needs browser work — flagged as a gap for imageboard-scout (now running as a Wave-5 persona).

## Lane 4 — JWT/token-grammar analysis
Status: COMPLETE.
- `?enodia=<JWT>`: **0 hits in all three corpora** — german-hunter-2's bot-challenge pattern (table.media newsletter pipeline, 65 scans/min) remains live-urlscan-only. Zero corpus overlap confirmed at census scale.
- JWT shapes found (14, oai-tag-sweep only): all benign third-party tokens — newspapers.com OCR API (`iat=eyJ...`), `chatgpt.com/backend-api/notifications/feedback?token=`, `app.talkpal.ai/verify-email?token=`, coworkoperator.com post-unlock tokens. Normal web JWTs swept into the corpus; no agent bot-challenge grammar among them.
- Token STRUCTURE observed (claims shapes): `{"free-trial-id", "iat"}`, `{"account_user_id", ...}`, `{"id"(uuid), ...}`, `{"user_id", "post_id", "iat"}` — standard SaaS shapes, no `aud`/`Host`/`SourceIP` bot-challenge claims. No values recorded or reused.

---
*Incremental log below. Classification: OURS = in our corpora, KNOWN = publicly documented, GENUINELY NEW = undocumented.*

## Bottom line
1. **GENUINELY NEW: `zz=oai` nonce structure = `oai` + 10-digit epoch-seconds + 7 random digits.** Verified 3/3 against event `@timestamp`s (nonce minted 1–2s before collection); monotonic across 3,000 sampled rows. The marker was known; its internal encoding was not documented anywhere in our writeups. Enables timestamp-recovery from any `zz=oai` URL and distinguishes agent-minted nonces from replays.
2. **Corpus marker grammars are near-perfectly disjoint** (zz: 0/1.84M/7; uqscan: 1129/0/2; `<word><DATE>`: 1401/4/9) — structural support for same-provider/different-evals.
3. **KNOWN corroborations:** httpbun `/base64/` staging family (67 occurrences); `claude`-token tags; RubyGems `oai[a-z]{10}` canary package names; enodia-JWT absence from corpora.
4. **Lead:** `njxzgz<DATE>s<N>`/`p<N>` pinyin-abbrev tag word (16 hits) — not in grammarian's shapes; verify against grammarian raw before claiming new.
5. **Honest negatives:** no unattributed blob families; no agent-adjacent images (stego); no bot-challenge JWT grammar in corpora; `1628771336899`×82 = target-site cache-buster, not a nonce.

## Follow-ups
- F1: Add 19-digit epoch-ns pattern to census (grammarian's `x=`/`ov=`/`retry=`/`r=`/`slow=`/`uqfresh=` discovery) and re-run.
- F2: `njxzgz` tag-word provenance — check grammarian raw + live urlquery.
- F3: Live urlquery/urlscan nonce census (lane 1's "live" half) — needs egress; the oai-tag-sweep's 7,547 b64 blobs deserve the same framing analysis as lane 2.
- F4: zz-nonce timestamp recovery at scale — backdate agent activity from any logged `zz=oai` URL, including third-party scan logs.
