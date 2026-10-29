# API-key reconciliation — rubygems-goimport-campaign — 2026-09-27

## Final numbers (independent census, this report)

- **Gems scanned:** 458 on-disk `.gem` files (608-pin harvest still running;
  fixtures `json-3.0.2`, `thor-1.5.0`, `oai-1.3.0` excluded). Re-run on completion.
- **54 gem-versions** carry full-length API keys: `rubygems_` + exactly 48 hex
  chars (57-char keys). Zero truncated/partial matches.
- **25 distinct key prefixes** (12-hex, unambiguous — verified no 6→12 collisions).
- **Key location:** 51 via gemspec text in `metadata.gz`; 3 via data files
  (`londonyardtestabc-0.0.2` gem.gemspec, `southfetchprobe42-0.0.3` lib/out.rb,
  `southlondonfetchroot-0.1.0` p.gemspec).
- **39 gem-versions** reference the bare POST-target push endpoint
  (`https://rubygems.org/api/v1/gems`, regex negative-lookahead excluding the
  `…/gems/<name>.yaml` go-import import prefix) — the true fetcher-builder tier.
- **12 reuse clusters** (10, 7, 5, 3, 3, 3, 3, 2, 2, 2, 2, 2 gems) + 13 singleton keys.
- **Multi-key gem:** `zzsouthrunnerb-1.0.0` carries 4 distinct keys.
- **Key rotation:** `lambfetchx548811-0.0.1` and `lambfetchx550961-0.0.1`
  assign the hardcoded key to `oldkey`, then GET a fresh key from
  `https://rubygems.org/api/v1/api_key.yaml` (authorized with the old key)
  before pushing. Hardcoded keys are bootstrap fallbacks — revocation alone
  will not stop a live operator; account-level action is required.
- 16 key-carrying gem-versions show no push-endpoint reference in this scan
  (key present in metadata, push code not detected — possibly dead code or
  split-string construction); 1 gem (`designfetchdemo-0.0.1`) references the
  push endpoint with no hardcoded key.
- All non-key `rubygems_*` strings in the corpus are the benign
  `rubygems_version` gemspec field — no alternate key formats.

## Method

Python `tarfile` over every `.gem`: gunzip `metadata.gz`, recurse
`data.tar.gz` members, regex `rubygems_[0-9a-f]{48}` on raw bytes (encoding-agnostic).
Second pass with `rubygems_[0-9a-zA-Z_\-]{1,80}` to catch non-conforming
formats — none found beyond `rubygems_version`. Prefixes recorded at 12 hex
chars; only redacted prefixes leave the workstation — full values never
reproduced in any report. Key validity never tested (live auth attempt —
out of scope).

## Audit trail (the whiplash, in order)

1. **Deep-dive** (`notes/gem-contents-deepdive-2026-09-27.md`): reported
   "~26 runner gems / 21 API keys". Directionally correct, undercounted; real
   pitfall it flagged (import-prefix vs push-endpoint confusion) is genuine.
2. **Runner-hunt** (`notes/gem-runner-hunt-2026-09-27.md` §0): "3 keys, 18
   confabulated". **Wrong.** Its byte scan covered extracted data files but
   missed the gemspec text inside `metadata.gz` — its 3 hits are exactly the
   3 data-file key carriers. Retracted in §0a; audit trail preserved in place.
3. **Keyword sweep** (`notes/gem-keywords-2026-09-27.md` §1): census found the
   `metadata.gz` keys — 44 gem-versions / ~23 prefixes on 427 gems (time-boxed,
   partial triage).
4. **This reconciliation**: 54 gem-versions / 25 prefixes on 458 gems. The
   keyword sweep's delta (+10 versions, +2 prefixes) is explained by harvest
   growth (427 → 458) plus its 15-minute triage box. Current ground truth.

## Files changed in this pass

- `notes/gem-runner-hunt-2026-09-27.md`: §0a reconciliation block added; §1
  no-reuse note marked superseded.
- `notes/gem-contents-deepdive-2026-09-27.md`: retraction banner updated —
  the "18 confabulated" retraction is withdrawn.
- `notes/gem-apikey-disclosure-2026-09-27.md`: **rebuilt** — 25 redacted
  prefixes, full gem membership, 12 reuse clusters, rotation finding,
  account-level (not key-only) recommendation.
- `data/gem-iocs-2026-09-27.md` (334 rows): no per-key rows exist (keys are
  disclosure material, not IOCs — correct); the push-endpoint URL row's
  `report_count` corrected 3 → 39 with rewritten context distinguishing the
  bare POST target from the import prefix.
- `notes/gem-deaddrops-2026-09-27.md`: terminology note updated ("verified
  3-gem uploader tier" → 39-version fetcher-builder tier / 54 key-carriers).

## Open items

- Re-run census on the full 608-pin harvest.
- The disclosure package is rebuilt and ready; sending it to RubyGems
  security is Christopher's call (standing offer).
