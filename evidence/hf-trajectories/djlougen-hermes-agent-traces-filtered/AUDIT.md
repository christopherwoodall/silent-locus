# Audit: DJLougen/hermes-agent-traces-filtered

- Source: `https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered` (raw under `raw/djlougen-hermes-agent-traces-filtered/`, provenance in `raw/djlougen-hermes-agent-traces-filtered/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: `data/train.jsonl` (83MB), 3,679 hermes-agent function-calling traces (quality-filtered subset of the lambda parent set). Cross-lane note: this is the hermes-agent population tied to the July hermes-agent cert burst.
- Method: full-file text scan (raw bytes, tolerant of embedded newlines) for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline; marker grammar hunt. Sharp-pattern grep (`captcha|turnstile|cloudflare|prove you are human|verify you are human|are you a robot|bot-check|webhook.site|ntfy.sh|httpbun|\boai[:-_]` + context review): **zero real hits**.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean. 256 broad-regex bypass hits are all code contexts; zero anti-bot encounters, zero challenge-solved strings. All 16 marker-grammar candidates are byte-verified false positives. (OBSERVED)

## Evidence

- 4 text files scanned; 256 bypass-flag hits, 0 challenge-solved hits, 0 sharp bypass hits (0/256).
- Distinct-context dedup of the 256: `rateLimiter.js` filenames, rate-limiting code the agent writes, `web.Response(status=403)` in CORS middleware code, and `403|`-style line numbers in file-view tool output. No site challenge encountered anywhere. (OBSERVED)

## Marker grammar — all killed (OBSERVED)

| candidate | byte context | verdict |
|---|---|---|
| `B423792362860`, `B676838000028`, `b5824186768fb`... | substrings of long hex blobs (binary dumps inside trajectories), e.g. `...A2DB04CA67001082AA6BEBEBFC606002321DACBC19E03087AA08B6768380000282FBAC0B8C...` | FP_HEX_BLOB, not Amap POI grammar |
| `northflank` | git branch name `remotes/origin/docs/northflank-deploy-guide` in a branch listing | benign doc branch, not the task-oai-NNN fleet lead |
| `Probe.js` | `DataLengthProbe.js`, `Crc32Probe.js` in jszip `node_modules` file listings | FP — library filenames, not the probe.js injection family |
| `oai-assignment`, `oai-history-bot` (6 lines) | Microsoft prompt-engineering course filenames in `git status` output: `new file: 04-prompt-engineering-fundamentals/python/oai-assignment.ipynb`, `06-text-generation-apps/python/oai-history-bot.py` | FP — course filenames, not oai* tag grammar |
| `zz=` params, webhook.site/ntfy.sh/httpbun, task-oai-NNN | zero | — |

## Verdict: **CLEAN**
