# RubyGems security disclosure package — rubygems-goimport-campaign — 2026-09-27 (rebuilt)

> **STATUS: DISCONTINUED — NOT SENT (2026-09-27, Christopher).** The campaign is
> publicly documented ("GemStuffer": Socket 2026-05-13, Nightingale Collective /
> rubyhack.ai 2026-09-11). RubyGems yanked 500+ packages, halted registrations
> May 12–16, and disclosed the Fastly cache issue (GHSA-9j48-x3c3-mrp2) itself.
> This is known info — no disclosure sent, none needed. Package retained for
> provenance only.

**Status: REBUILT on full credential census.** An earlier version of this package
reported 3 keys; that figure came from a byte scan that missed keys embedded in
the gemspec text inside `metadata.gz`. Census (2026-09-27, 458 non-fixture
on-disk gems, regex `rubygems_[0-9a-f]{48}` over decompressed `metadata.gz` +
all `data.tar.gz` members): **54 gem-versions carry full 57-char keys;
25 distinct key prefixes; 12 reuse clusters.** Full audit trail:
`notes/gem-key-reconciliation-2026-09-27.md`. Redacted prefixes only below —
full values never leave the analyst workstation (recoverable from the listed
`.gem` files under `data/raw/gems/`).

## Key-reuse clusters (redacted 12-hex prefixes)

| redacted prefix | gem-versions | n |
|---|---|---|
| `rubygems_9feada919f2f…` | councilfetchfff-0.0.1, lambeth71b-0.0.1, lambyard17-0.0.2, lambyardcal-0.0.1, londonyardtestabc-0.0.2, qwandfetch1-0.0.1, southyardmine1-0.0.1, yard-slnmultifetch-0.0.1, zzsouthrunner-1.0.2, zzsouthrunnerb-1.0.0 | 10 |
| `rubygems_4bb04aa6b8b9…` | dnsfetchabc12-0.0.1, lambcrawlxyz-0.0.2, lambfetchx528211-0.0.1, lambfetchx548811-0.0.1, lambfetchx550961-0.0.1, runnerhack1778553910-0.0.2, zzsouthrunnerb-1.0.0 | 7 |
| `rubygems_0e0f15776713…` | lambfetchjj1-0.0.1, lambyard17-0.0.1, southfetchefefd-0.0.1, southlondonfetchroot-0.0.1, swcalfetcha-0.0.1 | 5 |
| `rubygems_e4eb5a32dd13…` | councilprobexyz-0.0.1, southmqsedwjgw-0.0.1, wandcalentryzz001-0.0.1 | 3 |
| `rubygems_d8e875bd0a97…` | runnerhack1778553910-0.0.1, wandxprobe-0.0.1, zzsouthrunner-1.0.1 | 3 |
| `rubygems_1255ca6cf79b…` | slnfetchroot001-0.0.1, southnews-payload1-35329-0.0.1, southzzscrape-0.0.3 | 3 |
| `rubygems_830e967dd023…` | yard-controllerlambda-0.0.3, yard-runhack-0.0.3, yard-skyfetch-0.0.1 | 3 |
| `rubygems_68e9fe38ddfc…` | lambexploitabc1-0.0.2, lambtmp35293950-0.0.2 | 2 |
| `rubygems_71b27a5375c1…` | lambfetchjj2-0.0.1, wanfetcherx9-0.0.1 | 2 |
| `rubygems_75a85c0edc8c…` | swmeetfetcha-0.0.1, zzsouthrunnerb-1.0.0 | 2 |
| `rubygems_004a2ef4cc4f…` | wandzfetch1500929-0.0.1, wandzfetch1500929-0.0.2 | 2 |
| `rubygems_dc7592061cf3…` | zzsouthfetchsimplex-0.0.1, zzsouthfetchtestx-0.0.1 | 2 |

## Singleton keys (one gem-version each)

| redacted prefix | gem-version |
|---|---|
| `rubygems_a9d809658d92…` | civic-lambda-proxy-0.0.1 |
| `rubygems_928cefaecca4…` | fetchrootx1-0.0.1 |
| `rubygems_960ac400714d…` | lambcrawlxyz-0.0.1 |
| `rubygems_b996cb613441…` | lambproxydkz-0.0.1 |
| `rubygems_8cb9d02bd8ed…` | probeextwand-0.0.1 |
| `rubygems_7af4aa22f105…` | slfetchxyz-0.0.2 |
| `rubygems_478d77217be0…` | slhackprobe999-0.0.1 |
| `rubygems_38a29c1d6231…` | southfetchprobe42-0.0.3 |
| `rubygems_43fa578f03b5…` | southlondonfetchroot-0.1.0 |
| `rubygems_899a08ae773d…` | wandcabfetchfix21736-0.0.1 |
| `rubygems_b676646e208b…` | wandhackmy-0.0.2 |
| `rubygems_06298634eeb0…` | wandsfetchzzabc-0.0.2 |
| `rubygems_94343e985074…` | zzsouthrunnerb-1.0.0 |

**Multi-key gem:** `zzsouthrunnerb-1.0.0` carries 4 distinct keys
(`4bb04a…`, `75a85c…`, `94343e…`, `9feada…`) — rotation or multi-account in one
builder. Key location: 51 gem-versions carry keys in `metadata.gz` gemspec
text; 3 in data files (`londonyardtestabc-0.0.2` gem.gemspec,
`southfetchprobe42-0.0.3` lib/out.rb, `southlondonfetchroot-0.1.0` p.gemspec).

## CRITICAL: key rotation — revocation alone is insufficient

`lambfetchx548811-0.0.1` (and sibling `lambfetchx550961-0.0.1`) contain builder
code that assigns the hardcoded key to a variable literally named `oldkey`,
then **GETs a fresh API key from `https://rubygems.org/api/v1/api_key.yaml`**
(authenticated with the old key) and pushes with the fresh key. The operator
rotates keys programmatically; any hardcoded key is a fallback bootstrap.
**Recommendation is account-level action** (suspend/investigate the owning
account(s)), not just per-key revocation — a live operator can mint new keys.

## Campaign context for the RubyGems security team

- Publishing burst: 2026-05-11 → 2026-05-12, ~555 gems / 608 versions; all
  observed versions yanked. Payloads: `<meta name="go-import">` tags in gem
  summary/description pointing Go tooling at UK council calendar sites.
- Fetcher-builder tier: 39 gem-versions reference the POST-target push endpoint
  (`https://rubygems.org/api/v1/gems`); 54 carry push keys.
- Follow-on gems the uploaders tried to create (`lambresultabc` 0.0.2,
  `southfetchprobe42` 0.0.4, `southlondonfetchroot` 0.1.1): not observed on
  Diffend — no evidence any recursive push succeeded.
- Benign→weaponized versioning (`londonyardtestabc` 0.0.1 → 0.0.2) as a
  review-evasion pattern.

## Recommended actions for RubyGems security

1. **Account-level:** identify the account(s) owning these 25 keys from the
   publishing burst (2026-05-11 → 2026-05-12); suspend and investigate. Key
   revocation alone will not stop the operator (see rotation note above).
2. Revoke all 25 API keys (full values recoverable from the listed gems).
3. Audit `api/v1/api_key.yaml` issuance logs for the burst window — the
   rotation code path mints fresh keys server-side.
4. Check whether follow-on gems `lambresultabc` 0.0.2, `southfetchprobe42`
   0.0.4, `southlondonfetchroot` 0.1.1 were ever pushed (our Diffend check:
   not observed).

## What NOT to report

Do not treat victim infrastructure (council calendar domains, FADGI PDF host,
`r.jina.ai`/`s.jina.ai` reader proxies) as attacker-owned.

## Provenance

Gems recovered from Diffend (my.diffend.io) snapshots; yanked from rubygems.org.
Static analysis only; nothing executed; key validity never tested (that would
be a live authentication attempt). Collection: independent analyst pull,
2026-09-27 (NOT part of SwarmTraces). Census covers 458/608 harvested pins —
re-run on completion.
