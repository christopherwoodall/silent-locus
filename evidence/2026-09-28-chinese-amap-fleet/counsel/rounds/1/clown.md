# CLOWN — Round 1: the numbers station that whispers in fragments, and a board that got fuzzed by a gentleman named "probe"

*Chair's note, pre-read: everything below is either bytes I touched or labeled INFERENCE. The jokes are free; the claims are receipted.*

---

## LANE 2 (main): `njxzgz20261004{s,p,f}<0-7>` — provenance: RESOLVED (structurally)

### The bytes (OBSERVED, ours — `data/2026-09-28-chinese-amap-fleet/events.jsonl`)

Twenty-four scans, one Amap POI (`B00190BC3W`), three tight bursts on 2026-10-04, eight workers each, fired out of order like a starting pistol at a footrace:

| phase | tag shape | submitted URL shape | window (UTC) |
|---|---|---|---|
| `p0`–`p7` | `?uqscan=njxzgz20261004p<N>` (query param, server-visible) | `www.amap.com/ssr/place/B00190BC3W?uqscan=…` | 11:43:43–11:43:50 |
| `s0`–`s7` | `?uqscan=njxzgz20261004s<N>` (query param, server-visible) | `www.amap.com/ssr/place/B00190BC3W?uqscan=…` | 11:45:24–11:45:42 |
| `f0`–`f7` | `#njxzgz20261004f<N>` (**fragment — never sent to the server**) | `www.amap.com/place/B00190BC3W#…` | 12:03:35–12:04:38 |

Fire order inside each burst is scrambled (p: 5,4,1,2,7,3,0,6 — not 0–7), which is what eight parallel workers look like, not one polite loop. The f-phase also drops the `/ssr/` path the p/s phases used.

The fragment is not a rumor: urlquery's public report for one f-scan is titled, verbatim, **`Report - www.amap.com/place/B00190BC3W#njxzgz20261004f7`** (report `92559fd4-823a-4307-a58f-d1803e184caf`, read 2026-10-05 — PUBLIC SOURCE). The tag rode the fragment into a third-party scan log that Amap's own servers could never see, because URL fragments are never transmitted over HTTP. Somebody moved the exact same tag content from a server-visible channel to a server-invisible one *mid-campaign*.

Corpus census for context (OBSERVED): 57 tags fleet-wide match `<key><date><letter><digit>` (`claude20261001m1`, `hubeimuseum20261004d1`, `legacytarget20261004p1`, `srh20261004w2`, …); 7 keys carry multiple variant letters. `njxzgz` is the fleet's heavyweight: the only key with three variants, the only `f` variant anywhere, and the only 8-way fan-out. Zero hits in oai-traces (589,972 events) and oai-tag-sweep (96,353) — fleet-local grammar. Web search for `"njxzgz"` returns nothing relevant (PUBLIC SOURCE, honest null).

### Three absurd-but-plausible theories. Two die tonight.

**THEORY 1 — "It's a three-city corridor: 南京–徐州–赣州."** The fleet abbreviates cities per-syllable (`qd`=Qingdao), so `nj-xz-gz` reads as three 2-letter city codes and the fleet was probing a route. *KILLED.* All 24 scans pin the **same single POI** `B00190BC3W` — a corridor probe would touch ≥3 venues, and no other corpus key is a city-code chain (they're all single venues: `hubeimuseum`, `nanshanapi`, `zhenbeibao`). The corridor was a beautiful idea and the bytes shot it in the parking lot.

**THEORY 2 — "It's a random nonce, not pinyin."** *KILLED.* It wears the fleet's `<pinyin><date>` uniform exactly (cf. `qdnewapi20261005a`, `zhenbeibao20261005a`, and the per-syllable-initial convention `qd`/`zbb`/`zju`); a nonce wouldn't correlate 24/24 with one venue; and the cross-corpus nonce families (`zz=oai<17 digits>`) look nothing like it. It's a place-key. **Which place remains UNRESOLVED** — best structural read is per-syllable pinyin initials of a 6-syllable venue name (n-j-x-z-g-z). The expansion is an honest gap, not a guess I'm willing to launder.

**THEORY 3 — "The f-phase is talking to the scan log, not to Amap." (SURVIVES)** Same tag, same POI, but the tag moved from `?uqscan=` (Amap's server logs see it) into `#` (only the *scanner's* log sees it — and urlquery publishes that log). Whether the intent was server-log evasion or just a lazy note-to-self that happens to be server-invisible, the mechanics are identical, and the effect is a dead-drop: **the scanning service's public URL log is the mailbox.** This rhymes with tonight's other dead-drop finds (fresh webhook.site inboxes, the `?r=` nonce family) — the toolkit keeps using third-party logs as infrastructure. INFERENCE built on OBSERVED mechanics; intent labeled as such. **Novelty: GENUINELY NEW** (fragment-as-covert-channel in this corpus; provenance was UNRESOLVED per the task brief).

### Follow-up (LOGGED, not fetched — for a browser-capable persona)

- `https://www.amap.com/place/B00190BC3W` — provenance: corpus note `Submitted: www.amap.com/place/B00190BC3W#njxzgz20261004f4` (events.jsonl). Resolving the POI name cracks the `njxzgz` expansion (Theory 2's surviving gap). **Do not fetch without Chair's word; Amap is the surveilled target's own house.**

---

## LANE 1 (crooked pass): msgboard.dev — the Artist did straight; I did crooked

The Artist's round-1 report already covers the board's census, the Werbel bridge, and the probe fauna straight. I took the absurd hypotheses and beat them against the lobby bytes (`GET /messages?thread=lobby&limit=400&format=json`, read-only, 2026-10-05; returned newest 100 of 321 — window noted, honest).

**ABSURD HYPOTHESIS A — "Message lengths are steganography."** *KILLED, and the corpse is hilarious.* Handle `probe` posted 85 messages on 2026-10-03, and the lengths aren't a code — they're a **boundary-value fuzz**: `A`×2729→2732 (incrementing by one), `A`×4090→4097 (incrementing by one across the 4096 line), round probes at 100/1000/2000/2500/5000/8000/8192, and — the detail that ends the debate — `é` repeated at 4090→4096 **chars** (= 8180→8192 **bytes**), posted back-to-back with the `A`-probes: the agent was determining whether the limit is counted in characters or bytes. It closed with whitespace/escaping probes (`line1 line2\t tab "quoted"`, `lead and trail`, `A    B C`) and literally labeled one payload `extra-probe-marker`. 85 posts in ~4 minutes (12:51–12:55 UTC), a whitespace triplet at 13:53, then silence. OBSERVED / GENUINELY NEW as a byte-level calibration (the Artist logged the species; the char-vs-byte accounting and the labeled marker are mine).

**ABSURD HYPOTHESIS B — "Greeting loops are heartbeats."** *KILLED.* Inter-arrival gaps for `probe` are 0–1 seconds in a single 4-minute session, then nothing — that's a calibration run, not a heartbeat. (The actual heartbeat-shaped phenomenon — `my-agent`'s mutating-name hello loop in `handshake` — is the Artist's find; I don't touch it.)

**What survives, and why it's funny:** an agent that introduced itself to a public board by *fuzzing the board's input validation first* — max length, byte-vs-char accounting, whitespace normalization — before any real agent ever said hello there. QA as first contact. The board's metrology layer isn't emergent behavior; it's some agent's Tuesday afternoon, labeled and timestamped.

Non-probe lobby chatter observed in the same window (names only, no identity work): `Wally (wally-dk24)`, `Grok-4.5-xAI`, `NW001`, `musekey`/`Ekurhive` (a consent-protocol exchange), `arche-codex-manjangilchi`, `wicketwarden` (Lockzone/qevrulan.com), `Kashia` (Muse Mansion). Census only — the Artist owns the sociology.

---

## Scorecard for the Chair

| # | Finding | Evidence | Novelty | Status |
|---|---|---|---|---|
| 1 | njxzgz = 3 configs × 8 workers, 24 scans, one POI, scrambled fire order | OBSERVED (corpus) | GENUINELY NEW | KEEP |
| 2 | f-phase tag moved to URL fragment: server-invisible, scan-log-visible dead-drop | OBSERVED mechanics + PUBLIC SOURCE (report title) / INFERENCE (intent) | GENUINELY NEW | KEEP (Adversary: try to kill the intent reading; the mechanics stand regardless) |
| 3 | Corridor theory (南京–徐州–赣州) | OBSERVED (single-POI refutation) | — | KILLED |
| 4 | Random-nonce theory | OBSERVED (grammar + venue correlation + zero cross-corpus hits) | — | KILLED |
| 5 | njxzgz place expansion (6-syllable pinyin initials) | INFERENCE, unresolved | — | OPEN LEAD (needs POI-name resolution; URL logged, unfetched) |
| 6 | msgboard length-stego hypothesis | OBSERVED (fuzz sweep w/ byte-vs-char probes) | GENUINELY NEW (byte-level detail) | KILLED (as stego); the fuzz itself is the find |
| 7 | msgboard greeting-heartbeat hypothesis | OBSERVED (0–1s gaps, one session) | — | KILLED |

*No installs, no commits, no posts, no probes. The truth is funny; the spreadsheet is funnier.*
