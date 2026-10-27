# Verification — Fleet C (Cohere Qwen enrichment)

Verifier only. No commit, no push, no git staging, no Factum write, no trace or benchmark code executed. All re-fetching and hashing done 2026-10-27 (UTC) by the verifier.

Overall verdict: **VERIFIED-WITH-GAPS**

Core bytes, hashes, counts, lead pages, and corpus spot-checks reproduce. The gaps are a missing per-file sidecar set in the corpus raw dir and small location-offset inconsistencies in the entity files. Neither gap changes a headline value.

## 1. Re-download of the three dataset files — PASS

Re-downloaded with `curl -L` from `https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces/resolve/028b7cd7d931586dbfa05463903be9d45c4924ac/` (README.md, qwen-investigation.jsonl, data/train-00000-of-00001.parquet).

| File | Re-download sha256 | Worker sidecar | Match |
|---|---|---|---|
| README.md | 0e88e066b78d184d37b8fc708a72b4df9def4d105321a76e660759af8d291e8b | linguist + cryptologist sidecars, same value | yes |
| qwen-investigation.jsonl | 7110edee1203a58c8dea3b0e3f0a18a86fa42515a655b7b1901a7dda0278d1e6 | linguist + cryptologist sidecars, same value | yes |
| data/train-00000-of-00001.parquet | f8c4b224d7d45aabf8b817ed4a85d2dd58c2d239c8cf6ba78ce42c7ecfa61e8b | linguist + cryptologist sidecars, same value | yes |

The corpus raw copies hash to the same three values, even though the corpus dir has no per-file sidecars (see Check 2).

## 2. Raw-capture provenance + sidecar verification — FAIL (partial: corpus gap only)

- linguist: 4 data files, each with `.PROVENANCE.txt` + `.sha256`; `sha256sum -c` — all 4 OK.
- cryptologist: 4 data files, each with `.PROVENANCE.txt` + `.sha256`; `sha256sum -c` — all 4 OK.
- leads: 9 data files, each with `.PROVENANCE.txt` + `.sha256`; `sha256sum -c` — all 9 OK.
- corpus: FAIL on the literal criterion. Files present are `PROVENANCE.md`, `README.md`, `cohere-blog.html`, `cohere-blog.txt`, `qwen-investigation.jsonl`, `train-00000-of-00001.parquet` — zero per-file `.PROVENANCE.txt` and zero `.sha256` sidecars. Mitigation: the consolidated `PROVENANCE.md` lists all three dataset hashes and the blog hash, and every listed hash matches the actual bytes verified in Check 1 and below (corpus blog sha256 `ced73ad8ae446372806565fcc119682ae802af3b3dcb3eee7a37d7d35e75413c`).

Note, not a failure: the four blog captures are not byte-identical. Linguist and cryptologist captures are 474,274 bytes and differ at byte 277,080 (dynamic page content); corpus and leads captures are 474,286 bytes. Each capture verifies against its own sidecar where a sidecar exists, so provenance is intact; the difference is capture-time page variation, not tampering.

## 3. Recounts and entity spot-checks — PASS-WITH-GAPS

Counts:

- `entities-linguist.json`: 142 entities. Every row carries `source_file` + `source_location` (+ `byte_offset`). Missing: 0.
- `entities-cryptologist.json`: 193 entities (`total` field 193; type counts sum to 193: BUCKET 13, COMMAND 6, DATASET_ID 2, DOMAIN 46, ENDPOINT 1, FILE_PATH 6, FLAG_SEQUENCE 5, IP 4, MODEL_ID 2, OSS_REGION 6, TOKEN_PATTERN 27, TOOL_CALL 13, URL 62). Every row carries at least one `occurrences[]` entry with `source_file` + `location`. Rows with empty occurrences: 0.
- `ioc-list.md`: 125 bullet rows — URLs 62, DOMAINs 46, BUCKETs 13, IPs 4.

Spot-checks (at least 10 rows per entity file, against raw bytes):

- Linguist first 10 rows: 7 byte offsets match the value exactly at the stated offset. 3 host rows (ling-008 cohere.com, ling-009 huggingface.co, ling-010 router.huggingface.co) have offsets pointing at the start of the enclosing URL, so the bare host sits at offset+8. Full non-parquet audit: 79 exact, 45 near (value present within 16 bytes of the stated offset, same host-from-URL convention), 0 missing.
- Sanmaohe PUT URL `http://sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin`: present in the JSONL (1-indexed line 4; URL starts at byte 11538, host at byte 11545) and in the parquet trace string (URL starts at char 9432, host at char 9439; trace length 9,569 chars, 1 row, 3 columns — matches the corpus notes). Linguist rows ling-064/ling-065/ling-090 record these consistently.
- Routify URL: `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com` occurs in the README (18 matching lines by grep); cryptologist routify URL/domain rows and the first 10 cryptologist URL rows are all verbatim in the README bytes.

Gaps:

- Cryptologist sanmaohe JSONL occurrence says "line 3, byte offset 11536". The file's sanmaohe URL is on 1-indexed line 4 (0-indexed line 3), URL start byte 11538, host start byte 11545. The cited byte offset is off by 2 from the URL start and 9 from the host start.
- Cryptologist parquet char offset 9432 for the sanmaohe host is the URL start, not the host start (9439). Same host-from-URL offset convention as the linguist near-misses. Values are correct; offsets need the convention stated or corrected.

## 4. Blog fetch and lead-verdict spot-checks — PASS

- Blog present with provenance in all four raw dirs: linguist, cryptologist, leads (`00-cohere-blog.html`, provenance records HTTP 200, 474,286 bytes), and corpus (via `PROVENANCE.md`, hash verified above).
- Lead 1 (Hacker News, corroborated): confirmed against `01-hn-49379079.html`. Title "Qwen3.8 Fetches Weird URLs", a routify-file-proxy-sg URL, and the "16 times" count are all in the fetched page text. The verdict's caveat (no comments in the fetched page) matches the provenance note.
- Lead 4 (Reddit, unfetchable): confirmed against `04-reddit-1wxvt41.html`. The fetched body is a JavaScript shell with no thread text. Its provenance records HTTP 200 for the shell plus two unsaved attempts (old Reddit and the JSON endpoint, both HTTP 403 with a network-policy block). The UNVERIFIED (UNFETCHABLE) verdict is supported; it does not claim the blog is wrong.

## 5. Corpus overlap spot-checks (read-only) — PASS

Factum `status` at check time reproduced the notes exactly: 208,342 records, commit `2a7d4a74d1f5187281a3bc1ac96f87410e29326a`, not stale. No Factum write was made; only `status` and `match --text … --mode fuzzy --limit 20` were run.

| Query | Returned / strict-verbatim | Notes claim | Result |
|---|---|---|---|
| `169.254.169.254` | 15 / 2 | 15 / 2, ids `observation_c0a353921ee544b4a2e9c59f7a838223` (swarmtraces-hf-dataset, infra.ioc, IMDS note, record_count 5) and `observation_1f302f823f064d2fbbdfee92aed310dc` (paste-linuxiarz transcript) | reproduced exactly |
| `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com` | 1 / 0 | 1 / 0, clean-novel headline value | reproduced |
| `sanmaohe.oss-cn-beijing.aliyuncs.com` | 6 / 0 | 6 / 0, clean-novel | reproduced |
| `PROBE_PAYLOAD_ABC123` (extra clean-novel check) | 3 / 0 | 3 / 0 | reproduced |

Limitation carried from the notes: fuzzy top-20 cap means NO-HIT is strong but not proof of corpus-wide absence; the notes state this themselves.

## 6. Symlinks, secrets, git scope — PASS (with scope note)

- Symlinks under `data/lanes/cohere-qwen-enrichment/`: 0.
- Secret-pattern scan over `reports/cohere-qwen-enrichment/drafts/` (GitHub/PAT, `sk-`, AWS AKIA, Slack/1Password-style tokens, private-key headers, quoted api-key/password values): no matches. Only parameter names appear in prose (e.g. Expires/OSSAccessKeyId named as parameter names, no values) — not value-shaped secrets.
- Git scope: the enrichment trees are wholly untracked (`?? reports/cohere-qwen-enrichment/`, `?? data/lanes/cohere-qwen-enrichment/`); nothing under them is staged. The verifier staged, committed, and pushed nothing. The wider repo `git status` shows pre-existing staged/modified/untracked entries from other workers (1,094 lines total); the verifier did not touch any of them, and the verifier's only repo write is this file under `reports/cohere-qwen-enrichment/drafts/verifier/`.
- No files outside the enrichment dirs were modified by the verifier; all scratch went to `/tmp/verifier-c/`.
- Out-of-scope observation (not verified): `reports/cohere-qwen-enrichment/drafts/adversarial/review.md` exists but was not in the assigned material list; it was only covered by the secret-pattern grep above.

## Verdict

**VERIFIED-WITH-GAPS.** Use the drafts, but close the gaps first: (1) add per-file `.PROVENANCE.txt` + `.sha256` sidecars to `raw/corpus/` (or record the consolidated-PROVENANCE exception); (2) state or fix the host-from-URL offset convention and correct the cryptologist sanmaohe JSONL location to 1-indexed line 4 / URL byte 11538 / host byte 11545.
