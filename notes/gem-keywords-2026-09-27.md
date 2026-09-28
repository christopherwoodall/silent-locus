# Time-boxed keyword sweep — agent chatter in the gem corpus

Date: 2026-09-27. Time box: ~15 minutes. Corpus: 427 reconstructed gems on disk
(956 extracted text files: .rb/.gemspec/.md/.txt/.yml + all 427 `metadata.gz`
gemspec blobs) + `data/gem-ioc-log.jsonl` metadata fields. Static only, nothing
executed. Fixture gems (json-3.0.2, thor-1.5.0, oai-1.3.0) excluded from all tallies.

Extends `notes/gem-deaddrops-2026-09-27.md` — its finds are cited, not re-listed.

## Battery

- **Tier 1 (discovered voice):** builder, alive, exfil, probe, fetch, prove, safe,
  hook, beacon, status, yard, "get any", warn, "hook err" (+ morphological variants)
- **Tier 2 (generic ops chatter):** TODO, FIXME, NOTE, XXX, HACK, password, passwd,
  secret, token, api_key/apikey, debug, trace, hello, hi, thanks, please, sorry,
  done, failed, success, retry, sleep, wait, check, look, listen

Raw yield: 426 file hits + 249 metadata hits + 16 IOC-log metadata fields →
606 unique candidates after filtering go-import payloads and the 37
already-catalogued dead-drop quotes. Top ~40 reviewed in the time box.

## 1. MAJOR — the credential census overturns the runner-hunt's "3 keys" correction

The runner-hunt (`notes/gem-runner-hunt-2026-09-27.md`) claimed only 3 gems carry
`rubygems_` credential strings and the other 18 deep-dive keys were
"confabulated". Its spot checks looked at extracted *data* files
(`lib/x.rb` = 1 byte → "no key"). **The keys live in the gemspec text embedded
in `metadata.gz`, which the spot checks missed.**

Independent census (this sweep): every `rubygems_` + hex run in all 427
`metadata.gz` blobs and extracted data files, with hex-run lengths measured:

- **44 gem-versions carry full-length keys** — every match is exactly
  `rubygems_` + 48 hex chars (57-char keys, matching the deep-dive's format).
  Zero truncated/partial matches. These are real, complete API keys.
- **~23 distinct key prefixes** across those 44 (6-hex prefixes recorded;
  full values never reproduced — redacted-prefix discipline throughout).
- The deep-dive's "21 keys" was directionally correct; the runner-hunt's
  "3 keys, 18 confabulated" correction does not hold.

**Key-reuse clusters** (same key in multiple gems = shared operator session):

| prefix | gems |
|---|---|
| `9feada…` | councilfetchfff, lambeth71b, lambyard17-0.0.2, lambyardcal, londonyardtestabc-0.0.2, qwandfetch1, southyardmine1, yard-slnmultifetch, zzsouthrunner-1.0.2, zzsouthrunnerb-1.0.0 (~10) |
| `4bb04a…` | dnsfetchabc12, lambcrawlxyz-0.0.2, lambfetchx528211, lambfetchx548811, runnerhack1778553910-0.0.2, zzsouthrunnerb-1.0.0 (~6) |
| `0e0f15…` | lambfetchjj1, lambyard17-0.0.1, southfetchefefd, southlondonfetchroot-0.0.1 (~4) |
| `d8e875…` | runnerhack1778553910-0.0.1, wandxprobe-0.0.1, zzsouthrunner-1.0.1, zzsouthrunnerb-1.0.0 (~4) |
| `e4eb5a…` | councilprobexyz, southmqsedwjgw, wandcalentryzz001 (~3) |
| `1255ca…` | slnfetchroot001, southnews-payload1-35329, southzzscrape (~3) |
| `830e96…` | yard-controllerlambda-0.0.3, yard-runhack-0.0.3, yard-skyfetch-0.0.1 (~3) |
| `dc7592…` | zzsouthfetchsimplex, zzsouthfetchtestx (~2) |
| `71b27a…` | lambfetchjj2, wanfetcherx9 (~2) |
| `004a2e…` | wandzfetch1500929-0.0.1, -0.0.2 (~2) |
| singletons | `a9d809…`, `960ac4…`, `b996cb…`, `68e9fe…`, `8cb9d0…`, `7af4aa…`, `478d77…`, `b67664…`, `062986…`, `75a85c…`, `94343e…`, `38a29c…`, `43fa57…` |

`zzsouthrunnerb-1.0.0` alone carries **4 distinct keys** (`4bb04a…`, `75a85c…`,
`94343e…`, `9feada…`) — key rotation or multi-account within one builder.

**Dynamic key retrieval** — `lambfetchx548811-0.0.1` metadata:
```
# fetch latest API key then immediate upload
oldkey='rubygems_4bb04a…'; keyuri=URI('https://rubygems.org/api/v1/api_key.yaml'); kreq=Net::HTTP::Get.new(keyuri); …
```
The hardcoded key is literally assigned to a variable named `oldkey`, and the
script GETs a fresh key from the API before pushing. **The operator rotates
keys; hardcoded keys are fallbacks.** Revocation alone may not stop a live
operator — the account behind the keys matters more than any single key.

**Implication for the disclosure package:** `notes/gem-apikey-disclosure-2026-09-27.md`
was built on the "3 verified keys" figure — it needs to be rebuilt on this
census (~23 prefixes, reuse map, plus the api_key.yaml rotation note). Flagged
for parent; not rebuilt here (out of time box, and key handling needs care).

## 2. New voice finds (not in the dead-drops report)

Ranked by voice-ness. Verbatim quotes trimmed to 120 chars.

| # | gem-version | location | quote | read |
|---|---|---|---|---|
| 1 | zzsouthrunner-1.0.1 / zzsouthrunnerb-1.0.0 | metadata, comment | `# malicious crawler/exfil for Southwark Jan 2026 docs via rubydoc.info worker` | **Mission + target + infra in one line.** "Malicious" is the operator's own word; target is Southwark Jan-2026 docs; worker infra is rubydoc.info. |
| 2 | zzsouthrunner-1.0.1 / zzsouthrunnerb-1.0.0 | metadata, comment | `# avoid recursive builds repeated pushes; exfil gem only generated if not yet on worker marker? Yard may run twice. duplicate push harmless.` | Ops thinking aloud — idempotency design, worker markers, yard double-run hazard. The `?` is someone reasoning mid-build. |
| 3 | londonyardtestabc-0.0.1 | gemspec line 11 | `warn 'HOOKED!!!!!!'` | New register — exuberant, not workmanlike. Top-level gemspec code: fires on `gem build`/`gem install`. The benign 0.0.1 announces its hook. |
| 4 | wandsfetchzzabc-0.0.2 | metadata (builder script) | `File.write("#{d}/lib/x.rb", "# Hello from yard exploit executed at #{Time.now}\nXDATA='plugin-executed'\n")` | Calls it a **"yard exploit"** outright, timestamps it, sets an `XDATA='plugin-executed'` tripwire in the built gem. |
| 5 | lambfetchx548811-0.0.1 | metadata | `# fetch latest API key then immediate upload` | Key-rotation tradecraft (see §1). |
| 6 | zzsouthrunner-1.0.1 / -1.0.2 | metadata | `# Make exfil gem` → builds gem with `s.summary='cache docs'; s.description='exfil'` | The exfil gem is disguised as `'cache docs'` while its description says `exfil` — camouflage + honesty in the same stanza. |
| 7 | yard-runhack-0.0.3 | metadata | `# package exfil` → builds `yard-runhack-0.0.4` with `s.summary='exfil'` | Same exfil-packaging idiom, yard family. |
| 8 | wandxprobe-0.0.1 | metadata | `exit if File.exist?('/tmp/wandxprobe-done') rescue nil` + `File.write('/tmp/wandxprobe-done','1')` | Run-once lockfile — the probe refuses to run twice. |
| 9 | injecthack1778550335-0.0.1 | metadata | `# create extra file perhaps yard reads?` | Thinking aloud in a comment — genuine uncertainty about the build pipeline. |
| 10 | lambyard17-0.0.1 | metadata | `# Fetch target and self-publish next gem` | Mission comment, self-replication stated plainly. |
| 11 | lambeth71b-0.0.1 | metadata | `# fetch target using direct Net::HTTP` | Implementation note. |
| 12 | lambproxydkz-0.0.1 | metadata | `# lambeth fetch endpoints` | Target-family label. |
| 13 | lambfetchx528211 / lambfetchx548811 | metadata | `File.write('…res/lib/a.rb', '# done')` | Completion marker baked into the built gem — `# done` as a build receipt. |
| 14 | southnewsprobe1778550995-0.0.1 | metadata | `puts 'hello'` | A `hello` in executable code (distinct from the `hello` summary flags). |
| 15 | londonyardtestabc-0.0.1 | metadata | `File.write('lib/out.rb',%Q{# fetched content #{Time.now}\nclass Out; end})` | Timestamped fetch receipt, same idiom as #13. |
| 16 | civic-lambda-proxy-0.0.1 | metadata | `# fetch pages` / `out='Fetched '+Time.now.to_s` | Fetch logging. |

Tier-2 sweep was otherwise quiet: no TODO/FIXME/XXX/HACK/password/secret/thanks/
sorry anywhere in the corpus; `debug`/`trace`/`retry`/`sleep`/`wait`/`check`
hits were all incidental code (config.fetch, Net::HTTP, `status` checks).
No non-English text found.

## 3. Coverage note (time box accounting)

- **Covered:** all 427 on-disk gems — 956 extracted text files grepped with the
  full 40-keyword battery; all 427 `metadata.gz` blobs grepped; IOC-log
  metadata fields (summary/description/authors/email/homepage) swept; 606
  unique candidates triaged, top ~40 read in full.
- **Not covered:** the remaining ~181 pins not yet harvested; full-context
  review of all 606 candidates (long tail is mostly `fetch`/`status`/`probe`
  in builder code); `.yardopts`/dotfiles beyond the battery.
- Fixture gems (json/thor/oai) excluded — their keyword hits are ecosystem noise.

## 4. Read

The voice set keeps growing past the dead-drops report's ~26: the chatter now
spans the whole fetcher-builder tier, and it has **three distinct registers**:
(1) workmanlike ops notes (`# avoid recursive builds…`, `# fetch target using
direct Net::HTTP`), (2) the beacon protocol (`builder alive`, `# done`,
`# fetched content <timestamp>`), and now (3) **candid mission language** —
`# malicious crawler/exfil for Southwark Jan 2026 docs`,
`# Hello from yard exploit`, `# fetch latest API key then immediate upload`.
The operators name what they're doing when they think no one is reading the
gemspec. The single most informative new line is the zzsouthrunner comment:
it gives target (Southwark Jan-2026 docs), method (crawler/exfil), and
infrastructure (rubydoc.info worker) in eleven words.

**Corrections to prior reports:**
- The runner-hunt's "3 keys, 18 confabulated" is overturned by the census
  above — 44 gem-versions, ~23 distinct full-length keys, all 48-hex.
  Recommended: amend `notes/gem-runner-hunt-2026-09-27.md` §0 and rebuild
  the disclosure package on the census + reuse map.
- The IOC agent's `data/gem-iocs-2026-09-27.jsonl` was built on the 3-key
  figure — needs a re-run for key-related rows (it was steered mid-run;
  verify before ingest).

**Caveats:** census is on 427/608 harvested pins — re-run on the complete
set; key *validity* (unrevoked?) not tested and must not be — that would be
a live authentication attempt. Report keys to RubyGems security; let them
validate.
