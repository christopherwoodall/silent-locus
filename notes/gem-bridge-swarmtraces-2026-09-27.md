# Bridge analysis: gem campaign ↔ SwarmTraces HF dataset (2026-09-27)

**Question from Christopher:** "Anything connected to our other dataset?"
**Corpora:** gem side = our independent Diffend-sourced collection (359 harvested gems, `data/gem-ioc-log.jsonl`); HF side = SwarmTraces `data/raw/redacted.jsonl.gz` (189,579 records, fields id/cite/kind/parent_id/time_utc/tags/text). Read-only on both; no gem code executed.

## Method
Built a 570-pattern literal search battery from the gem side (infrastructure strings, all 329 distinctive gem names, 38 epoch nonces from gem names, VCS keywords, exfil/tool patterns) and streamed all 189,579 HF records once. Separately extracted zz-token sets from both sides (gem: 97 distinct; HF: 417 distinct) and compared exact + digit-stripped stems.

## Gem-side inventory (what was searched)
- **go-import tags:** 275 occurrences in gem summary/description; VCS values hg 146, fossil 26, mod 24, git 8, bzr 8, svn 6
- **Repo proxy:** `r.jina.ai` 156, `s.jina.ai` 9; gem names literally contain `zzjinavcs{fossil,hg,svn,bzr,git}`
- **Council targets:** moderngov.lambeth.gov.uk 32, digitizationguidelines.gov 12, democracy.wandsworth.gov.uk 6, moderngov.southwark.gov.uk 2
- **Authors:** `- x` 163, `- a` 69, `- z` 20, `- SLN` 14, `- DL` 11, `- oai` 8, `- zz` 7
- **Epoch nonces in names:** 38 distinct (all May 11–12 2026: 17784…–17785…)

## Literal hits (gem ↔ HF)

### 1. The `jina` reader-proxy laundering convention — 17 HF records (STRONGEST BRIDGE)
The HF operation runs its own reader-proxy URL-wrapping, structurally identical to the gem campaign's `https://r.jina.ai/http://<target>` pattern, and literally calls it "jina":

- **R0016759, R0016836** (payload): a JSON config with parallel proxy keys for the same Artifactory target —
  `"jina":"https://[SERVICE HOST 52]/http://packages.hub.ace-research.openai.org/artifactory/github-remote/zzFILE_OURB88_3818_EC3_PRECOMPILED_CONFIG_V1/"`, alongside `"isogit"`, `"jinas"`, and `"ssh"` keys wrapping the same URL through different proxies
- **R0085604** (recovered_text): agent code fetching through the proxy — `rq=urllib.request.Request(ju,...); ... print('JINAFINAL',mode,rr.status,...)` with `JINAERR` error handling
- **R0117636, R0117839, R0118652** (payload) and **R0154651, R0155212, R0157474** (response): beacon pages `<div>JINA SHORTTRY</div>` attempting a shortener URL through the jina proxy service
- R0016928, R0017118, R0017156, R0049761 (payload); R0091841, R0170413, R0175033, R0178599 (recovered_text): same family

Gem side for comparison: `https://r.jina.ai/http://democracy.wandsworth.gov.uk/mgCalendarWeekView.aspx?...` (156 uses), `s.jina.ai` (9), gems named `zzjinavcs*`.

**Reading:** same tradecraft convention — `<reader-proxy>/<target-URL>` wrapping — and the same literal name for it. But different proxy hosts (HF uses its own redacted service host; gems use public r.jina.ai/s.jina.ai) and different target classes (HF: own Artifactory; gems: UK council calendar sites). Shared convention, not shared infrastructure.

### 2. httpbun — 6 HF records, ZERO gem-side (not a gem↔HF bridge)
R0001241, R0001494, R0003848, R0009649 (payload): used as Host-header/DNS recon target (`headers={'host':'httpbun.com'}`), host-allowlist probing (`okhost`), and beacon image src (`i.src='...httpbun.com...'`). Gem corpus contains zero httpbun references. HF-internal pattern only (previously noted as inverted vs the frozen hunt: recon target there, code carrier in the hunt).

### 3. ntfy — 4 HF records, ZERO gem-side (not a gem↔HF bridge)
R0117987 (payload), R0155625 (response), R0185155 (recovered_text): `ntfy aihwpre1781775983` topic beacon page; R0131503 (payload): `https://[redacted]/w0/ntfy.sh` URL. Gem corpus contains zero ntfy references. HF-internal pattern only. (Note the epoch-bearing topic name `aihwpre1781775983` — same epoch-suffix convention as gem names, different epoch value.)

## Verified literal negatives (zero hits in all 189,579 HF records)
- `r.jina.ai`, `s.jina.ai` — 0 (165 combined uses on gem side)
- Council domains: wandsworth.gov.uk, lambeth.gov.uk, southwark.gov.uk, moderngov, digitizationguidelines — 0
- `go-import`, `rubygems.org/api` — 0
- All 38 gem epoch nonces — 0
- All 329 distinctive gem names (tryf3zz, wandsworthprobe1778551714, southwarkssrfhack, …) — 0
- zz tokens: 97 gem-side vs 417 HF-side — 0 exact overlap; digit-stripped stems overlap only on `zztest` and `zzzz` (generic test artifacts, coincidental)
- `bzr` (word-boundary) — 0 in HF; `fossil` — 2 hits, both false positives (`EVALUATE 'Fossil fuels'` in a PowerBI-style query, R0079383/R0106075)

## Pattern-level comparison (no literal reuse)

| Convention | Gem campaign | SwarmTraces HF | Assessment |
|---|---|---|---|
| Reader-proxy URL laundering, literally named "jina" | r.jina.ai/s.jina.ai wrapping council URLs; `zzjinavcs*` names | own proxy host (redacted SERVICE HOST 52) wrapping Artifactory URLs; `"jina"`/`"jinas"` config keys; `JINAFINAL`/`JINA SHORTTRY` code | **Shared tradecraft** — strongest bridge; same shape, same name, different hosts/targets |
| Epoch-suffix naming | gem names self-timestamp (17784…–17785…, May 11–12 2026) | build tags `-imds1-1784182621` (1,164 plausible epochs, Jun–Jul 2026 window); ntfy topic `aihwpre1781775983` | **Shared convention** — different values, different windows, different use |
| zz labels | try[a-z][0-9]zz, zzfadgivarNN, zzpdfvarNN | zzFILE_…, zzMODALBE90_RECON1_, github-remote-cache/zz | **Shared habit** — zero token overlap, different grammars |
| Exfil beacon pages | none observed | `<pre id=s>ntfy …` beacon pages, JINA SHORTTRY beacons | HF-only |
| go-import injection | core payload mechanism | absent | gem-only |
| httpbun | absent | recon/beacon target | HF-only |

## Verdict
**Shared tradecraft, not a shared operation.** The `jina` reader-proxy laundering convention is genuinely present in both corpora — same `<proxy>/<target>` shape and the same literal name, which is more specific than the generic zz/epoch habits. But every literal anchor fails: no shared proxy host, no shared target URL, no shared gem name, no shared epoch nonce, no shared zz token, no shared VCS value, and the active windows differ (gem burst May 11–12 2026; HF epochs cluster June–July 2026). The gem campaign's distinctive payload (go-import meta tags) is entirely absent from the HF data. Treat as two operations drawing on the same tradecraft vocabulary — consistent with a shared playbook or tooling lineage, not actor attribution. Do not merge the datasets; the existing separation (independent Diffend-sourced gem collection vs SwarmTraces corpus) is correct and should be preserved.

## Caveats
- zz-token extraction regexes differed slightly between the F3 fingerprint pass and this pass (417 vs 813 distinct HF tokens); the zero-overlap conclusion holds under both.
- HF `fossil` hits are false positives (unrelated "Fossil fuels" string).
- The frozen hunt's r.jina.ai IOC (618 reports) is a separate, previously established pattern-level bridge to the *hunt*, not re-verified here.
