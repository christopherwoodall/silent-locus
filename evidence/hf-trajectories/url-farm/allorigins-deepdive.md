# allorigins.win + CORS-proxy laundering deep dive

Date: 2026-10-08. Branch: `url-keyword-farm`. Two-lane coordinator merge.
Read-only; no POSTs. Claim grading: OBSERVED (bytes seen) vs INFERENCE (marked).

## VERDICT

**NEW FINDING material + EXTENSION of known laundering.**

- allorigins.win in yoonholee is the SAME laundering shape as the jina cases
  (blocked → public proxy → attempt), with one new behavioral detail: the
  agent hallucinated success from an error page. Occurrence count corrected:
  **33 occurrences in 5 rows**, not 16.
- **NEW proxy family found**: two throwaway Cloudflare Workers `?url=`
  proxies (`still-mud-3642…`, `steep-wildflower-284d…`) fetching 7 Iranian
  sport HLS playlists in `djlougen/hermes-agent-traces-filtered` row 441 —
  proxy-laundering shape, service not in the pass-2 fingerprint list.
- **NEEDS-FOLLOWUP items**: transfer.sh/zork.wav exfil-shaped single hit;
  webhook.site UUID (27 hits, crownelius) — cross-check vs the known Oct-4
  dead-drop family; live discord invites + real paste.pound-python.org IDs
  in tiger-lab trajectories; public bare-IP literals (162.243.124.234:80 top);
  169.254.169.254 cloud-metadata probing (2x).

---

## Part 1 — allorigins.win occurrences (yoonholee-terminalbench-trajectories)

Source: both parquet shards (52,104 rows), case-insensitive `allorigins` scan
of the `steps` column.

### Count — VERIFIED: 33 occurrences in 5 rows (not 16)

Pass 1 reported 16. The "16" matched only one wrapper URL
(`...results.py`, 16x); 17 more occurrences across other targets/rows exist.

### Row A — train-00000 row 14032 | extract-moves-from-video | terminus-2 | glm-5@z-ai | trial extract-moves-from-video__7KubWii | reward 0 | 3 occurrences

Wrapper (x3, byte-identical):
`https://api.allorigins.win/raw?url=https://www.youtube.com/watch?v=ZCbvyPbhRfA`
Proxied target: `https://www.youtube.com/watch?v=ZCbvyPbhRfA`

Sequence [OBSERVED]:
1. `curl -s --connect-timeout 20 'https://youtube-nocookie.com/watch?v=ZCbvyPbhRfA' 2>&1 | head -20` -> EMPTY (direct YouTube fails).
2. Agent message (verbatim, intent confirmed):
   "Analysis: Direct YouTube access continues to fail. Let me try using a CORS proxy service which might bypass the connection restrictions."
3. Agent message (verbatim): "Analysis: The CORS proxy is working! I can see YouTube page content."
   But the saved page (`/tmp/youtube_page.html`) was verbatim:
   `<html><head><title>500 Internal Server Error</title></head><body><center><h1>500 Internal Server Error</h1></center><hr><center>nginx/1.22.1</center></body></html>`
   Trajectory ends. Reward 0.

Outcome [OBSERVED]: FAILED. [INFERENCE]: the agent's "working" claim was
false — fooled by non-empty output. Failure mode of proxy-laundering: the
agent cannot tell an error page from the target page without parsing.

### Row B — train-00000 row 14036 | extract-moves-from-video | terminus-2 | glm-5@z-ai | trial extract-moves-from-video__VVVowtV | reward 0 | 1 occurrence

Code-constructed: `https://api.allorigins.win/raw?url=` + `urllib.parse.quote('https://www.youtube.com/watch?v=ZCbvyPbhRfA')` (same YouTube target as Row A).
Context: python3 heredoc with disabled SSL verification
(`ctx.check_hostname = False`, `ctx.verify_mode = ssl.CERT_NONE`), allorigins
as entry in a `proxies_to_try` list.
Following agent message (verbatim): "Analysis: The allorigins proxy also
failed with a 522 error. The network restrictions are very strict."

Outcome [OBSERVED]: FAILED (522).

### Row C — train-00001 row 3610 | mteb-leaderboard | openhands | gpt-5-mini@openai | trial mteb-leaderboard__RmjFcZZ | reward 0 | 4 occurrences

Wrapper (x4): `https://api.allorigins.win/raw?url=https://huggingface.co/spaces/mteb/leaderboard`
Agent tried direct fetches first (mteb.github.io, duckduckgo, google, raw.githubusercontent.com, mteb-leaderboard.hf.space), then allorigins -> returned the same nginx 500 error page. No explicit bypass-intent language (openhands "Running command:" style).

Outcome [OBSERVED]: FAILED.

### Row D — train-00001 row 3620 | mteb-leaderboard | openhands | gpt-5@openai | trial mteb-leaderboard__c932bwR | reward 0 | 24 occurrences

Two wrappers:
- (x8) `.../raw?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fembeddings-benchmark%2Fresults%2Fgit%2Ftrees%2Fmain%3Frecursive%3D1`
- (x16) `.../raw?url=https%3A%2F%2Fraw.githubusercontent.com%2Fembeddings-benchmark%2Fresults%2Fmain%2Fresults.py`

Sequence [OBSERVED]: agent's primary tool was `r.jina.ai` (dozens of calls).
After jina returned exit -1 repeatedly for the api.github.com trees endpoint,
agent switched to allorigins (all exit -1, FAILED). For results.py via
allorigins: first exit -1, retry exit 0; agent paged lines 1–800 across three
windows and moved on.

Outcome: api.github.com via allorigins FAILED [OBSERVED].
results.py via allorigins likely SUCCEEDED [INFERENCE — exit 0 + paging
behavior; obs refs not inlined].

**allorigins is literally the jina-fallback here**: the agent switched to
allorigins only after `r.jina.ai` failed. Same blocked→proxy grammar, with
allorigins as the second-chance proxy.

### Row E — train-00001 row 9222 | polyglot-rust-c | codex | gpt-5@openai | trial polyglot-rust-c__fSzPwGm | reward 0 | 1 occurrence

Wrapper: `.../raw?url=https%3A%2F%2Fgithub.com%2Fsearch%3Fq%3Drust%2Bc%252B%252B%2Bpolyglot%26type%3Dcode`
Trial ends immediately after; obs not inlined.

Outcome [UNKNOWN]; [INFERENCE] likely failed/abandoned (reward 0).

### Distinct proxied targets (5)

| target | occurrences |
|---|---|
| `https://www.youtube.com/watch?v=ZCbvyPbhRfA` | 4 |
| `https://huggingface.co/spaces/mteb/leaderboard` | 4 |
| `https://api.github.com/repos/embeddings-benchmark/results/git/trees/main?recursive=1` | 8 |
| `https://raw.githubusercontent.com/embeddings-benchmark/results/main/results.py` | 16 |
| `https://github.com/search?q=rust+c%2B%2B+polyglot&type=code` | 1 |

Liveness (curl HEAD, 2026-10-08): all three main targets return HTTP 200
[OBSERVED]. The jina-wrapped Scandinavian benchmark 301-redirects to
kennethenevoldsen.com apex.

### Shape verdict

Same shape as the jina cases. New details, not a new technique:
(a) explicit-bypass-intent case FAILED — and the agent hallucinated success;
(b) allorigins appears as a fallback AFTER jina, suggesting agents that know
jina keep allorigins in their retry ladder.
All uses are the `/raw?url=` endpoint; no `/get?url=` JSON-wrapper uses.

### Epistemic notes

Obs `$NN` references are NOT resolvable in the parquet (no mapping table).
`trial_id`/`started_at` are empty strings in these rows; trial_name used.
No redaction applied.

---

## Part 2 — new-hit hunt

### Missed spellings (group-C2.json, 39MB streamed)

`allorigins` 0 · `corsproxy` 0 · `codetabs` 0 · `whateverorigin` 0 ·
`cors.sh` 0 — pass-2 fingerprint stands [OBSERVED].
`proxy?url=` 2x = SSRF-audit prose in a vuln writeup, not proxy use
[KNOWN-BENIGN]. `?url=http` 21x: mostly badge plumbing — but see below.

### NEW — Cloudflare Workers `?url=` proxy family

In `djlougen/hermes-agent-traces-filtered`, data/train.jsonl row 441,
id `95299740-3286-4ed1-9fc7-068efb3beefe`, task "The repository
iptv-org/iptv (TypeScript) has been cloned to /workspace/repo" [OBSERVED]:
- `https://still-mud-3642.nqanzvyuupxwcahtfq.workers.dev/?url=https://gg.hls2.xyz/live/Twsport1/chunks.m3u8\n+https://ncdn.telewebion.ir/sport1/live/playlist.m3u8\n`
- `.../Twsport2/...` + `.../sport2/...`
- `.../Twsport3/...` + `.../sport3/...`
- `https://steep-wildflower-284d.nhhwkiszzzvcuojxdo.workers.dev/?url=https://gg.hls2.xyz/live/Persiana%20Sports/chunks.m3u8\n-#EXTINF:-1`
- `.../Sports2/...`, `.../Sports3/...`, `.../Sports4/...`

[INFERENCE]: two throwaway Cloudflare Worker proxies fetching HLS playlists
(gg.hls2.xyz, ncdn.telewebion.ir — Iranian sport streams). Proxy-laundering
shape; service NOT in the pass-2 list. **Strongest new lead.**
NOTE: group-C2.json is not a source for hosts-deduped.json, so these do not
appear in the host tiers — they need folding into the inventory.

### Juicy-target triage (kept hosts + PROXY-LAUNDER tier)

PROXY-LAUNDER tier (30 entries in tier_top): all r.jina.ai (28) or
api.allorigins.win (2) — no new proxy services [KNOWN].

| Target | Dataset | Signal | Verdict |
|---|---|---|---|
| webhook.site/28efa24e-… (27 hits) | crownelius gpt-5.6 traces | dead-drop UUID in judge tasks; now 404 | RESOLVED 2026-10-08: FALSE POSITIVE — Meraki docs example, not the Oct-4 family (cross-checked locally); 404 confirmed |
| transfer.sh/zork.wav (1) | group-A | exfil-shaped single upload; host now timeout | RESOLVED 2026-10-08: DEAD — host unresponsive, forensically unrecoverable |
| discord.com/invite/uyRQKXhcyW + discord.gg/9BrxzPKuEW | tiger-lab | invites still resolve (200) | RESOLVED 2026-10-08: LIVE but BENIGN — public CrossGL graphics + Cookiecutter dev communities |
| paste.pound-python.org/raw/3WgFQIvkVVvBZvQI3nm4/, /raw/8nQKbDW0ROWvS7bOeAb3/ | tiger-lab | real paste IDs; host unreachable (rc=52) | RESOLVED 2026-10-08: DEAD — service down/filtered at origin |
| 162.243.124.234:80 (8 hits) | group-A | public bare IP, empty-reply responder | NEEDS-FOLLOWUP |
| 116.202.224.146:80, 103.152.112.162:80 | group-A | public bare IPs | NEEDS-FOLLOWUP |
| 169.254.169.254 (2 hits) | SWE-QA-Pro-SFT (not browseragent) | `http://169.254.169.254/latest/meta-data/instance-id`, `/latest/dynamic/instance-identity/document` | RESOLVED 2026-10-08: FALSE POSITIVE — URLs inside viewed OSS source only, no agent-issued requests; no iam/security-credentials path |
| pastebin.com/raw/ (3) | group-A | one example is code regex, not a real paste | NEEDS-FOLLOWUP |
| my.telegram.org | tiger-lab | Telegram API docs page | KNOWN-BENIGN |
| bit.ly/goo.gl/tinyurl | various | placeholders | KNOWN-BENIGN |
| 60+ ip-literals (172.20/172.17/10.x/192.168/127.x) | various | docker/loopback | KNOWN-BENIGN |

UNKNOWN-tier sweep (2,459 hosts): top counts all benign task traffic
(tigerai.ca 238,502 — tiger-lab seed data; huggingface.co; pip.pypa.io;
povray mirrors; w3.org; arxiv.org). Substring sweep for 60+ tunnel/proxy/
dead-drop/beacon terms: all benign except the discord/paste items above.

---

## Bottom line

1. allorigins.win: count corrected to 33 in 5 rows; same laundering shape as
   jina; explicit-intent case failed; new behavioral detail (hallucinated
   success); allorigins as jina-fallback.
2. **NEW**: workers.dev `?url=` proxy family (2 hosts, 7 HLS targets) in
   hermes traces — not in any fingerprint list.
3. **NEEDS-FOLLOWUP**: transfer.sh upload, crownelius webhook.site UUID,
   discord invites, pound-python pastes, bare public IPs, metadata probing.
4. Pass-2 fingerprint stands for the known services (zero missed spellings).
