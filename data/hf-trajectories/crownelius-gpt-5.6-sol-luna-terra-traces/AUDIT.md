# Audit: Crownelius/GPT-5.6-Sol-Luna-Terra-Traces

- Source: `https://huggingface.co/datasets/Crownelius/GPT-5.6-Sol-Luna-Terra-Traces` (raw under `raw/crownelius-gpt-5.6-sol-luna-terra-traces/`, provenance in `raw/crownelius-gpt-5.6-sol-luna-terra-traces/PROVENANCE.md`)
- Audited: 2026-10-07
- Rows/files: `data/train.parquet` (297MB), 15,353 rows. Schema: row_hash, first_source_dataset/config/split/row_index, seen_count, row_json (nested coding-agent trace JSON).
- Method: row-group streaming scan (scripts/rg_scan.py) of all text across 3 row groups; sharp-pattern + challenge-solved + marker-grammar regexes; byte-verification of every distinct hit with full context.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

Clean. 8 sharp-pattern hits and 1 dead-drop-pattern hit across 15,353 rows are all byte-verified false positives (docs text, package names, a vendor docs example URL). ~340 `B\d{10}` marker candidates are hex-blob substrings. Zero challenge-solved strings. (OBSERVED)

## Evidence

- 3 row groups scanned; 8 sharp hits, 0 challenge-solved, 1 dead-drop hit — all killed:
  - `cloudflare` x1: `.cloudflared/` directory in a `git status` untracked-files listing (cloudflared tunnel client config dir). (OBSERVED)
  - `Cloudflare`/`CLOUDFLARE` x2: API-key docs table listing `CLOUDFLARE_API_KEY` (+ `CLOUDFLARE_ACCOUNT_ID`) as one provider option among Anthropic/xAI/OpenRouter/Vercel/ZAI — docs text, not a challenge. (OBSERVED)
  - `turnstile` x1: `cpp-turnstile` in a vcpkg-style C++ package list (`cpp-fairride cpp-filterview ... cpp-turnstile ...`) — a package name, not the Cloudflare widget. (OBSERVED)
  - `CAPTCHA` x1: OAuth client docs ("configure the client to supply the authorization header ... rather than relying on its default mechanism"). (OBSERVED)
  - `Captcha` x1: API error-docs example ("E0000165: Domain not verified exception", HTTP 403). (OBSERVED)
  - `captcha` x1: `google-cloud-recaptcha-enterprise` package name in a citation list. (OBSERVED)
  - `cloudflare` x1: NetApp docs page metadata. (OBSERVED)
  - `webhook.site` x1: `https://webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031` inside vendor webhook docs (Meraki-style: placeholder device `QXXX-XXXX-XXXX`, base64 `https://www.example.com/webhooks`, `"sharedSecret":"secret"`) — a docs example callback URL, not agent dead-drop tradecraft. (OBSERVED)

## Marker grammar — all killed (OBSERVED)

- ~340 `B\d{10}[A-Z0-9]{2}` hits: all substrings of hex blobs in trace text. FP_HEX_BLOB.
- `oai*` tags, `zz=` params, task-oai-NNN, northflank, probe.js: zero.

## Verdict: **CLEAN**
