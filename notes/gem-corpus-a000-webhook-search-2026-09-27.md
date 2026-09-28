# A000/ZZEND + webhook dead-drop corpus search — 2026-09-27

**Task:** housekeeping confirmatory search. Lane 21 confirmed via JFrog and Nightingale Collective
(rubyhack.ai) that the campaign used `https://rubygems.org/api/v1/web_hooks` as a data store with
A000 chunk sequencing (`https://example.com/A000/<chunk>`, ≤220-char chunks). This search checks
what our own corpus bytes show.

**Verdict: CONFIRMED in our own bytes — and earlier than expected.** Seven gems in the local
Diffend-reconstructed corpus carry the webhook dead-drop payload, all published **2026-05-12**
(01:57–03:28 UTC), i.e. the **May burst**, not July. The July 7 wave's 59 epoch-named gems in our
corpus contain zero webhook markers.

## Method

- Static extraction only (no execution, no network). For each of the 618 `.gem` files in
  `data/raw/gems/`: decompressed `metadata.gz`, scanned small files inside `data.tar.gz`,
  regex-searched for `A000`, `ZZEND`, `web_hooks`, `webhook`, `southpxdatapp6pi`,
  `example.com/A`, `oast.online|webhook.site`, chunk-scan patterns (`scan(/.{1,N}/)`),
  `%03d|%04d|rjust`, and `Net::HTTP::Post` + Authorization markers.
- Grepped all notes and data JSONL/CSV (excluding raw gems) for the same markers.
- Wave dating from `data/gem-ioc-log.jsonl` `published_at`; JFrog membership from
  `data/gemstuffer-jfrog-2026-09-27.csv`.
- The Elastic index `rubygems-goimport-campaign` was not queried (no vault access from this
  lane); it was ingested from these same local files, so the local search is authoritative.

## The 7 webhook dead-drop gems (all May 12, 2026)

All POST zlib-deflated, base64-urlsafe-encoded page scrapes as ≤N-char chunks to
`https://rubygems.org/api/v1/web_hooks` via `set_form_data({'gem_name'=>..., 'url'=>...})`,
authenticating with an embedded `rubygems_` API key (keys redacted below per standing rule).

| Gem | Ver | Published (UTC) | Chunks | URL template | Terminator | Scrapes | Delivery vector | JFrog XRAY |
|---|---|---|---|---|---|---|---|---|
| southpxdatapp6pi | 0.0.1 | 2026-05-12 01:57 | `.{1,220}` | `https://example.com/A%03d/<chunk>` → A000, A001… | `…/ZZEND/<count>` | moderngov.southwark.gov.uk calendar | lib/x.rb | XRAY-982441 |
| wandzfetch1500929 | 0.0.1 | 2026-05-12 02:33 | `.{1,150}` | `https://example.com/W17162/<i.rjust(4,'0')>/<chunk>` | `…/W17162END/<datalen>` | democracy.wandsworth.gov.uk calendar | lib (payload in gemspec area) | XRAY-982373 |
| wandzfetch1500929 | 0.0.2 | (same harvest) | `.{1,800}` | run=`Q61361` (same family, snapshot truncated) | unknown (truncated) | wandsworth calendar | — | XRAY-982373 |
| lambtmp35293950 | 0.0.2 | 2026-05-12 03:02 | single ping | `https://example.com/EVILTEST-<epoch>` | n/a | none (liveness ping) | evil.rb | XRAY-982379 |
| sl-yard-probe2 | 0.0.1 | 2026-05-12 03:18 | single ping | `https://example.com/PLUGINRAN<epoch>` | n/a | none (liveness ping) | **plugin.rb (yard plugin hook)** | XRAY-982324 |
| fetchrootx1 | 0.0.1 | 2026-05-12 03:20 | `.{1,180}` | `https://example.com/<i>_<chunk>` | `…/ERR<sanitized msg>` | moderngov.lambeth.gov.uk calendar | **ext/z/extconf.rb (native-ext build hook)** | XRAY-982429 |
| fetchrootx2 | 0.0.1 | 2026-05-12 03:28 | `.{1,180}` | `https://example.com/<i>_<chunk>` | `…/ERR<sanitized msg>` | democracy.wandsworth.gov.uk calendar | **ext/z/extconf.rb (native-ext build hook)** | XRAY-982428 |
| wandcabfetchfix21736 | 0.0.1 | 2026-05-12 03:23 | `.{1,700}` | `https://example.com/CAB%04d/<chunk>` → CAB0000… | `…/CABEND/<count>` | wandsworth ieListDocuments (CId=792) | lib payload | XRAY-982417 |

Notes:
- `southpxdatapp6pi` is the canonical A000/ZZEND specimen: chunks of exactly ≤220 chars,
  `A%03d` sequencing, `ZZEND/<chunk-count>` terminator, and an `ERR/<class>_<message>` error
  path (message sanitized to `[A-Za-z0-9.-]`, 80 chars). Full payload preserved at
  `data/raw/gems/southpxdatapp6pi-0.0.1.gem`.
- `lambtmp35293950`'s payload declares `gem_name='wandsworthproxyabcabc'` — a name mismatch
  with the published gem name, suggesting payload reuse across names.
- Delivery vectors vary: `lib/*.rb`, `extconf.rb` (runs at `gem install` build time), and
  `plugin.rb` (runs when YARD loads the gem — the "YARD RAN" family).
- `wandzfetch1500929-0.0.2` is a **truncated Diffend snapshot** (717-byte metadata.gz, cut
  mid-payload, no gemspec header). Run id changed `W17162` → `Q61361`, chunk size 150 → 800.
  Its POST target line did not survive the snapshot.

## Mechanism taxonomy (4 chunk grammars + 2 probe pings)

1. `A%03d` — 3-digit zero-padded (`A000…`), 220-char chunks, `ZZEND` terminator — southpxdatapp6pi
2. `<RUN>/%04d`-via-`rjust(4,'0')` — run-scoped (`W17162/0003/…`), `<RUN>END` terminator — wandzfetch1500929
3. `<PREFIX>%04d` — prefix-scoped (`CAB0007/…`), `<PREFIX>END` terminator — wandcabfetchfix21736
4. `<i>_<chunk>` — bare index prefix, 180-char chunks, `ERR` terminator only — fetchrootx1/x2
5. Single liveness pings (`EVILTEST-<epoch>`, `PLUGINRAN<epoch>`) — lambtmp35293950, sl-yard-probe2

Literal `A000` **never appears in gem bytes** — it is generated at runtime (`'A%03d' % i`).
A literal-string search for "A000" misses the mechanism; the searchable pattern is
`%03d|%04d|rjust` sequencing inside a `web_hooks` POST. Literal `ZZEND` appears once
(southpxdatapp6pi).

## Wave classification

- **May go-import wave (2026-05-12):** all 7 webhook gems. The webhook dead-drop is a **May
  mechanism**, parallel to the go-import tags — not a July invention. All 7 are in JFrog's
  inventory (XRAY-982324 … XRAY-982441).
- **July XSS/SSTI wave:** 59 epoch-named (`177855…`) gems in our corpus (chatoaifetch*,
  chatoaitest{git,hg,svn,bzr,fossil}, hack{git,hg,svn,bzr,fossil}*, wandsworthprobe1778551714,
  …). Their markers are go-import tags and `example.com` placeholders
  (e.g. `<meta name="go-import" content="… git https://r.jina.ai/http://example.com/">`).
  **Zero** contain `web_hooks`, `oast.online`, or `webhook.site` in our bytes. JFrog's
  oast.online/webhook.site July callbacks are not represented in our corpus snapshots.
- **Separate mechanism — push-endpoint family:** ~60 additional gems match
  `Authorization` + `Net::HTTP::Post` but POST to `https://rubygems.org/api/v1/gems`
  (the gem-publish endpoint) or `/api/v1/api_key` — credential use for self-publishing
  (e.g. slnleaker4/5's wandpayload self-replication), not the webhook data store.
  Do not conflate the two.

## Negative results

- `southpxdatapp6pi`: no other gem in the corpus references this name in bytes (only in
  our own IOC logs/notes and the JFrog CSV).
- No `oast.online`, `webhook.site`, `interactsh`, or `burpcollaborator` strings in any of
  the 618 gem payloads.
- No additional `web_hooks` POSTs beyond the 7 gems above (full-metadata sweep).
- Notes/data references to A000/ZZEND/web_hooks are all hunt-lane writeups citing the
  JFrog report — no independent local source besides the 7 gems.

## Corpus gaps / caveats

- `wandzfetch1500929-0.0.2`'s Diffend snapshot is truncated; its 0.0.2 exfil target is unknown.
- July-wave webhook callbacks (oast.online/webhook.site per JFrog) have no byte-level
  representation in our corpus — the July gems we hold are the go-import/placeholder subset.
- The pending Diffend sweep (Lane 20) covers 1,284 advisory names missing from this corpus
  and may surface more dead-drop variants.
- Embedded API keys were redacted in this report per standing rule (never use, validate,
  expose, or transmit recovered keys). Key reuse observed: wandzfetch1500929 0.0.1/0.0.2
  share one key; slnleaker4/5 share another.

## Cross-refs

- JFrog integration: `notes/gem-jfrog-report-2026-09-27.md`
- Advisory layer: `notes/gem-hunt-osv-2026-09-27.md`, `data/osv/ghsa_gemstuffer_classified.json`
- Dead-drop (agent-chatter) note — different mechanism: `notes/gem-deaddrops-2026-09-27.md`
- Diffend sweep in progress: `data/osv/diffend_sweep_results.jsonl`
