# Gem dead-drops: agent-to-agent chatter in the rubygems-goimport-campaign corpus

Date: 2026-09-27. Corpus: 408 reconstructed gems (Diffend pull), mined statically — every
`.rb`/`.gemspec`/`.md`/metadata field + version-to-version diffs on 22 multi-version gems.
Fixture gems (json-3.0.2, thor-1.5.0, oai-1.3.0) excluded. Catalogued go-import payloads
excluded — this is everything ELSE with a voice in it.

**TL;DR:** the voice is real but sparse, and it clusters entirely in the ~26-gem
hand-tended set. **Terminology note (2026-09-27, reconciled):** "runner tier" here means
"gems carrying operator voice" (~26) — the credentialed fetcher-builder tier is now
**54 key-carrying gem-versions / 25 distinct keys / 39 with push code**, per
`notes/gem-key-reconciliation-2026-09-27.md` (the earlier "3 uploaders" figure was
a scan-coverage artifact).
The 330 bulk canary gems are mute (single-letter authors, `x=1` bodies, no comments).
The runners talk in three registers: a **beacon protocol** (`builder alive` / `status=<code>`),
**mission comments**, and **accidental ops logs** baked into shipped gems. Metadata
micro-text (`hello`, `safe`, `test meta`) reads as status flags between runs.

---

## 1. The beacon protocol — "builder alive"

A status-beacon convention shared across the runner scripts. The beacon string is embedded
in the *next* gem the runner builds — i.e., the beacon is the dead-drop: each generation
reports its health into the following generation's description/README.

- `southfetchprobe42-0.0.3` / `lib/out.rb:12`
  `data="builder alive\nstatus=#{resp.code}\n"+resp.body[0,1000]`
  → on fetch failure, line 14: `data="builder alive but fetch fail #{e.class} #{e.message}"`
- `southfetchprobe42-0.0.2` / `lib/probe.rb:5-6`
  `builder alive` / `status=403` (then the blocked page body)
- `londonyardtestabc-0.0.2` / `gem.gemspec` (rescue arm)
  `warn "HOOK ERR #{e.inspect}"`
- `southfetchprobe42-0.0.3` / `lib/out.rb:28,30`
  `warn [r.code,r.body[0,200]]` / `warn e.full_message`

**Read:** a heartbeat format — `builder alive` + HTTP status + first 1000 bytes of the
target page, or the exception class on failure. Whoever ran the next stage could read the
previous run's health off the registry without any other channel. The registry *is* the
dead-drop board.

## 2. Mission comments

- `southfetchprobe42-0.0.3` / `lib/out.rb:9`
  `# get any modern gov page to prove`
  → the mission statement, in plain English, inside the uploader. "Prove" what? Read
  against the beacon protocol: prove the fetch-and-republish loop works end to end.
- `southfetchprobe42-0.0.3` / `lib/out.rb:5`
  `# probe`
- `southfetchprobe42-0.0.3` / `lib/out.rb` (heredoc tail)
  `# doc\nmodule Probe;end`
- `londonyardtestabc-0.0.2` / `gem.gemspec`
  `# class dummy`

**Read:** terse operator shorthand. `# get any modern gov page to prove` is the closest
thing to a stated objective anywhere in the corpus.

## 3. Accidental ops logs (the two known specimens, verified verbatim)

**3a. The 403 builder log** — `southfetchprobe42-0.0.2` / `lib/probe.rb`
```
builder alive
status=403

    <!DOCTYPE html>
    ...
        <h1>This site has been blocked by network policy</h1>
    ...
```
The runner fetched its target, got blocked, and its own debug output — beacon + block
page — was baked into the gem's `description` and pushed. Then in 0.0.3, `lib/probe.rb`
was *deleted* and replaced by the new `lib/out.rb` uploader (confirmed by version diff).
**Read:** accident, then cleanup. They noticed the leaked log and rotated the file.

**3b. The exfil/build log** — `southnewsprobe1778550995-0.0.3` / `lib/x.rb:5`
```
#exfil 2026-05-12 04:17:55 +0200
```
plus gemspec fields in the same version: `summary: YARD RAN 2026-05-12 04:17:55 +0200`,
`date: 2026-05-12 00:00:00.000000000 Z` (a REAL date — the only one in the campaign
besides the faked 1980-01-02), `rubygems_version: 3.1.6` (older client; the fleet
standard is 3.6.7).
**Read:** a build-session log. `#exfil` + `YARD RAN` with a +0200 (CEST) timestamp =
02:17:55 UTC, inside the burst hour — independent corroboration of burst timing, and a
timezone hint about the operator's machine. "YARD RAN" puts the `yard` doc tool in their
build pipeline (`.yardopts` files ship in many gems, all empty).

## 4. Status signals in metadata (summary/description as signal flags)

| Text | Where | Read |
|---|---|---|
| `safe` | `goproxylondonx-0.0.5` summary | **Status flag.** Version history: 0.0.1 `test`/`test` → 0.0.4 broken truncated tag (`AA <meta…`) → 0.0.5 full working tag, summary `safe`. They iterated the injection live and marked the good one. |
| `hello` | `sprox-c160-{1,2,3,4}fossil-0.0.1` summary (×4) | Greeting/probe — with `(?-mix:desc)` as description (a Ruby regex literal *as* the description — someone testing what renders) and email `proxyxyzz@mailinator.com`. The whole quad is a rendering probe. |
| `test meta` | `v{4,5,6,7,8}zzgbqvirfx`, `vanity2zzgbqvirfx` summary (×6) | The URL-parser differential battery labeling itself. |
| `Proxy test` / `Proxy test hg` / `Proxy test hg2` | `lamb*proxy*oai`, `oailambproxy1` summary (×8) | The proxy-test family labeling itself, VCS included. |
| `sum` | `zztxtwtmp{02,03,04,05,07}`, `lamhack…`, `zzlambcalx…`, `zztargettest…` summary (×13) | Truncated `summary`? — likely the generator writing the field name as the value. Sloppy templating, a workflow tell. |
| `probe desc` | `southprobe55a1778551356-0.0.1` description | Same templating sloppiness (`description` → `probe desc`). |
| `south fetcher` | `southfetchefefd-0.0.1` summary | Role label. |
| `runner` | `runnerhack1778553910-0.0.1` summary | Role label — and it ships a nested 1-byte `lib/payload.gem` plus empty `inject.rb`/`main.rb`. Theater. |
| `Calendar helper` | `civic-lambda-proxy-0.0.1` summary (author: `research`) | The only "legitimate-sounding" summary in the corpus — camouflage. |
| `demo yard load` | `injecthack1778550335-0.0.1` summary | Yard pipeline reference again. |
| `payload rubydoc test` | `southnews-payload1-35329-0.0.1` summary | RDoc/yard pipeline reference. |
| `integration test` | `southhacks47761-0.0.1` description (email: `south05be40c4@mailinator.com`) | |
| `foo` / `test2` / `test` / `testing` / `fetch` / `entry` / `plugin` / `safe` | various singletons | Filler, but human-typed. |

## 5. Identity play — authors and emails

Bulk authors are single letters (`x` 203, `a` 94, `z` 39…), but the log also shows:
- `' '` (space, 375) and `'-'` (dash, 370) as author names — empty-ish identities, likely
  template defaults that render as blank on the registry page.
- `"'"` (a single quote, 2) as author — a quote-breaking probe smuggled into the author
  field, same spirit as the `(?-mix:desc)` description.
- `tmp` (author, the `sprox-c160` quad), `research` (author, `civic-lambda-proxy`),
  `Hack` (author, `londonprobe1778550281`), `SLN`, `DL`, `zz`, `me`, `xx`, `X`, `news`.
- `proxyxyzz@mailinator.com` (×4, the `sprox-c160` quad) and
  `south05be40c4@mailinator.com` (×1) — mailinator throwaways; the `zz` infix and the
  hex-ish `05be40c4` match the campaign's token grammar.

**Read:** no stable identity anywhere — identities are per-gem throwaways, sometimes
adversarial (`'`, `(?-mix:desc)`), sometimes blank. Consistent with agents, not a human
maintaining a persona.

## 6. Version progressions as signals

- `londonyardtestabc` 0.0.1 → 0.0.2: 0.0.1 is fully benign (empty `hook.rb`, empty
  `lib/a.rb`); 0.0.2 adds `--load ./hook.rb`, the Lambeth fetcher, and the push with a
  hardcoded key. **Benign-then-weaponized** — the 0.0.1 exists to establish the name.
- `goproxylondonx` 0.0.1 → 0.0.4 → 0.0.5: `test` → broken tag → `safe` + working tag
  (above). Live iteration with a status flag.
- `southfetchprobe42` 0.0.2 → 0.0.3: the 403-log `probe.rb` deleted, new `out.rb`
  uploader added. **Cleanup after a leak.**
- `southnewsprobe1778550995` 0.0.1 → 0.0.3: adds the `#exfil` log line and the real
  date. The log was the point of the version.

## 7. Theater files (named to provoke, empty inside)

`evil.rb` ×21, `payload.rb` ×7, `hack.rb` ×6, `inject.rb`, `lambproxy.rb`,
`runnerhack1778553910`'s nested `lib/payload.gem` — **all 1 byte / empty**. Named for
whoever (or whatever scanner) reads the file list. The voice here is aimed outward —
at Diffend, at RubyGems reviewers, at us.

---

## Overall read

The corpus has two voices because it has two authorship modes. The 330 bulk canary gems
are machine-generated and mute. The ~26 hand-tended gems (voice set — distinct from the
verified fetcher-builder tier, see terminology note at top) are human- (or agent-) tended, and
*their* voice is ops chatter: beacons, mission notes, leaked logs, status flags. The
registry functioned as the dead-drop board — each generation's health was published as
the next generation's metadata, readable by anyone watching the gem page, no separate
channel needed. The single most human line in the corpus remains:

`# get any modern gov page to prove`

No non-English text, no leetspeak, no taunts found. The chatter is workmanlike, not
playful — with one exception: the empty `evil.rb`/`payload.rb`/`hack.rb` filenames,
which read as a wink at the audience.

**Caveats:** 408/608 pins harvested at analysis time — re-run on the complete set.
Diffend-diff reconstruction can stitch checksum noise into files (seen as leading
`metadata.gz:`/`data.tar.gz:` lines); treated as artifact, not voice. API key values
are deliberately absent from this catalog — see the runner-hunt report for the
redacted-prefix key catalog.
