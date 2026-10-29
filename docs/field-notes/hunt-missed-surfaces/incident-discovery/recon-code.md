# RECON: novel n-grams in public code (2026-10-03)

Scout: lay-of-the-land sweep for the n-grams nobody else has published, in public code corpora.
Date: 2026-10-03 ~18:35 CDT. Read-only.

## Venues
- **Sourcegraph** (`sourcegraph.com/.api/search/stream`, `context:global`, unauthenticated) — WORKED. All 11 terms queried; every query logged to `/tmp/sg-*.txt` (query log at `/tmp/sg-queries.log`).
- **grep.app** — BLOCKED. All requests 429, then Vercel Security Checkpoint for our egress IP. Unusable from this VM without a browser route.
- **searchcode.com** — BLOCKED (returns non-JSON/HTML, likely bot-gated).

## Per-term verdicts (Sourcegraph, content matches, forks+archived excluded)

| term | matches | verdict |
|---|---|---|
| `zzbulk` | 92 | CLEAN — every line is `FuzzBulk` (cncf-fuzzing Go fuzz tests, civitai buzz helpers). Zero `zzbulk<digits>` grammar. |
| `prepnonce` | 3 | CLEAN — one repo only: `polycrypt/polycrypt`, `prepNonce()` JS in a web3 wallet signin page. camelCase coincidence; no `prepnonce<digits>` grammar anywhere. |
| `wbdisable` | 393 | CLEAN — `MwbDisable…` (PowerToys GPO), `EwbDisableMouseWheelFix` (Delphi EmbeddedWB). Substring coincidences. |
| `arqcb` | 461 | CLEAN — GameCube `ARQPostRequest` callbacks in bfbb/decomp projects. Coincidence. |
| `LINKINJECT` | 382 | CLEAN — `LinkInjection` classes (tempest-framework PHP highlighter, containernet fault injectors). No standalone marker usage. |
| `PHPTEST` | 9,449 | CLEAN — PHPUnit test classes named `PHPTest`. |
| `GOLINK` | 10,000 | CLEAN — `GoLink` OBD2 hardware library (`FuzzyLuke/OBD2Kit`), Go tooling. No probe-marker usage. |
| `tok=expt` | 2 | CLEAN — `EXPT_PER_TOK` in huggingface triton-kernels (experts-per-token). Different token arrangement; no `tok=expt` literal. |
| `OAI_META_1312` | 0 | CLEAN — zero hits. |
| `?fresh=x` / `?fresh=` | 8 | CLEAN — legitimate `?fresh=1` cache-busters in test files (pinokio, VoiceStudio, kaapana, nodus, prismical). None with our `?fresh=x<epoch>.<random>` nonce grammar. |
| `AgentSECCountyLinker` | 0 | CLEAN — zero hits. |

## Read
Nothing surprising turned up — and that is the finding. The probe-marker family (`LINKINJECT`/`PHPTEST`/`GOLINK`) and the arquivo fuzz grammar (`zzbulk`, `prepnonce`, `wbdisable`, `arqcb`) exist in public code ONLY as unrelated identifiers; their agent-toolkit grammar forms (`zzbulk<digits>`, `?fresh=x<epoch>.<random>`, standalone marker labels) have zero public-code presence. `OAI_META_1312` and `AgentSECCountyLinker` are our most novel strings — if either ever appears in public code, that is a fresh find worth chasing.

Nearest miss: `prepnonce`'s only public-code home is one crypto wallet's `prepNonce()` function — a coincidence, but it means the lowercase `prepnonce<digits>` form is genuinely unattested outside our corpus.

## Venue notes for future sweeps
- grep.app needs a browser route (Vercel checkpoint). Retry later or via live browser.
- Sourcegraph unauthenticated streaming API works fine from this VM (~30s/query, polite pacing).
- Re-run `OAI_META_1312` / `AgentSECCountyLinker` periodically as standing watch terms — cheapest possible new-find tripwire.
