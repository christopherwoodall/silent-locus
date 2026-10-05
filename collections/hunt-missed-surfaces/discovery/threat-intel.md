# Threat-intel venue scout — 2026-10-03

Mission: check PUBLIC threat-intel venues (keyless only) for our incident markers.
Question: has the intel community independently cataloged OUR markers?

## Markers queried
`zzproxyoaiabc431848`, `zz=oai`, `openai_research` variants, campaign packages
(`slnleaker5`, `f2fe-s1`, `yardxabc889`, `southpxdatapp6pi`, `southwarkssrfhack3`),
`county.json` + sec.gov, `civilrightsdata.ed.gov`, `survey_Year_Key`, `1 OR 1=1`.

## Per-venue verdicts

### AlienVault OTX — KEY-WALLED
- `GET /api/v1/search/pulses?q=...` → **HTTP 403 `{"detail": "Authentication required"}`** (no key).
- Browse page (`/browse/pulses?q=...`) → HTTP 200 but only an 8KB JS app shell; no server-rendered pulse data retrievable via curl.
- `site:otx.alienvault.com` web searches for `zzproxyoaiabc431848`, `openai_research`, `"zz=oai"` → **no results** (caveat: reflects the search backend's index, not OTX's internal DB).
- Verdict: no keyless access; no indexed OTX pulses for our markers. A free OTX API key would unlock real pulse search.

### urlhaus (abuse.ch) — BOT-WALLED
- `browse.php?search=...` → **HTTP 307 → `/verify-ua/`** (UA-verification wall; curl blocked).
- `site:urlhaus.abuse.ch` searches → no results.
- Verdict: unscourable keyless. Free abuse.ch auth key would unlock the API.

### ThreatFox (abuse.ch) — BOT-WALLED
- Same `/verify-ua/` redirect wall as urlhaus.
- `site:threatfox.abuse.ch` searches → no results.
- Verdict: unscourable keyless; same free-key path as urlhaus.

### VirusTotal — KEY-WALLED
- Public API requires a key; web GUI is JS/captcha-walled.
- `site:virustotal.com` searches for `zzproxyoaiabc431848` → no results.
- Verdict: no keyless route. Free VT API key would unlock file/URL search.

### Censys — LOGIN-WALLED
- search.censys.io requires an account; API requires key. Not probed further (established wall).
- Verdict: free account would unlock host/cert search for our infra.

### GreyNoise (community API) — KEYLESS, WORKS
- `GET https://api.greynoise.io/v3/community/<ip>` returns valid JSON with no key.
- `20.49.140.101` (gem-campaign raw IP from our IOC list) → `noise: false`, "IP not observed scanning the internet."
- Verdict: honest zero — expected; it's dead-drop/C2-shaped infra, not a scanner. GreyNoise only covers mass-scanning IPs, so it's the wrong lens for this infrastructure anyway.

### Maltiverse — AUTH-WALLED (in practice)
- `GET https://api.maltiverse.com/hostname/...` → HTTP 400 (auth required for useful queries).
- Verdict: free token would unlock.

## Cross-confirming hits (intel community DID see our infrastructure)

These are public, third-party, and reference our exact markers — not just generic gem-malware:

1. **JFrog Xray IOC table** — https://research.jfrog.com/post/gemstuffer-openai-rubygems/
   Lists `slnleaker5` (XRAY-982350), `f2fe-s1` (XRAY-1024400), `yardxabc889`
   (XRAY-982421), `southpxdatapp6pi` (XRAY-982441), `xss-test-gem`, `test-apex-gem`
   — all version 0.0.1. These are byte-for-byte our word-list v2 package IOCs
   (from notes/gem-*.md). Independent vendor cataloging of the same packages.

2. **GitHub Advisory Database GHSA-3qpq-4vg7-f4x6** (published Jul 18, 2026)
   "Malicious code in zzproxyoaiabc431848 (RubyGems)", affected `= 0.0.1`.
   OSSF/GitHub cataloged our exact marker package. (Also mirrored as
   OSSF:MAL-2026-9973 on vulners/offseq/vulert.)

3. **Socket GemStuffer tracker** — 155 artifacts, all published 01:27–03:25 UTC
   May 12; scanner flagged each within 3 minutes of upload. Independent
   confirmation of the dead-drop mechanism (registry as storage layer).

4. **Nightingale Collective recount** (rubyhack.ai, via LinkedIn/Sarvex Jatasra,
   Oct 3 2026) — 11–12 May: 2,000+ packages; 5 more May 26–27; **83 on Jun 18**.
   Timeline matches our corpus exactly, including the June 18 wave.

5. **vibe-coding-security advisory** (github.com/pranava0x0/vibe-coding-security,
   advisories/2026-09-openai-agents-rubygems-gemstuffer-campaign.md) —
   publicly names the `.yardopts` RCE primitive AND the scraping of
   "SEC `county.json` datasets" from the RubyDoc foothold. Cross-confirms
   county.json as campaign infrastructure in public writing.

## Honest zeros (markers found NOWHERE in intel venues)

- `zz=oai` / `zz=oai<digits>` — zero hits in every venue; only Transluce's
  report and our own Arquivo.pt corpus.
- `openai_research` variants — zero; only our fake-org/wiki corpora.
- `survey_Year_Key`, `State_Id=1 OR 1=1`, `Measure_Id` — zero outside
  Transluce's Sep-30 report (which names `State_Id=1 OR 1=1` verbatim).
- `civilrightsdata.ed.gov` SQLi — only Transluce + press echoing Transluce.
- `southwarkssrfhack3` — no threat-intel hits (only unrelated "Southwark" noise).

## Bottom line for the hunt

The intel community has independently cataloged the **malware-package layer**
(JFrog Xray IDs, OSSF/GitHub advisories, Socket tracker) — our package IOCs
cross-confirm. But the **agent layer** (`zz=oai` tags, `openai_research`
labels, DoE SQLi params) has NOT propagated into any public threat-intel
venue; it exists only in Transluce's reporting and our own corpora. That
asymmetry is itself a finding: the "agent" framing lives in research
writeups, while intel feeds see only commodity malicious gems.

Free keys that would unlock the walled venues: OTX API key, abuse.ch auth key
(urlhaus + ThreatFox), VirusTotal API key, Censys account, Maltiverse token.
