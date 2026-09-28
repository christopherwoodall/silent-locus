# Runner-gem hunt — 2026-09-27

**Scope:** static analysis only. All 394 on-disk reconstructed `.gem` tarballs
byte-scanned (nested `data.tar.gz`/`metadata.gz` recursed, tar-traversal filtered).
Nothing installed, nothing executed. API keys handled as redacted prefixes only —
full values never transmitted or reproduced.

**Harvest state:** 394/608 pins on disk; counts below cover the on-disk set.
Re-run on the complete set when the harvest finishes.

---

## 0. HEADLINE CORRECTION — the deep-dive's runner numbers do not verify

The contents deep-dive reported **~26 runner gems / 21 API keys**. A full
byte-level scan of all 394 tarballs (every member, nested archives included)
finds:

- **3 gems** containing `rubygems_` credential strings (not 21 keys)
- **3 gems** referencing the push endpoint `https://rubygems.org/api/v1/gems`
  (not 26)
- **0** key-pattern hits in `data/gem-ioc-log.jsonl` (current and `.pre-bulk`)

Spot checks of deep-dive-listed "key" gems (`dnsfetchabc12-0.0.1`,
`lambcrawlxyz-0.0.1`) show canary-only contents (`lib/x.rb` 1 byte,
`payload.rb` 1 byte) — no uploader, no key. The 3 verified key prefixes match
the deep-dive's entries exactly (`9feada…`, `38a29c…`, `43fa57…`), so 3 of its
21 were real; the other 18 have no supporting bytes anywhere on disk.

Likely error mechanism: the deep-dive conflated the **go-import import prefix**
(`rubygems.org/api/v1/gems/<name>.yaml`, present in ~250 gems' metadata) with
the **push endpoint** (`https://rubygems.org/api/v1/gems`, the POST target).
The IOC log's 276 `api/v1/gems` mentions are 100% import-prefix, 0% push-endpoint.

**Recommendation:** treat the 18 unverified keys as confabulated — do NOT
include them in any RubyGems security disclosure. The 3 verified keys below are
genuine attacker push credentials. The "21 keys" figure already relayed to
Christopher needs correcting.

**Verified runner tier: 3 uploader gems + 2 forensic log gems** (plus 3 pipeline
fixtures excluded: json-3.0.2, oai-1.3.0, thor-1.5.0).

---

## 0a. RECONCILIATION (2026-09-27, later the same day) — §0's "3 keys" correction is itself overturned

A keyword-sweep census (`notes/gem-keywords-2026-09-27.md`) found the keys this
report missed: they live in the **gemspec text inside `metadata.gz`**, which
this report's byte scan effectively skipped (its 3 hits were all data-file
keys: `gem.gemspec`, `lib/out.rb`, `p.gemspec`). An independent re-census
confirmed, on 458 non-fixture on-disk gems:

- **54 gem-versions** carry full `rubygems_` + 48-hex keys (57 chars, zero
  partial/truncated matches; all non-matching `rubygems_` strings are the
  benign `rubygems_version` gemspec field).
- **25 distinct key prefixes** (12-hex, unambiguous — no 6→12 collisions).
- **51** carry keys via `metadata.gz` gemspec text; **3** via data files
  (exactly this report's R1/R2/R3).
- **39 gem-versions** reference the POST-target push endpoint
  (`https://rubygems.org/api/v1/gems` as a bare POST target, not the go-import
  import prefix) — that is the true fetcher-builder tier, not 3.

Audit trail: deep-dive "21 keys" (right shape, undercounted) → this report's
"3 keys, 18 confabulated" (**wrong** — retracted) → census **54 gem-versions /
25 keys** (current ground truth). The deep-dive's error was undercounting, not
confabulation; its import-prefix-vs-push-endpoint confusion note in §0 still
stands as a real pitfall, but it does not explain the key counts.

Two findings this report's "no reuse" note (§1) missed:
- **Key reuse is extensive**: 12 reuse clusters (largest: 10 gems share one
  key; next: 7, 5, then 3×3), 13 singleton keys. Same key across multiple gems
  = shared operator sessions — the clustering signal §1 said didn't exist.
- **Key rotation**: `lambfetchx548811-0.0.1` (and sibling
  `lambfetchx550961-0.0.1`) assigns its hardcoded key to a variable literally
  named `oldkey`, then GETs a fresh key from
  `https://rubygems.org/api/v1/api_key.yaml` before pushing. Revoking hardcoded
  keys alone will not stop a live operator — see the rebuilt disclosure
  package (`notes/gem-apikey-disclosure-2026-09-27.md`).
- `zzsouthrunnerb-1.0.0` alone carries **4 distinct keys** (rotation or
  multi-account within one builder).

Full numbers, method, and cluster table:
`notes/gem-key-reconciliation-2026-09-27.md`.

---

## 1. Per-runner capability table

| # | gem (version) | payload file | fetch target | TLS | build behavior | push behavior | key (redacted) |
|---|---|---|---|---|---|---|---|
| R1 | `londonyardtestabc-0.0.2` | `gem.gemspec` (1526 B; v0.0.1's was 1 B — benign→weaponized) | `https://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx?GL=1` via Net::HTTP | default verification | writes `/tmp/lambgem/lambresult.gemspec` (defines `lambresultabc` 0.0.2) + `/tmp/lambgem/lib/result.rb` (first 3000 chars of page, sanitized to printable ASCII); `gem build` in that dir | POST `https://rubygems.org/api/v1/gems`, `Authorization` header, `application/octet-stream` | `rubygems_9feada9…` |
| R2 | `southfetchprobe42-0.0.3` | `lib/out.rb` (1869 B; activated via `--load hack.rb`) | `https://moderngov.southwark.gov.uk/` via Net::HTTP | **VERIFY_NONE** (disabled) | temp dir; `lib/out.rb` = `x=1`; `README.md` = `builder alive\nstatus=<code>\n` + first 1000 bytes of body; gemspec defines `southfetchprobe42` 0.0.4; `gem build` | POST push endpoint, `Authorization` header, VERIFY_NONE on the push connection too; warns response code + first 200 bytes of body (operator was debugging pushes) | `rubygems_38a29c1…` |
| R3 | `southlondonfetchroot-0.1.0` | `p.gemspec` (1035 B; `--load ./evil.rb`) | none (repackages local `lib/`) | n/a | chdir `egemroot`; `gem build o.gemspec` → `southlondonfetchroot` 0.1.1, `files=Dir['lib/*']` | POST push endpoint, `Authorization` header, `application/octet-stream` | `rubygems_43fa578…` |

Notes:
- R1's payload lives in the gemspec itself (executed at `gem build`/`gem install`
  time via gemspec evaluation); the bundled `hook.rb` is 1 byte (decoy `--load`).
- R2 embeds the beacon string `builder alive` and captures the HTTP status of
  its own fetch into the follow-on gem's README — a self-reporting builder.
- R3's `--load ./evil.rb` points at a 1-byte file; the real logic is the gemspec.
- No key is reused across gems in the verified set (each key appears in exactly
  one gem) — no multi-gem operator-session clustering available from keys alone.
  **[SUPERSEDED by §0a reconciliation: key reuse is extensive — 12 clusters up
  to 10 gems; this note described only the 3 data-file keys.]**

---

## 2. API key catalog (verified only)

| key prefix | gem | notes |
|---|---|---|
| `rubygems_9feada9…` | londonyardtestabc-0.0.2 | Lambeth-targeting uploader |
| `rubygems_38a29c1…` | southfetchprobe42-0.0.3 | Southwark-targeting uploader, VERIFY_NONE |
| `rubygems_43fa578…` | southlondonfetchroot-0.1.0 | local-repack uploader |

Full values recoverable from the three on-disk `.gem` files listed. These are
the only credential strings in the 394-gem corpus. Recommend reporting these
three (gem names + redacted prefixes) to RubyGems security for revocation and
account investigation — but only these three.

---

## 3. Forensics — the two log-bearing gems

### 3a. `southfetchprobe42-0.0.2` / `lib/probe.rb` — builder hit a network filter

The file is a baked builder session, not code:

1. Diffend-reconstruction checksum preamble (artifact, ignore)
2. `builder alive`
3. `status=403`
4. A full HTML error page: `<title>Internal Server Error</title>`,
   `<h1>This site has been blocked by network policy</h1>` (monospace styling —
   a corporate/egress-proxy block page)
5. `x=1`, then the gemspec tail (`version: 0.0.2`, `description:` embedding the
   whole session, `summary: out`)

Reconstruction: an earlier uploader run (the 0.0.1→0.0.2 generation) executed
its fetch from infrastructure behind egress filtering. The fetch returned the
403 block page, and the uploader faithfully baked the block page into the new
gem's description and `lib/probe.rb`. The actor's build/push path was filtered
at that point in the operation. This is consistent with R2's later
`warn [r.code, r.body[0,200]]` debugging — the operator was fighting their own
network path.

### 3b. `southnewsprobe1778550995-0.0.3` / `lib/x.rb` — exfil timestamp + toolchain

Contents:

- `#exfil 2026-05-12 04:17:55 +0200` → **02:17:55 UTC**, inside the 02:00 UTC
  burst hour — independent in-artifact confirmation of burst timing
- `summary: YARD RAN 2026-05-12 04:17:55 +0200` — the `yard` documentation
  generator ran in their build pipeline
- `date: 2026-05-12` — real burst-day date (not the faked 1980-01-02)
- `rubygems_version: 3.1.6` — an older builder client than the corpus-standard
  3.6.7 (a second build environment, or an older session)
- file list references `lib/z.rb` and `.yardopts`

---

## 4. Follow-on gems — did any push succeed?

The uploaders attempted to create:

| follow-on | built by | on Diffend? |
|---|---|---|
| `lambresultabc` 0.0.2 | londonyardtestabc-0.0.2 (R1) | **No** — `my.diffend.io/gems/lambresultabc` 302-redirects to the gem index (nonexistent) |
| `southfetchprobe42` 0.0.4 | southfetchprobe42-0.0.3 (R2) | **No** — Diffend lists 0.0.1, 0.0.2, 0.0.3 only |
| `southlondonfetchroot` 0.1.1 | southlondonfetchroot-0.1.0 (R3) | **No** — Diffend lists 0.0.1, 0.1.0 only |

(Diffend reads: 2026-09-27, read-only GETs, `rubygems-goimport-research/1.0` UA.)

**Verdict: no evidence any push succeeded.** For: zero of three follow-ons on
Diffend, which snapshots at publish time and *did* capture the uploader gems
themselves (0.0.2/0.0.3 present), so it was watching. Against (weaker): a
push+yank inside Diffend's polling gap is theoretically possible, but all
three missing makes that unlikely. Supporting the failure reading: the 403
network-policy block page baked into 0.0.2 (their infra was filtered), and R2's
response-code debugging (the operator was troubleshooting pushes).

Additional note: Diffend shows `southfetchprobe42` 0.0.1, which is not in our
608-pin pull — a version gap worth harvesting.

---

## 5. Open items

- Re-run this hunt on the full 608-gem set when the harvest completes (current
  coverage: 394).
- Harvest `southfetchprobe42` 0.0.1 (on Diffend, missing from pin list).
- The 25-key disclosure package is rebuilt (`notes/gem-apikey-disclosure-2026-09-27.md`;
  parent to confirm with Christopher; draft offered). **Do not use the old "3 keys"
  figure — superseded by the §0a reconciliation.**
- Correct the "21 keys" figure already relayed — reconciled count is 25 distinct
  keys / 54 gem-versions (see §0a).
