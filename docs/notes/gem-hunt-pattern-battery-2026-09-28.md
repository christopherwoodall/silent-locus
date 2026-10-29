# Pattern battery on libraries.io — 2026-09-28

Per Christopher's guidance (hunt by PATTERN, not exact phrase), the libraries.io lane was
re-run as a grammar battery. libraries.io has no anonymous search API (login/API key
required — not pursued), so the pattern battery ran as direct project-page fetches over
generated + inventory name lists, with mechanism-marker greps over the returned
descriptions.

## Battery composition

| Battery | Size | Source |
|---|---|---|
| `try[a-z][0-9]zz` combinatorial | 231 unseen combos | generated (29 already in census excluded) |
| JFrog grammar names | 648 | gemstuffer-jfrog-2026-09-27.csv names matching: 10-digit epoch suffixes, oai*/zz* prefixes, try[a-z][0-9]zz, probe/proxy/prx/fetch/yard/hack/jina/test/xss/hook keywords |
| JFrog non-grammar rest | 1,819 | all remaining JFrog-only names |
| **Total checked** | **2,698** | |

Result: **1,609 new live pages** (tryzz 0/231, grammar 455/648, rest 1,154/1,819), of which
**1,191 carry go-import payloads in their descriptions**. Combined census now
`hidden_files/lane1/census_combined.jsonl`: 3,027 unique names, 1,912 found live.

Scripts: `hidden_files/lane1/pattern_battery.py`; raw: `tryzz_hits.jsonl`,
`jfrog_grammar_hits.jsonl`, `jfrog_rest_hits.jsonl`.

## Findings (cream)

### 1. tryzz namespace exhausted — 0/231
Every unseen `try[a-z][0-9]zz` combination (231 checked) is absent from libraries.io.
The family was fully captured by our harvest + original census. The namespace is closed.

### 2. July-7 wave fully mirrored — 55 gems, atom-dated 2026-07-07 03:30–06:15 UTC
The complete third-family catalog (XSS/SSRF/tar/YAML red-team) is preserved on
libraries.io, all dated via `versions.atom` feeds to July 7:
- `apex_xss_test` (04:05Z): `<img src=x onerror=alert(document.domain)>` —
  https://libraries.io/rubygems/apex_xss_test
- `apex-black-test-030`: `<svg onload=alert(1)>`
- `apex-black-test-033`: "Testing link verification with webhook.site"
- `apex-black-test-032` / `apex_exfil_test` / `apex_chain_test` / `apex_inject_test`:
  "Testing link verification SSRF"
- `test-xss-xss-html`: `<script>alert(1)</script>`; `test-xss-xss-link`:
  `[click](javascript:alert(1))`; `test-xss-xss-data`: markdown data-URL XSS
- `apex_tar_test` (05:25Z): "Testing tar traversal"; `apex_yaml_test` (05:00Z):
  `!ruby/object:Hash` deserialization probes
- **`apexblack-evidence-1783394610`** (03:30Z): "Proof-of-impact: pushed via
  scope-escalated legacy API key" — direct admission of the API-key mechanism.
  https://libraries.io/rubygems/apexblack-evidence-1783394610
- `attacker-tenant-test-1/2` (04:45Z), `apex-test-write-001` (05:15Z),
  `apex-final-test-1783404427` (06:15Z): "Cross tenant test gem" /
  "cross-tenant write testing" — matches the July 6 vuln report / July 9 fix timeline.

### 3. oai echo-rig family — 123 found, dated 2026-05-11 09:50–10:35 UTC
go-import tags with `mod` VCS pointed at **HTTP echo services**
(httpbin.org, postman-echo.com, httpbingo.org, eu.httpbin.org) — instrumentation to verify
the go-import fetch actually fires. Example:
`oaibo048288`: `<meta name='go-import' content='rubygems.org/api/v1/gems/oaibo048288.yaml mod https://postman-echo.com/get?fo...`
- **`oaihx7579061`** (2026-05-11T10:35Z): `<meta name='go-import' content='rubygems.org/api/v1/gems/oaihx7579061.yaml mod https://webhook.site/token?foo=1'>` —
  webhook.site as a go-import callback target **on May 11**. The webhook dead-drop
  technique's lineage traces back to the May-11 echo rig, not July.
  https://libraries.io/rubygems/oaihx7579061

### 4. Timeline pushed back — May 8/9 waves
- `zzpa` / `zzpc` / `zzpe` (**2026-05-08**T16:25Z): go-import → Google Drive file
  `0ByXlrcn4L69jdUJDTGhwQ0RfdGM` via lh3.googleusercontent.com and drive.google.com —
  a new target host class (Google-hosted content).
  https://libraries.io/rubygems/zzpa
- `aoswproxytest8012` (**2026-05-09**T12:15Z): `<meta name="go-import" content="rubygems.org/gems/aoswproxytest8012 git https://aosw.org/file"> <script>x</script>` —
  the go-import + inline-XSS hybrid existed from the campaign's first week.
- `proxssrfetviqtfb` (**2026-05-12**T02:10Z): "Remote exfil" — the exfil concept is May-wave.
- `exfiltestwand2/3` (**2026-05-12**T02:15Z): `<img src="https://democracy.wandsworth.gov.uk/mgCalendarMonthView.aspx" />` and the markdown-image
  variant — May-wave **image-tag exfil beacons** at the Wandsworth calendar (mechanism
  variant: neither go-import nor webhook).
- `agentxyztest987`: `</p><meta name="go-import" content="rubygems.org/gems/agentxyztest987 git https://github.com/pkg/errors"><p>` —
  go-import → the real Go package github.com/pkg/errors, with `</p>...<p>` HTML breakout
  in the description rendering; import path uses `rubygems.org/gems/<name>` (no /api/v1/)
  — a distinct grammar variant.

### 5. June-18 wave mirrored — 55 gems
June-18-style `00proxy`/`00prx`/`-00` names present with innocuous descriptions
("Public transformation references", "Reference transport"). `a--00cfmapjson726`
atom-dated **2026-06-18**T18:05:02Z. No sec.gov/county.json targets in their descriptions
(the June wave's links lived in gem metadata, not descriptions).

### 6. Pattern (3) partially blocked — "Testing <Animal>" authors
libraries.io exposes **no author field** anywhere: not in HTML pages, not in
`versions.atom` feeds (author is "Libraries.io"), not in the public API project endpoint
(verified — no `authors` key). The July "Testing <Animal>" author format cannot be
verified through this mirror. The descriptions do carry "Testing …" markers (45 hits).

### 7. Mechanism markers absent — as expected
Zero hits for `web_hooks`, `oast.online`, `A000`, `ZZEND` across all 1,912 found
descriptions. The southpxdatapp6pi zlib+base64 dead-drop lives in gem metadata URL
paths, invisible to the libraries.io description mirror — it remains a Diffend-bytes-only
technique.

## Wave timeline as now dated (libraries.io atom feeds)
May 8 (Drive targets) → May 9 (XSS+go-import hybrid) → May 11 (oai echo rig, 09:50–10:35 UTC;
rehearsal) → May 12 (main burst; "Remote exfil", image-tag beacons) → June 18 (link-posting)
→ July 7 (XSS/SSRF/cross-tenant red-team, 03:30–06:15 UTC).

## Caveats
- libraries.io is a partial mirror: 1,115/3,027 names checked are missing (time-freeze
  effect from the May-12 burst still applies).
- "Testing " description markers are operator-written labels, not author metadata.
- The `versions.atom` `<updated>` field is the feed timestamp; `<published>` entries are
  the version publish dates used above.
- Broad pattern *search* (substring/regex across all of libraries.io) remains unavailable
  without login/API credentials — this battery covered generated grammars + the JFrog
  3,025-name inventory only. The oai family per the July-18 advisory is 206 names vs 141
  in the JFrog CSV; the delta list is not in hand.
