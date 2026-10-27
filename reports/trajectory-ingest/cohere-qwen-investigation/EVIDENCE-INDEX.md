# Evidence index: Cohere Qwen investigation

Every key citation in REPORT.md maps to a file, a location inside it, and a grade. Lane id `lane_28e9347bbc3544c384f4a582b8bc918f` is coordinator-supplied from the Factum `lane new` output (2026-10-27T05:43Z), not raw-observed.
Hashes are SHA-256 of the downloaded bytes. Sidecars live beside each file.

## Lane raw files

| File | Bytes | SHA-256 | Provenance sidecar |
|---|---|---|---|
| `data/lanes/cohere-qwen-investigation/raw/cohere-blog.html` | 474,286 | e4b4afa2815a91cc26d5f6182d78e461e094db4ceb9b231b9b9244d2c85203c4 | `cohere-blog.html.PROVENANCE.txt` |
| `data/lanes/cohere-qwen-investigation/raw/README.md` | 15,020 | 0e88e066b78d184d37b8fc708a72b4df9def4d105321a76e660759af8d291e8b | `README.md.PROVENANCE.txt` |
| `data/lanes/cohere-qwen-investigation/raw/qwen-investigation.jsonl` | 11,758 | 7110edee1203a58c8dea3b0e3f0a18a86fa42515a655b7b1901a7dda0278d1e6 | `qwen-investigation.jsonl.PROVENANCE.txt` |
| `data/lanes/cohere-qwen-investigation/raw/train-00000-of-00001.parquet` | 11,945 | f8c4b224d7d45aabf8b817ed4a85d2dd58c2d239c8cf6ba78ce42c7ecfa61e8b | `train-00000-of-00001.parquet.PROVENANCE.txt` |

## Citation map

| Report claim | File and location | Grade |
|---|---|---|
| PUT probe command, full shell block | jsonl line 4, `export-message-2`, `export-call-0` | OBSERVED |
| `sanmaohe` present (1 occurrence) | jsonl line 4 | OBSERVED |
| `PROBE_PAYLOAD_ABC123` present (1 occurrence) | jsonl line 4 | OBSERVED |
| Thinking block says no tool calls, then tool call follows | jsonl line 4, thinking block + toolCall in same message | OBSERVED sequence |
| Empty assistant text, no detection rule | jsonl line 4 vs line 3 (user task) | OBSERVED sequence |
| Prior-turn reference absent from file | jsonl lines 1–4 (no prior assistant message) | OBSERVED reference; INFERENCE on invention |
| `169.254` absent from trace | jsonl, full-file grep, 0 hits | OBSERVED absence |
| `routify` absent from trace | jsonl, full-file grep, 0 hits | OBSERVED absence |
| `unshare` absent from trace | jsonl, full-file grep, 0 hits | OBSERVED absence |
| Session header origin claim (cfahlgren1, cb30f9f3) | jsonl line 1, `source` object | OBSERVED as a header claim |
| Export time 2026-10-26T23:52:49Z; original time unknown | jsonl line 1 | OBSERVED; export time is not event time |
| Defanged URL `hXXp://...test.bin*` | Blog HTML, "What Cohere's sandbox caught" | OBSERVED (blog) |
| Rate <1 in 100,000; clean re-run gives correct rule | Blog HTML, same section | UPSTREAM |
| Prior sightings (Aug HN, Sept project, Oct Reddit) | Blog HTML, "Others have seen pieces" | UPSTREAM |
| Prefill table (4%→92%, 0.5%→23%, routify count 42) | Blog HTML, "How we found the trigger" | UPSTREAM; denominator not stated in the blog text checked, so percentages are publisher claims, not recomputed here |
| Payload entropy 3.68 bits per character, marker-like form | Cryptologist review, encoding analysis of `PROBE_PAYLOAD_ABC123` | OBSERVED form; canary function INFERENCE |
| Host grammar `<bucket>.oss-<region>.aliyuncs.com`, bucket `sanmaohe`, region `cn-beijing` | Cryptologist review, host-structure analysis | OBSERVED string parse; bucket ownership not established |
| Dedup scan: incident strings absent from `data/records/` | Cryptologist review, dedup table; coordinator Factum fuzzy checks | OBSERVED absence by grep + fuzzy checks; fuzzy "found" hits were substring noise with zero value-field hits |
| Sandbox blocking / no-route-out claim | Blog HTML, "What Cohere's sandbox caught" | UPSTREAM; no tool result in trace |
| Trace-hash indicator `c2f61152…e769b98` | jsonl line 1, `trace_sha256` field | OBSERVED as a header claim; not verified against parquet bytes |
| Metadata address 23–36% of completions | Blog HTML, prefill section | UPSTREAM |
| QEMU test, turns 77–79, `unshare -Urm` | Blog HTML, "Root, sort of" | UPSTREAM |
| 113,000+ derivatives; routify in 4 publishers' builds | Blog HTML, "Backdoor or sloppy plumbing?" | UPSTREAM |
| 64 repro samples; routify full host, 18 mentions | README.md, sample list | OBSERVED bytes; not the trace event |
| Signed-like sample 63, truncated | README.md, sample 63 | OBSERVED bytes; full URL not observed, do not reconstruct |
| Metadata-style sample `100.100.100.200/latest/meta-data/` | README.md, samples 5 and 57 | OBSERVED bytes; cloud mapping INFERENCE |
| Parquet byte strings (sanmaohe, PROBE_PAYLOAD, aliyuncs once each) | Parquet file, plain-byte grep | OBSERVED bytes; not a token decode |

## Factum records

- Lane: `cohere-qwen-investigation`, lane id `lane_28e9347bbc3544c384f4a582b8bc918f`.
- Batch id: `34a02248bf6d43888e76d2335e5e2039`. Batch dir: `data/records/34a02248bf6d43888e76d2335e5e2039/`. Records hash: `f98a64d054d1f7e38e3be2d08c61693ac96c64575432369a7dd3eeac22ef7a93`.
- Every record carries `tags.lane = cohere-qwen-investigation`.
- Run: `run_937d919ff0724212aa563de7c77af9c0`.
- Sources: `source_eb0a1718b9794088b271a0f1a97cdf7a` (blog), `source_46948237c79a4e6992ea139389455329` (dataset).
- Observations: `observation_166e51eb9cc646c4af75c05e4a17dbac` (blog capture), `observation_a9139bf7282340bba2c32f2e5287c078` (dataset snapshot), `observation_db9b488b5d85418cb67bf24722baddf8` (tool sequence), `observation_ffb47d6320aa4edd96aa309c92406302` (sanmaohe host), `observation_8b29989e0fdd47e5a92a0b106ce7df8b` (sanmaohe URL), `observation_57674aeddfaf453e975c1d7e4519158a` (probe payload), `observation_e5b50966645c48218289d5ee43c9b61c` (local path `/tmp/put_probe`), `observation_95360bfabdaf475ca77c20bf4c03a16f` (routify host, README samples, status candidate).
- Claims: `claim_bbcc0b37da3544788a028ec70a399048` (probe attempt, OBSERVED), `claim_e3a8d3583e734bc2bb86e04cc936dde6` (reasoning mismatch, OBSERVED), `claim_4c77e80b79e445d9b37164d8cd9be8ba` (prefill trigger, UPSTREAM), `claim_d467b1b614d34c7f976a92958bd2f889` (metadata probing, UPSTREAM), `claim_c2ee3ac8bbf044fa8fd64d3931787b4b` (namespace escape, UPSTREAM), `claim_b8cf519b35874a6e915ab877de891b67` (revision mismatch, OBSERVED).
