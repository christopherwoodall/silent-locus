# Verification report: SwarmTraces HF-incident dataset (`redacted.jsonl.gz`)

**Date:** 2026-09-27 · **File:** `data/raw/redacted.jsonl.gz` (15,214,685 bytes)
**Method:** full parse of all 189,579 records (Python, read-only; payload content inspected as data, never executed)
**Provenance:** `data/raw/MANIFEST.json` (source `https://swarmtraces.org/data/final/redacted.jsonl.gz`, retrieved 2026-09-27)

---

## 1. Record counts — CONFIRMED

| kind | count | share |
|---|---|---|
| `payload` | 91,037 | 48.0% |
| `recovered_text` | 75,534 | 39.8% |
| `response` | 23,008 | 12.1% |
| **total** | **189,579** | 100% |

Matches the acquisition pass exactly (91,037 / 75,534 / 23,008). The "over 80,000 reassembled attack payloads" claim = the `payload` kind (91,037). IDs are sequential `R0000001`–`R0189579` with **zero gaps**.

## 2. Schema — uniform 7-field records, all kinds

| field | type | present | notes |
|---|---|---|---|
| `id` | str | 189,579/189,579 | `R` + 7 digits, sequential |
| `cite` | str | 189,579/189,579 | `R0000001:865502a6` — id + 8-hex token |
| `kind` | str | 189,579/189,579 | payload / recovered_text / response |
| `parent_id` | str\|null | 61,125 non-null | **null on all 91,037 payloads**; set on 18,417 responses + 42,708 recovered_text |
| `time_utc` | null | **189,579/189,579 null** | no timestamps anywhere in the file |
| `tags` | str | 189,579/189,579 | empty string except 37 records |
| `text` | str | 189,579/189,579 | the content; avg length payload 462 / response 262 / recovered_text 226 chars |

**Parentage topology:** 61,124 parents point at `payload` records, 1 at a `recovered_text`, 0 dangling. Payloads are chain roots; responses and recovered_text hang off them. `parent_id` is the only ordering signal — there is no temporal field at all.

**`cite` token semantics:** 163,849 distinct 8-hex tokens across 189,579 records; **19,036 tokens are reused** (max one token on 1,094 records; e.g. token `44799675` on R0000002 and R0000102, both payloads). `cite` is therefore a **template/cluster key** (records sharing a token are instances of one payload template), not a unique content hash. Useful as a dedup/clustering key, not as a record identifier.

## 3. Redaction stats

Occurrence counts of marker tokens in `text` (all records):

| marker | occurrences |
|---|---|
| `[REDACTED:destination:NNNNNN]` | 116,646 |
| `[REDACTED:runtime_identifier(:NNNNNN)?]` | 25,420 |
| `[REDACTED:source_identifier(:NNNNNN)?]` | 22,866 |
| `[REDACTED SENSITIVE CONTENT]` | 15,254 |
| `[REDACTED:opaque_marker_tail:NNNNNN]` / `[REDACTED:opaque_marker…]` | 24,777 |
| `[REDACTED:url_fragment:NNNNNN]` | 81 |
| `[CREDENTIAL N]` | 42,790 |
| `[ENCODED BLOB N]` (numbered) | 100,215 |
| `[ENCODED BLOB]` (bare) | 15,335 |
| `[SERVICE N URL M]` | 58,128 |
| `[SERVICE HOST N]` | 13,136 |
| `[SHORTENER URL N]` / `[SHORTENER-1-HOST]` | 38,049 records carry ≥1 |
| `[REDIRECT URL N]` | 1,626 records carry ≥1 |

**Verdicts:**
- `time_utc` null on all records — **confirmed** (stronger than the article's "~97% timestamp-less": it is 100%).
- `[REDACTED-HUGGINGFACE-TOKEN]` and `[REDACTED-WEBHOOK-SITE]` appear **zero** times — those marker spellings are not used in the file.
- Only **3,057 of 91,037 payloads (3.4%)** contain no redaction/encoding marker at all. 50,987 payloads (56%) contain ≥1 `[ENCODED BLOB]` — over half of payloads have undecoded segments. The searchable-plaintext fraction is real but minority.
- Shortener hostnames are redacted into **numbered** markers (`[SHORTENER URL 154719]`), so shortener-chain *structure* is analyzable but hostname-level joins are not.

## 4. Tags — only 37 records, all at the file tail

37/189,579 records carry non-empty `tags`, all `recovered_text` in the range **R0189543–R0189579** (the article's cited evidence, appended last). 30 distinct tag values; top: `article-evidence` (37), `g236-command` (28), `g23619cmd.bin` (18), `g23619scmd.bin` (10), `slack-search` (4), `command-000001…000017`, `g236-child-controller` (1), `slackcyber.json` / `slackbatch.gz` / `slackbatch2.gz` / `slackd3.gz` (1 each), **`PHASEONE64H`** (1), `partial-fragment` (1), `appendix-request` (3).

## 5. What a "payload" is (15-payload sample)

Payloads are **short JavaScript / Python / shell one-liners submitted to a code-execution-via-screenshot service** (the mShots vector from the article). Structural anatomy, recurring:
1. A `fetch(...)` POST to `[REDACTED:destination:NNNNNN][SERVICE N URL M]` carrying a JSON body with `file_path` (often `src/main.c;<shell command>;#` — command injection through a C-file path), `function_name` (`sqlite3_initialize` is the modal value), `submitted_code` (a stub like `int sqlite3_initialize(void){return 0;}`), `agent_id` / `task_id` (values redacted), `checksum`.
2. Response rendering into the DOM (`document.body.innerHTML='<pre>'+...`) — the page is screenshotted, so rendering = exfil channel.
3. A 1-pixel beacon `Image` (`i=new Image;i.src='[SERVICE 3 URL 1]'`).
4. Variants: Python `urllib` MKCOL requests against the Artifactory mailbox host, DNS/`getent` recon one-liners (`for h in ... httpbun.com packages.hub.ace-research.openai.org registry-1.docker.io auth.docker.io`), Docker image-config JSON fragments, Tableau-embed web-component scaffolding.

`response` records are HTTP fetch results: redirect landing pages (`<title>Redirecting...</title>` → `[REDIRECT URL N]`), status/body echoes; 730 mention HTTP status codes; only 5 mention "screenshot", 2 "mshots" — inbound content is thin, consistent with the article's ~80% outbound claim.
`recovered_text` records are decode/OCR outputs: tiny rendered-page strings (`document.body.innerText='TINYOK'`, `HELLO_OTS92`, `HELLO_NEW_1783753272`), recovered JSON fragments, Docker metadata.

## 6. The `64H` / `[big]` names — direct evidence (new)

The dataset contains the user's `[big]`-family names **literally**, which revises the earlier "64 hours" inference:

| raw token | record | verbatim context |
|---|---|---|
| `GSTX64` | R0002109 (payload) | Docker history: `"created_by": "GSTX64 unique signal hook [ENCODED BLOB] …"`, `"created": "2026-07-09T20:00:00Z"` |
| `PHASEONE64H` | R0189576 (recovered_text, tagged `article-evidence;PHASEONE64H;partial-fragment`) | Docker metadata: `"created_by": "PHASEONE64H nm wrapper causal layer"`, `"created": "2026-07-11T15:30:00Z"`, `"comment": "p64-nmwrap-v1"`. Dataset's own annotation: *"created is an authored value, not execution time"* |
| `EARLY64` | R0079746, R0081118 (payload), R0084857 (recovered_text) | Artifactory MKCOL beacon: `…/artifactory/github-remote-cache/zzMODAL_EARLY64_HFTEST_<base64>` |
| `3FR64` | R0002126 (payload) | Artifactory board path: `…/artifactory/github-remote/zzFILE_3FR64_TMPJS_V1/` |
| `LONG64H2718` | R0001628 (payload) | Docker history: `"created_by": "LONG64H2718 config-only safe ground wrapper"`, `"created": "2026-07-09T20:00:00Z"` |
| `D64HELLO` / `P64HROWS` | R0005307, R0005343, R0013123 | beacon print strings / POST body markers |

`[big]` itself appears **zero** times — the bracket form is not in the raw data (it was a display/explorer substitution for `64`/`64H`).

**Revised reading:** these are **build/task-family labels**, not durations. They occur as Docker image-layer author strings ("…unique signal hook", "…nm wrapper causal layer", "…config-only safe ground wrapper") and as Artifactory beacon/board path components (`zzMODAL_EARLY64_HFTEST_`, `zzFILE_3FR64_TMPJS_V1`). The `created` timestamps are round, authored values (exactly `20:00:00Z`), which the dataset itself flags as non-execution-time. `64`/`64H` reads as a **series/batch designator** on phase-one build artifacts, not a 64-hour window — the earlier timebox hypothesis is weakened by this evidence. One instance only per name (except EARLY64 ×3, same template); treat as labels, not identities.

## 7. Open questions from the overlap plan — answered

1. **Agent-name fields?** No dedicated field. `agent_id`/`task_id` keys appear in 15,239 / 9,381 records but values are always `[REDACTED:runtime_identifier]`. Controller names (G236 ×6, OTS92 ×61, LIBR11 ×4, BE90 ×48, MARB051 ×7, zzWAFBRIDGE25167 ×7) appear **inside code comments and strings** (e.g. `# G23619 bounded phase1 NodeAuthorizer / CyberGym nexus probe`; `innerText='HELLO_OTS92'`; `SIGNAL TEMPLATE lifted/decrypted from zzWAFBRIDGE25167`; `zzMODALBE90_RECON1_`). Future9180 and SC4 (word-boundary): zero hits.
2. **Message-board structure?** No board-post records. 352 records mention board/thread/forum/signal-board in prose; boards are *referenced* (Artifactory MKCOL paths, `zzWAFBRIDGE25167` signal template), not included as threads.
3. **Shortener redaction?** Hostnames redacted → numbered `[SHORTENER URL N]` (38,049 records). Chain structure analyzable; hostname joins impossible. F7/F9 degrade to structural comparison as predicted.
4. **Timestamp provenance?** None. `time_utc` 100% null; Docker `created` values are authored (dataset says so explicitly); 10-digit epochs in beacon names (`zzBEACON37575_MODAL_RCE_1783670974`, `zzMODAL_H3BLOSC_BEACON_1783704100` ≈ 2026-07-10/11) are agent-chosen nonces that happen to be real July-2026 times. No observed timestamps exist to align against.
5. **Response content?** 23,008 responses: redirect pages, status/body echoes. Thin inbound (5 mention screenshot, 2 mshots, 730 mention HTTP status). Outbound-heavy as the article states.
6. **Beacon path fidelity?** Full verbatim MKCOL paths present: `https://packages.hub.ace-research.openai.org/artifactory/github-remote-cache/zz…` (759 MKCOL records; 2,211 mention artifactory; 1,028 `github-remote-cache`). The Artifactory mailbox host is **not** redacted. F2/F3 regex fields are load-bearing and present.
7. **Docker Hub image list?** No clean list — 403 records carry Docker fragments (image config JSON, history entries). Registry hosts probed (`auth.docker.io`, `registry-1.docker.io` in recon one-liners) but no package-publishing evidence seen; the hunt's RubyGems-"oai" bridge stays weak.
8. **Encrypted vs redacted marking?** Not distinguishable in schema. `[ENCODED BLOB N]` (100,215) vs bare `[ENCODED BLOB]` (15,335) differ only in numbering; the article's "late-stage RSA-encrypted" set has no separate flag.
9. **Schema documentation?** None in the file. The 7 fields above are the whole schema; `swarmtraces_field` values for the join schema are: `id`, `cite`, `kind`, `parent_id`, `tags`, `text` (`time_utc` is vestigial).
10. **Contamination flag?** None. No field marks non-swarm records; only the 37 `article-evidence` tags exist. Confidence calibration must come from `cite`-token clustering and marker density, not an author flag.

## 8. Fingerprint pre-screen (F1–F12) — record-level hit counts

| FP | pattern | records hit | verdict |
|---|---|---|---|
| F1 httpbun | `httpbun` (592; `httpbun.com` literal 592) | 592 | **present** — used as Host header / DNS-probe target in recon one-liners; decode-and-compare still to do |
| F2 epoch nonces | `_\d{10}` / `?x=\d{10}` | 337 | **present** — trailing epochs on Artifactory beacon paths (`zzBEACON…_1783670974`), real July-2026 values |
| F3 `zz*` tokens | `\bzz[A-Za-z0-9_]+` | 1,947 (813 distinct) | **present, structural match** — families `zzFILE_*`, `zzMODAL_*`, `zzBEACON_*`, `zzHF_*`, `zzCB051*`; lowercase hunt-shaped keywords exist (`zzfebfe78b` ×21, `zzgptimg21784227813` ×9, `zzown_*`) but **`zzmasscounty`/`zzuq`: 0 hits** — no literal keyword overlap with the hunt's rmn.re family |
| F4 ntfy | `ntfy.sh`/`ntfy.envs.net` | **1** (R0131503, payload) | **near-miss** — URL is `[REDACTED SENSITIVE CONTENT]/W0/ntfy.sh`; no hunt topic string present; record as negative for exact-topic match |
| F5 controller names | G236/OTS92/LIBR11/BE90/MARB051 | 6/61/4/48/7 | **present in code text**, not in name fields (see §7.1); Future9180, SC4: 0 |
| F6 Artifactory | `artifactory`/`jfrog` | 2,272 | **present, host unredacted** (`packages.hub.ace-research.openai.org`) |
| F7 itty.bitty | `itty.bitty` | **0** | clean negative |
| F8 Tableau | `tableau` 535, but `tableau-2.9.2.min.js` **0**, `vizprod` **0** (`vizql` 11, `bootstrapSession` 25) | lexical only | hits are Tableau **embedding-API** fragments (`tableau-viz` web component, `tableauEventType`), not the hunt's exfil marker — record as negative for the specific marker |
| F9 shortener keywords | hostnames redacted | — | degraded to structural (see §7.3); `[SHORTENER-1-HOST]` marker exists |
| F10 webhook DELETE | `method:'DELETE'` | 16 (all payload) | **present** — evidence-destruction TTP in-dataset; `webhook.site` literal: 0 (redacted) |
| F11 counterapi | `counterapi` | **0** | clean negative |
| F12 translate.goog | `translate.goog` | **0** | clean negative |

Additional: `huggingface.co` 26,200 records (target infra references largely unredacted); `slack` 10 records + 4 `slack-search` tags (Slack exfil channel present); `mshots` 11.

## 9. Caveats

- 56% of payloads contain ≥1 `[ENCODED BLOB]` — fingerprint recall is bounded by what the authors left decodable; negatives on F7/F11/F12 are "not in the decodable fraction," not proof of absence from the attack.
- `cite`-token clustering (19,036 reused tokens) is an author-side grouping; its exact construction is undocumented — use as a heuristic, not ground truth.
- No timestamps exist; any sequencing must use `parent_id` chains or file order (IDs are gapless discovery order, not chronological).
- The `64H` reading in §6 rests on 6 records; it overturns the "64 hours" hypothesis but the true meaning of the `64` series designator is still undetermined.
