# Cryptologist lane — July 2026 RubyGems spike CSV

Source: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
SHA-256: `765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0`
Rows: 533. Withdrawn: 533/533. Dates: 2026-07-06 00:27:26 to 2026-07-13 19:35:05 UTC.
Scope scanned: `name`, `summary`, `homepage_uri`, `source_code_uri`, `runtime_dependencies`.
No live fetch was done in this lane. No file was changed.

## Answer in one line

No go-import mechanism is present in this file. The payloads that ARE present
are registry-metadata injections: SSRF / out-of-band callbacks, XSS, and SSTI
strings placed in summaries, homepages, and author fields. That is the July-7
shape, not the May go-import shape.

## Payload inventory (found)

### 1. Out-of-band (OAST) callbacks — 29 distinct rows

Hosts (homepage_uri, source_code_uri, or summary):

- `d966sooa8p5umhpheccg6tnm9at8ix9kh.oast.online` — 23 URL hits, mostly path
  `/ssrf_linkback`; also `/homepage`, `/homepage_uri`, `/source_code`,
  `/ssrf_verify`, `/homepage-ssrf-test`, `/chain_backend`.
  Rows include apex-black-test-012, apex-black-test-013, apex-black-test-031,
  apex-black-test-032, apex_ssrf_test_v2, apex_exfil_test, apex_xss_test,
  apex_webhook_capture, apex_registry_test, apex_yaml_test, apex_html2_test,
  apex_es_exfil, apex_es2_exfil, apex_req_test, apex_probe,
  test_with_newline_char.
- `d96977lq1pkct8do7pn0dh1nbhzygujby.oast.online` — 1 hit, path `/ssrf`.
  Row: xss-test-gem (source_code_uri).
- `d96877a5q295v25se560q7ntmmwky7x8o.oast.online` — 2 hits, paths
  `/xss-desc` and `/admin-xss-1`. Rows: attacker-oob-test, attacker-xss-admin-1
  (both in summary, inside `<img>` tags).
- `d968608m2jk0d0682igg8sstei7ijqcs1.oast.site` — 1 hit. Row in inventory.json.
- `d96ah6oa8p5vog0r7qe0iijrn6y5nmozg.oast.me` — 2 hits, paths `/` and
  `/ssrf-chain-test`. Rows: ssrf-dns-e2600722, ssrf-dns3-69011af4.
- `d96ah88a8p5vopcdrlb019aprpm4n8bao.oast.live` — 1 hit. Row: ssrf-dns2-08e81090.

Note: the two `oast.me` hits also matched a naive `t.me` substring check.
They are OAST hosts, not Telegram links. No real `t.me` link is present.

### 2. webhook.site dead drops — 19 rows by substring, 18 by homepage host

Distinct webhook.site UUID paths (homepage_uri):

- `6915e541-204f-4e05-88d1-34de1f8bf35a` — apex-black-test-033 (bare)
- `dc9695db-cae6-4363-9973-482e9149af23` — apex_hp_callback, path `/homepage-verify`
- `276a367e-e997-43c4-8549-24fee408795c` — apex_link_tracker, path `/tracker`
- `355bfd32-9087-4f08-9c57-415bbe11585d` — apex_link_meta (bare)
- `ea5f8276-b681-4027-8172-4f70156c6f63` — apex_chain_test, path `/linkback-chain`
- `36683ea5-366e-4487-8ffe-3d2d6a508977` — 4 rows: ssrf-test-verify-1783406109,
  noko-test-1783406292, noko-deep-1783406351, timeout-test-1783406412
- `07937131-729b-4c30-b902-ff30cdc340b2` — 5 rows: large-html-1783406587,
  nullbyte-1783406604, badhtml-1783406636, deepnest-1783406648,
  formtable-1783406675
- `b8549d30-757a-4621-8ba0-65a0f2add1fb` — 3 rows: ssrf-baseline-d6cceaae,
  ssrf-redir-dde965d9, ssrf-asset-befc1f79
- `d09dfc77-cd5f-4ed9-8429-d155d8b0cd36` — ssrf-chain-a-1783408612 (bare)

Extra chain shape: ssrf-redirect-test-1783406163, homepage_uri =
`https://httpbin.org/redirect-to?url=https://webhook.site/36683ea5-366e-4487-8ffe-3d2d6a508977`.
That row is counted in the 19-row substring total, not the 18-row host total.
Summary-only webhook mentions: apex_es_exfil, apex_es2_exfil (exfil-token
wording), webhook-fire-1783405247, webhook-payload-1783405583,
webhook-capture-1783406220 (name/summary only, no homepage).

OAST and webhook.site row sets do not overlap. Combined OOB rows: 48.

### 3. SSRF / internal targets — 24 distinct homepage rows

- Cloud metadata paths: `169.254.169.254/latest/meta-data/` —
  apex-black-internal-000, apex_hp_internal, apex_link_aws;
  `metadata.aws.internal/latest/meta-data/` — apex-black-test-001
  (homepage_uri AND source_code_uri);
  `metadata.google.internal/` — apex-black-internal-003;
  `instance-data.us-west-2.compute.internal/latest/meta-data/` —
  apex-black-dns-000; `ip-10-0-0-1.us-west-2.compute.internal/` —
  apex-black-dns-001.
- Loopback / private: `127.0.0.1` with ports 3000, 9200, paths `/admin`,
  `/rails/info`, `/search?query=...` — apex-black-internal-001,
  apex_link_es, apex_link_admin, apex_link_health, apex_inject_test,
  apex_inject2_test; `10.0.0.1/` — apex-black-internal-002.
- Public IPs as targets: `16.148.236.35` (9 URL hits: bare, `:3000`, `:443`,
  `/internal/ping`, `/internal/revision`, `/api/v1/gems/apex-black-test-001.json`)
  — apex-black-backend-000/001/002, apex-black-probe-000/001/002/003,
  ssrf-ip1-c7947273, ssrf-ip1p3000-ab43636d; `34.210.16.211/` —
  ssrf-ip2-9aecd88c.
- Summary-only local target: internal-scan-1783405777, summary URL
  `http://localhost:3000/sidekiq`.
- `http://` (not `https`) homepage/source rows: 12, all in the SSRF set
  above except jrjackson and apex_homepage_ssrf.

### 4. XSS in summary — 10 rows

attacker-hunt-xss, xxstest-1783395545, apex-black-test-030, apex_xss_test,
test-xss-meta, attacker-oob-test, attacker-xss-admin-1, apex_html2_test,
apex-black-fuzz-045, xss-test-gem-001.
Shapes: `<img src=x onerror=alert(1)>`, `<svg onload=alert(1|2)>`,
`alert(document.domain)`, and the two OAST `<img>` tags above.
apex_html2_test also carries a summary link to `https://evil.com`.

### 5. SSTI in summary — 4 rows

apex-black-fuzz-050 (`{{7*7}}` shape), test-ssti-0, test-ssti-1, test-ssti-4
(`${7*7}` / ERB-style shapes; exact template strings are in the CSV).

### 6. Payloads in authors_declared (outside the tasked columns, found while scanning)

9 rows carry a script, image, or template payload as the author string:
apex-black-test-030, attacker-xss-admin-1, test-ssti-0, test-ssti-1,
test-ssti-4, test-xss-meta, test-yaml-erb, xssname-1783397821,
xxstest-1783395545. One of these (xssname-1783397821) is the single
`document.cookie` hit in the whole file, and it is in authors_declared only.
This is metadata injection into the author field, not a separate mechanism.

### 7. Payload-shaped names — do NOT infer payloads from these alone

- `ssrf-*` names: 23. `webhook-*` names: 3. Of those 26 rows, only 12 carry
  an OOB/IP/metadata homepage; the other 14 have an empty homepage or a
  rubygems.org-internal homepage (for example ssrf-port3000-7b3bf122 →
  `https://rubygems.org:3000/`, ssrf-chain-b-433928ce → a rubygems.org gem
  page). Name alone is not a payload.
- 8-hex suffix names (`-[0-9a-f]{8}$`): 18. Epoch-like names
  (`-1[67]…`): 34. These are identifiers, not encoded data.
- `apex_*` names: 114. That is a naming family, not a payload.

### Explicit NONE results (target columns, all 533 rows)

- go-import tags: 0. Import paths: 0. VCS values (`hg`, `fossil`, `bzr`,
  `svn`, `mercurial`, `darcs`, VCS schemes): 0. `github.com` URLs are
  code-host links, not a VCS-value field.
- Jina laundering (`r.jina.ai`, `jina.ai`): 0. UK council targets
  (Wandsworth, Lambeth, Southwark): 0.
- Cloud buckets (`s3.amazonaws`, `storage.googleapis`, `blob.core.windows`): 0.
- Other dead drops: ntfy 0, requestbin 0, pipedream 0, beeceptor 0,
  hookbin 0, ngrok 0, trycloudflare 0, localtunnel 0, pastebin 0,
  discord.gg 0.
- Code-execution shapes: `curl `, `wget `, `eval(`, `os.system`,
  `subprocess`: 0.
- Genuine base64 blobs (≥32 chars, mixed case + digits): 0. The only
  long-token hits are two `a…` repeated-character names, which are
  length artefacts, not encoded data.
- Credential-shaped values: 5 fields matched a keyword-only pattern
  (`token` / `api key` wording in summaries). Count only, per task rules —
  no values are copied here. No `sk-`, `ghp_`, or `AKIA` pattern hit: 0.
  Full bytes stay in the preserved CSV only.

## Mechanism match / no-match

| Known mechanism | This file | Verdict |
|---|---|---|
| May 2026: go-import meta tags pointing Go tooling at UK council calendar sites via r.jina.ai, VCS hg/fossil/git/bzr/svn | 0 go-import, 0 jina, 0 council hosts, 0 VCS values | NO MATCH |
| June 2026: plain link-posting | No target-site link posts. Links are rubygems.org profiles, github.com repos, or the OOB endpoints above. The mass batches (309× "University research based on …") are template metadata, not target links | NO MATCH as a distinct mechanism |
| July-7: XSS / SSTI in registry metadata | XSS summaries 10 rows, SSTI summaries 4 rows, payload authors 9 rows | MATCH |
| July-7-adjacent, not in the brief's July-7 label: SSRF / OOB callback in metadata links | OAST 29 rows, webhook.site 19 rows (substring), IP/metadata 24 rows, dashboard "oob url" on 48 rows, "probe name" on 59 rows, both on 21 rows | MATCH (same metadata-injection family, SSRF/OOB flavour) |

Union of rows with any OOB, IP/metadata, XSS, or SSTI field above: 82 rows.
The other 451 rows carry no payload string in the scanned columns — mostly
the 309-row "University research based on …" template batch and the
combinatorial-name batches.

## Host / scheme / dependency tallies

- URL occurrences in scanned columns: 645. Schemes: https 630, http 15.
- Distinct hosts: 29. Top hosts: rubygems.org 340, github.com 217,
  d966sooa8p5umhpheccg6tnm9at8ix9kh.oast.online 23, webhook.site 18
  (host-count; 19 by substring, see above), 16.148.236.35 9, 127.0.0.1 6,
  httpbin.org 3, 169.254.169.254 3, gitlab.neatnerds.be 2,
  metadata.aws.internal 2, www.ecoportal.com 2. Full list in tallies.json.
- URL host+path shapes: 56 distinct, including
  `rubygems.org/profiles/<name>` (303), `github.com/Andrey78/<name>` (78),
  `github.com/monib110/<name>` (46), `github.com/Prvaz12_mars/<name>` (67),
  `rubygems.org/gems/<name>` (12), `webhook.site/<uuid>` (15 bare),
  `*.oast.online/<path>` shapes above.
- Homepage_uri: empty on 100 rows, 82 distinct values.
  Source_code_uri: empty on 327 rows, 205 distinct values.
- runtime_dependencies is NOT a name list in this file. It is a count:
  `0` on 509 rows, `1` on 9, `2` on 6, `3` on 4, `4` on 2, `5` on 1,
  `17` on 1, `22` on 1. Distinct dependency names present: 0. No dependency
  payload can be assessed from this file.
- Summary "based on …" mentions: 310 rows, 116 distinct values — these are
  copied legitimate-gem names inside the template summary, not declared
  dependencies. Do not treat them as a dependency list.
- Names: 533 distinct. Summaries: 224 distinct values (top: "Test" 54,
  "Testing link verification SSRF" 26, "testing" 19).

## Coverage limits (grade: material)

1. This CSV holds registry metadata strings only. It holds no gem code,
   no gemspec file bytes, and no served homepage HTML. A go-import tag
   lives in served HTML, not in these columns, so "0 go-import here" rules
   out a go-import payload *in this file*, not a go-import payload in any
   gem or page behind these rows. That check belongs to the corroboration
   lane, which owns live checks.
2. No dependency names exist in this file (see above), so dependency-based
   hiding cannot be assessed here.
3. Payload counts above are string-presence counts in metadata fields.
   Presence of an XSS/SSTI/SSRF string is not proof it executed or that a
   callback fired. Whether any OAST/webhook endpoint received a hit is
   outside this lane and outside this file.
4. Dashboard labels ("oob url" 48 rows, "probe name" 59 rows) are analyst
   labels in the CSV, not observed payloads. They agree with the string
   findings on the OOB rows but were not used as evidence for any row
   counted above, except where noted as labels.

## Outputs (this lane only, no git, no Factum)

- [report.md](sandbox://workspace/silent-locus/reports/rubygems-july-spike-review/working/cryptologist/report.md)
- [scan.py](sandbox://workspace/silent-locus/reports/rubygems-july-spike-review/working/cryptologist/scan.py)
- [inventory.py](sandbox://workspace/silent-locus/reports/rubygems-july-spike-review/working/cryptologist/inventory.py)
- [tallies.json](sandbox://workspace/silent-locus/reports/rubygems-july-spike-review/working/cryptologist/tallies.json)
- [inventory.json](sandbox://workspace/silent-locus/reports/rubygems-july-spike-review/working/cryptologist/inventory.json)

CSV untouched (read-only scan; sha256 re-verified at scan time).
