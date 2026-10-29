# Gem contents deep dive — 2026-09-27

> **RECONCILIATION (2026-09-27, later the same day):** the "3 keys" figure below
> is itself overturned. The runner-hunt's byte scan missed keys embedded in the
> gemspec text inside `metadata.gz` (its 3 hits were data-file keys only). An
> independent census of 458 on-disk gems finds **54 gem-versions carrying full
> 57-char keys, 25 distinct prefixes, 12 reuse clusters**, plus a key-rotation
> mechanism (`oldkey` → fresh key via `api/v1/api_key.yaml`). The deep-dive's
> original "21" was directionally correct but undercounted. Full audit trail:
> `notes/gem-key-reconciliation-2026-09-27.md`. The "18 confabulated" retraction
> below is withdrawn — those keys are real.
>
> **CORRECTION (2026-09-27, verified by byte-level re-scan):** the "~26 runner
> gems / 21 API keys" figures in §1 below **do not verify**. A full scan of all
> tarballs found only **3 gems** containing `rubygems_` credential strings and
> **3 gems** referencing the push endpoint — the 21-key count conflated the
> go-import import prefix (`rubygems.org/api/v1/gems/<name>.yaml`, in ~250 gems'
> metadata) with the push endpoint (`https://rubygems.org/api/v1/gems`).
> Verified tier: 3 uploaders / 3 keys — see `notes/gem-runner-hunt-2026-09-27.md`.
> The 18 unverified "keys" are retracted and must not be disclosed. The rest of
> this report (canary tallies, theater files, author/date distributions) stands.

**Scope:** static extraction only. 358 of 362 on-disk reconstructed `.gem` tarballs analyzed
(harvest still running; 608 pins expected total). Never installed, never executed.
Tar member names traversal-filtered; no traversal attempts observed in any gem.

**Pipeline fixtures excluded from campaign tallies:** `json-3.0.2`, `thor-1.5.0`, `oai-1.3.0`
(downloaded during the pipeline test, not campaign gems).

---

## 1. HEADLINE: this is not just a go-import probe campaign

~26 gems carry **active self-replicating uploader scripts**. The campaign has two tiers:

- **Tier 1 (bulk, ~330 gems):** go-import meta-tag injections in summary/description,
  canary file contents (`x=1` / single newline), faked dates. Pure probing.
- **Tier 2 (~26 gems):** Ruby scripts that fetch a UK council modern.gov page over
  HTTPS (SSL verification disabled), package the fetched content into a **new gem**,
  and **POST it to `https://rubygems.org/api/v1/gems`** using hardcoded
  `rubygems_*` API keys. Self-publishing follow-on gems under the attacker's account(s).

**21 distinct hardcoded `rubygems_` API keys** (57 chars each) found across the corpus —
these are attacker push credentials and the highest-value IOCs in this dataset.
Key prefixes (redacted) with gem membership:

| key prefix | in gems |
|---|---|
| `rubygems_4bb04aa6b8b9c…` | dnsfetchabc12, lambcrawlxyz-0.0.2, lambfetchx528211, lambfetchx548811, runnerhack1778553910-0.0.2, zzsouthrunnerb-1.0.0 |
| `rubygems_960ac400714d9…` | lambcrawlxyz-0.0.1 |
| `rubygems_9feada919f2ff…` | lambeth71b, lambyard17-0.0.2, lambyardcal, londonyardtestabc-0.0.2, yard-slnmultifetch, zzsouthrunnerb-1.0.0 |
| `rubygems_0e0f157767130…` | lambfetchjj1, lambyard17-0.0.1, southfetchefefd, southlondonfetchroot-0.0.1 |
| `rubygems_71b27a5375c15…` | lambfetchjj2, wanfetcherx9 |
| `rubygems_b996cb6134413…` | lambproxydkz |
| `rubygems_68e9fe38ddfc6…` | lambtmp35293950-0.0.2 |
| `rubygems_8cb9d02bd8ed0…` | probeextwand |
| `rubygems_d8e875bd0a97e…` | runnerhack1778553910-0.0.1, zzsouthrunner-1.0.1 |
| `rubygems_7af4aa22f1055…` | slfetchxyz-0.0.2 |
| `rubygems_478d77217be0f…` | slhackprobe999 |
| `rubygems_1255ca6cf79b8…` | slnfetchroot001, southnews-payload1-35329, southzzscrape-0.0.3 |
| `rubygems_38a29c1d62317…` | southfetchprobe42-0.0.3 |
| `rubygems_43fa578f03b58…` | southlondonfetchroot-0.1.0 |
| `rubygems_e4eb5a32dd13b…` | wandcalentryzz001 |
| `rubygems_06298634eeb08…` | wandsfetchzzabc-0.0.2 |
| `rubygems_004a2ef4cc4f9…` | wandzfetch1500929-0.0.1, -0.0.2 |
| `rubygems_830e967dd023d…` | yard-controllerlambda-0.0.3, yard-runhack-0.0.3 |
| `rubygems_dc7592061cf36…` | zzsouthfetchtestx |
| `rubygems_94343e9850744…` | zzsouthrunnerb-1.0.0 |
| `rubygems_75a85c0edc8cd…` | zzsouthrunnerb-1.0.0 |

(Full key values recoverable from the listed on-disk `.gem` files under
`data/raw/gems/`. Recommend reporting to RubyGems security for revocation.)

Gems referencing the full push endpoint URL (`https://rubygems.org/api/v1/gems`) — 26:
dnsfetchabc12, lambcrawlxyz-0.0.1, lambeth71b, lambfetchjj1, lambfetchjj2,
lambfetchx528211, lambfetchx548811, lambproxydkz, lambyard17-0.0.1, lambyard17-0.0.2,
lambyardcal-0.0.1, londonyardtestabc-0.0.2, probeextwand, slfetchxyz-0.0.2,
slnfetchroot001, southfetchefefd, southfetchprobe42-0.0.3, southlondonfetchroot-0.0.1,
southlondonfetchroot-0.1.0, southzzscrape-0.0.3, wandcalentryzz001, wandsfetchzzabc-0.0.2,
wanfetcherx9, yard-runhack-0.0.3, yard-slnmultifetch, zzsouthrunnerb-1.0.0
(plus slfetchxyz-0.0.2, southzzscrape-0.0.3, wandxprobe, yard-controllerlambda,
zzsouthrunner-1.0.1 referencing the endpoint without the full Net::HTTP+build pair).

---

## 2. The five substantive non-canary files (full behavioral description)

### 2a. `londonyardtestabc-0.0.2.gem` / `gem.gemspec` (1526 bytes) — ESCALATE
Uploader script (v0.0.1's `gem.gemspec` was 1 byte; the malicious version is 0.0.2 —
classic benign-then-weaponized versioning). Behavior, statically read:
1. HTTPS GET `https://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx?GL=1` (Lambeth council calendar)
2. Writes `/tmp/lambgem/lambresult.gemspec` defining a new gem `lambresultabc` v0.0.2
3. Writes `/tmp/lambgem/lib/result.rb` = first 3000 chars of the fetched page, sanitized to printable ASCII
4. Runs `gem build`, then POSTs the built gem to `https://rubygems.org/api/v1/gems`
   with `Authorization: rubygems_9feada…`
References `--load ./hook.rb` (the bundled `hook.rb` is 1 byte/empty — the payload
lives in `gem.gemspec` itself).

### 2b. `southfetchprobe42-0.0.3.gem` / `lib/out.rb` (1869 bytes) — ESCALATE
Uploader script. Behavior: HTTPS GET `https://moderngov.southwark.gov.uk/` with
`OpenSSL::SSL::VERIFY_NONE`; builds `southfetchprobe42` v0.0.4 in a temp dir with
`lib/out.rb` = `x=1` and `README.md` = fetch result (`"builder alive\nstatus=#{code}\n"` +
first 1000 bytes of body); `gem build`; POST to the push endpoint with
`Authorization: rubygems_38a29c…`. Beacon string `builder alive` embedded.

### 2c. `southlondonfetchroot-0.1.0.gem` / `p.gemspec` (1035 bytes) — ESCALATE
Uploader variant. Behavior: in dir `egemroot`, `gem build o.gemspec`
(spec name `southlondonfetchroot` v0.1.1, `s.files=Dir['lib/*']`), POST to the push
endpoint with `Authorization: rubygems_43fa57…`. References `--load ./evil.rb`.

### 2d. `southfetchprobe42-0.0.2.gem` / `lib/probe.rb` (1655 bytes) — builder session log
Not code — a captured build/operator session: checksums block, `builder alive`,
`status=403`, then an HTML error page **"This site has been blocked by network
policy"**, then `x=1`. The actor's infrastructure hit a network filter (403) at
some point and they pasted/embedded the evidence. Operational artifact.

### 2e. `southnewsprobe1778550995-0.0.3.gem` / `lib/x.rb` (712 bytes) — exfil log
Contains `#exfil 2026-05-12 04:17:55 +0200` and `summary: YARD RAN 2026-05-12 04:17:55 +0200`.
04:17:55 +0200 = **02:17:55 UTC** — inside the 02:00 UTC burst hour, confirming burst
timing from inside the artifact. "YARD RAN" shows the actor ran `yard` (doc generator)
as part of their build pipeline. Also lists `- lib/z.rb`, `- ".yardopts"`.

---

## 3. Canary baseline (everything else)

- **File contents:** the dominant content hash is a single `\n` byte — 446 file instances.
  `x=1` canaries in `lib/x.rb` (100 gems), `lib/a.rb` (66), `lib/test.rb` (47).
- **Provocative names, empty bodies:** `evil.rb` (21 gems), `payload.rb` (7), `hack.rb` (6),
  `lib/inject.rb` (3), `lib/lambproxy.rb` (3), `lib/south.rb` (4), `lib/main.rb` (4),
  `a.txt`, `in.gemspec`, `gem.gemspec` (v0.0.1), `x`, `lib/x` — ALL 1 byte (`\n`).
  The names are theater; the bodies are canaries. (Exception: the three weaponized
  files in §2, where later versions carry the real payload.)
- **Dependencies:** zero across all campaign gems (the only gems with dependencies
  are the `oai`/`thor` fixtures). **Executables:** zero. **Extensions:** one campaign
  gem (`docfetchxyz`, `extensions=['extconf.rb']`) — but `extconf.rb` is 1 byte;
  it's an extension-*field* propagation test, not native code.
- **Authors:** 24 distinct. `x` (165), `a` (70), `z` (20), then `SLN` (14), `DL` (11),
  `oai` (9), `zz` (7), `news`/`me`/`tmp` (3 each), `South`/`xx`/`sln` (2),
  `abc`, `71`, `Hack`, `tester`, `south`, `tmpgeo`, `X` (1 each).
  (Fixture authors Florian Frank / Ed Summers / Yehuda Katz / José Valim excluded.)
- **Dates:** 319 × `1980-01-02 00:00:00Z` (faked). 37 multi-version gems (`*-0.0.2`,
  `-0.0.3`, …) have **no `date:` line at all** — later versions drop the field.
  One gem kept a real date: `extfetchedwand1778555624` → `2026-05-12` (burst day).
- **Gemspec boilerplate:** `required_ruby_version` / `required_rubygems_version`
  `>= 0` on essentially every gem — noise, not signal. `rubygems_version: 3.6.7`
  on most; the exfil-log gem (`southnewsprobe…-0.0.3`) reports **3.1.6** — a
  different/older builder client for that artifact.
- **Distinct file-content hashes:** 160 across the analyzed set (inflated by fixture
  gems' real files — LICENSE/README/extconf sources; campaign-only distinct
  payloads are far fewer: newline, `x=1`, and the §2 files).
- **Tar hygiene:** member names clean across all 358 gems; no absolute paths,
  no `..` segments. `metadata.gz` member in reconstructed gems carries a checksums
  YAML preamble before the spec (Diffend-reconstruction artifact, harmless).

---

## 4. Operational picture from all evidence

1. **Two-tier campaign.** Bulk tier: 500+ go-import metadata probes with canary bodies
   (SSRF/parser probing of Go tooling against UK council calendar sites via r.jina.ai).
   Runner tier: ~26 gems with uploaders that fetch council pages and self-publish
   follow-on gems to RubyGems with hardcoded API keys.
2. **Version-iteration pattern.** `londonyardtestabc`: v0.0.1 benign (1-byte files) →
   v0.0.2 weaponized. `probejiqptzco` has 6 versions. Later versions drop the `date:` field.
3. **Their infra hit filtering.** The `lib/probe.rb` session log shows a 403
   "blocked by network policy" — something in their build/push path got filtered.
4. **Internal timestamp confirms the burst.** `#exfil 2026-05-12 04:17:55 +0200`
   (02:17:55 UTC) sits inside the 02:00 UTC burst hour independently measured from
   Diffend "Last diff" timestamps.
5. **Toolchain fingerprints.** `rubygems_version` 3.6.7 (main builder) vs 3.1.6
   (one artifact); `YARD RAN` shows yard in the pipeline; `builder alive` beacon
   strings; `VERIFY_NONE` SSL in uploaders (their fetch path ignores certs).
6. **Key hygiene is terrible (for them).** 21 distinct push keys committed into
   gems, several reused across gems (`9feada…` in 6 gems, `4bb04aa6…` in 6 gems) —
   suggests multiple builder sessions/accounts or key rotation during the burst.

## 5. Caveats & follow-ups
- Analysis covered 358/362 gems on disk at run time; harvest still running toward 608.
  **Re-run this deep dive on the complete set.**
- Diffend-diff reconstruction can stitch artifacts (checksums headers inside files);
  treat odd file preambles as reconstruction noise unless corroborated.
- Static only — uploader behavior described from code reading, never executed.
- The 21 API keys are attacker credentials: recommend reporting key prefixes +
  uploader gem names to RubyGems security for revocation and account investigation.
- Open: whether any follow-on gems (`lambresultabc`, `southfetchprobe42-0.0.4`,
  `southlondonfetchroot-0.1.1`) were actually published to RubyGems before the yank.
