# CRYPTOLOGIST lane — working notes — RubyGems July 2026 spike set

Source: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
(533 rows + header). Method: independent Python csv + regex re-derivation over
`name`, `summary`, `homepage_uri`, `source_code_uri` (scan set), plus
`authors_declared` where stated. Row counts are rows unless marked "cell".
No payload, token, canary, or identifier value is reproduced here: shapes,
hosts-by-category, and counts only. No fetched payload was executed; this
lane did no live fetching at all — it classifies strings already in the CSV.

## 0. Headline: the review's counts reproduce, with two small corrections

- Payload-string union: **82 rows** in the scan set, **84 rows** including the
  author field. CONFIRMED exactly under the definitions below.
- Set sizes sum to 86; the union is 82 because exactly one pairwise overlap
  exists: OAST ∩ XSS = 4 rows. Every other pair overlaps 0.
- Correction 1 — the review's "24 homepage rows" for SSRF/internal: the 24
  rows are **23 home/source rows + 1 summary-text row** (a localhost URL
  carried in summary text, not in a link field). Homepage cell hits = 23;
  source cell hit = 1, on a row already counted via its homepage.
- Correction 2 — the review's "6 OAST hosts": confirmed as **6 distinct full
  hosts**, but only **4 base domains** (oast.online / oast.me / oast.site /
  oast.live shapes). One of the 6 hosts appears only in summary text, not
  in a link field (hosts per column: homepage 4, source 2, summary 1,
  with overlap).

## 1. Shape table (recomputed)

| # | Shape (mechanism) | Rows (scan set) | Where it sits |
|---|---|---|---|
| 1 | OAST callback URL (out-of-band collaborator host) | 29 | homepage 26 cells, source 2 cells, summary 2 cells; 30 cells over 29 rows (1 row has both homepage + source) |
| 2 | Webhook callback URL (webhook.site host + path token) | 19 | homepage 19 cells, all 19 rows; 0 in source/summary as URL |
| 3 | SSRF / internal target URL | 24 | see §0 correction; target hosts: cloud-metadata link-local IP (3), loopback (6), RFC1918 10-net (1), cloud metadata internal hostnames (3 rows across two provider shapes + one instance-data shape), plus public IPs below |
| 3a | Public-IP homepage URL (counted inside shape 3's 24 by the review's IP rule; split out here) | 10 | two public IPv4 hosts: one host on 9 rows, one host on 1 row |
| 4 | XSS markup in summary | 10 | summary only (0 in name/homepage/source). Marker split (rows, overlapping): image-tag 7, alert-call 8, onerror-attr 6, svg-tag 3, onload-attr 3; script-tag 0 in scan set |
| 5 | SSTI / template expression in summary | 4 | summary only. Shape split: double-brace 1, dollar-brace 1, ERB angle-percent 2 (of which strict `<%=` form 1) |
| 6 | Payload string in author field only | 2 author-only rows; 9 author rows total carry a markup/template payload | 7 of the 9 already inside the 82; 2 are author-only. Author markers: script-tag 4 rows (incl. scan-set overlap counting), image-tag +1 vs scan set, onerror +1 vs scan set, document.cookie 1 row (author field ONLY — the file's only cookie-exfil shape), template markers 4 author rows |
| 7 | YAML anchor / alias / tag | 0 confirmed | No document marker, no `!!` tag, no key structure anywhere; metadata fields are not YAML documents. Ambiguous fragments only: 1 `&word` row, 6 `*word` rows — 4 of the 6 sit inside template arithmetic (digit-star-digit), 2 bare `*word` summary fragments with no template context. A bare `*` can be multiplication, wildcard, or prose; none is established as an alias |
| 8 | Tar traversal (`../`, encoded, backslash) | 0 | all three forms, scan set and incl. author |
| 9 | Regexp-injection shape (lookahead / lookbehind / nested-quantifier run) | 0 | — |
| 10 | Code-execution string (curl / wget / eval-call / os.system / subprocess) | 0 | — |
| 11 | Go-import tag / jina-laundering string | 0 | — |
| 12 | Plain-http scheme (not a payload by itself) | 12 rows | 11 already inside the union; 1 http row outside it. Scheme shape only — http vs https proves nothing about the target |
| 13 | Other link shapes (not payloads) | httpbin mentioned on 3 rows (2 homepage, 2 summary cells, overlapping); example.com 1; nonexistent-domain shape 1; github.io 1; bitbucket 1; one further small-host shape 1 each | 2 of the 3 httpbin rows are already inside the union via other shapes; the rest sit outside it. An echo-service homepage is a generic request-reflection surface, not a callback receipt |
| 14 | Name-only probe shapes (NOT counted as payloads) | ssrf- prefix 23 + webhook- prefix 3 = 26 names | Of the 26, only 12 carry an out-of-band or IP homepage; 14 have empty or rubygems.org-internal homepages. A probe name is a label, not a callback |

Union check: 29 + 19 + 24 + 10 + 4 = 86 set sizes, minus the 4-row
OAST ∩ XSS overlap = **82**. Plus 2 author-only rows = **84**.

## 2. Prove / not-prove, per shape

General rule for every row below: the CSV holds registry metadata strings
only — no gem code, no gemspec bytes, no served-page HTML, no receiver
log. A published string proves, at most, that the string was published.

### Shape 1 — OAST callback URL (29 rows)
- PROVES: a metadata field carried a URL whose host belongs to an
  out-of-band interaction service, with a per-row or shared identifier in
  host/path. Host reuse is heavy: 1 host carries 22 of the 29 rows; the
  other 5 hosts carry 1–2 rows each. Path first-segment shape is mostly
  an `ssrf_linkback`-like segment (21 URL cells); the rest are
  token-like paths or bare hosts.
- DOES NOT PROVE: that any request was ever sent to the host; that any
  interaction was received or logged; what sent it (registry renderer,
  link follower, victim browser, the publisher testing their own
  string); exfiltration of anything; agent authorship. A callback URL
  in a homepage field is an invitation to fetch, not a fetch.
- NOTE: an OAST identifier is a canary by design (§3). Its presence in
  a public CSV does not burn anything — the receipt, if any, lives in
  the operator's receiver log, which is not in this file.

### Shape 2 — Webhook callback URL (19 rows, 9 distinct path tokens)
- PROVES: a homepage field carried a webhook.site URL with a
  UUID-shaped path token. Reuse: 6 tokens used once, 1 token used on
  3 rows, 2 tokens used on 5 rows each — so most rows share a small
  set of buckets rather than carrying one fresh canary each.
- DOES NOT PROVE: that any POST ever arrived at the bucket; what the
  payload would have been; who would have sent it; exfiltration.
  Webhook.site buckets are also the standard shape for a QA engineer
  testing "does this field get fetched / rendered". QA vs exfiltration
  is indistinguishable from the string alone.
- OAST and webhook row sets do not overlap (0 rows). Combined
  out-of-band rows = 48.

### Shape 3 — SSRF / internal target URL (24 rows incl. 10 public-IP rows)
- PROVES: a metadata link field (23 rows) or summary text (1 row)
  pointed at a link-local metadata address, loopback, RFC1918 address,
  provider-internal metadata hostname, instance-data hostname, or a
  public IPv4 host. The internal shapes are the classic SSRF target
  set; the public-IP rows are ordinary IP-literal homepages that the
  review's IP rule sweeps in — they are NOT internal targets and
  should not be quoted as "internal" without that split.
- DOES NOT PROVE: that any server-side fetch was attempted; that any
  fetch reached the target; that any metadata was returned; that any
  registry or link-follower performs server-side fetching at all;
  victim, impact, or authorship. A URL string in a gem homepage is not
  a request. The two public-IP hosts, in particular, prove nothing
  beyond "someone put an IP-literal homepage on a gem" — that host
  could be a test server, a sinkhole, or an unrelated box.

### Shape 4 — XSS markup in summary (10 rows)
- PROVES: a summary field carried HTML-tag / event-handler / alert-call
  markup strings. All 10 sit in summaries; none sits in a name,
  homepage, or source field. No script-tag row exists in the scan set;
  the markup is image/svg-tag + handler + alert-call shapes.
- DOES NOT PROVE: that any page rendered the summary as HTML; that any
  script executed; that any browser ran it; that any cookie or session
  was taken; that any user saw it. Whether RubyGems (or any mirror,
  dashboard, or API consumer) escapes summary text is a property of
  the renderer, not of this string. The file contains no rendered-page
  evidence.
- The file's only document.cookie shape sits in the AUTHOR field, not
  in a summary — it is a stored-string shape one field further from
  any plausible render path, and it still proves execution of nothing.

### Shape 5 — SSTI / template expression in summary (4 rows)
- PROVES: a summary field carried a template-expression string
  (double-brace, dollar-brace, or ERB angle-percent shape). The
  arithmetic inside is the classic `7*7` detector shape — it is a
  probe for "does something evaluate this", not a computed result.
- DOES NOT PROVE: that any template engine saw the string; that any
  evaluation happened; that a computed value (e.g. 49) was ever
  returned or displayed; which engine, if any, would be involved.
  A `7*7` string that was never evaluated is indistinguishable in this
  file from one that was — the file holds the input, never an output.
  Note the trap: the `*` inside the arithmetic is what trips naive
  YAML-alias scans (§1, shape 7). It is multiplication, not an alias.

### Shape 6 — Payload string in author field (9 rows, 2 author-only)
- PROVES: an author metadata value carried markup or a template
  expression instead of a name/handle. This is a field-abuse shape:
  it tests whether a consumer renders or evaluates the author field.
- DOES NOT PROVE: execution, rendering, or authorship in any stronger
  sense — same bar as shapes 4–5, with one extra weakness: author
  fields are less likely than summaries to be rendered as rich HTML
  by any given consumer, so the render hypothesis is thinner, not
  stronger.

### Shapes 7–11 — YAML, traversal, regexp, code strings, go-import (all 0)
- PROVE: nothing, because nothing is there. A zero in this file rules
  out the string in THESE FIELDS ONLY. It does not rule out a YAML
  payload inside a gemspec, a traversal inside a tarball, or a
  go-import tag in served gem-page HTML — none of those artifacts are
  in the CSV. Do not quote these zeroes as "the gems are clean".

### Shape 12 — Plain http (12 rows)
- PROVES: only that the link used an unencrypted scheme. No payload
  content follows from scheme alone.

### Shape 13 — Other link shapes (httpbin etc.)
- PROVE: a homepage or summary mentioned a generic echo/test service
  or a placeholder/example host. A placeholder host (example.com,
  nonexistent-domain shape) is evidence of a dummy value, not of an
  attack. An httpbin mention is consistent with "I wanted to see the
  request" QA testing and proves no receipt.

### Shape 14 — Name-only probe shapes (26 names)
- PROVE: the publisher chose a self-describing probe label. A name
  that says "ssrf" is a claim about intent to test, made by the
  publisher, in the publisher's own label.
- DOES NOT PROVE: that any SSRF test ran, succeeded, or targeted
  anything; that the name's claim is true; anything about the gem's
  code. 14 of the 26 names have no out-of-band or IP homepage at all
  — label without link.

## 3. Canary / marker assessment (shapes only, no values)

A canary is distinguished from a real secret and from a synthetic test
value by structure and by where the secret would have to live, not by
looking secret-like:

- **Canary shape:** a unique (or small-set-shared) identifier embedded
  in a locator the publisher controls the receiver for — an OAST
  subdomain, an OAST path token, a webhook path token. Its whole
  function is to appear in a receiver log. Identifying features here:
  (a) it sits in a URL host/path, not in a credential field;
  (b) it is unique per row or per small row-group (webhook: 9 tokens
  over 19 rows; OAST: 6 hosts over 29 rows, one host dominant);
  (c) it has no service prefix and no key=value framing;
  (d) its value is useless to anyone except the holder of the receiver
  log. A canary in a public CSV is therefore NOT a leak — it is a
  spent or unspent detector, and only the receiver log can say which.
- **Real-secret shape (absent here):** a credential would sit in a
  value position (not a URL host/path), carry a recognised service
  prefix or a key=value / bearer framing, and be usable by anyone who
  copies it. Scan results: service-prefix shapes 0 rows; key=value
  shapes 0 rows; bearer shapes 0 rows; token/api-key/checksum wording
  appears on 7 summary rows but as WORDS ABOUT tokens, not tokens
  (see below). No row establishes a real secret.
- **Synthetic test value shape:** a value that declares itself fake.
  One summary cell carries a `FAKE_`-prefixed shape co-occurring with
  checksum wording in the same row — a synthetic value by
  construction, not a leaked checksum. The `FAKE_` prefix is the
  declaration; treating it as a real checksum would be a category
  error.
- **Keyword-wording rows (7 summary rows):** token-word 4 rows,
  api-key-word 2 rows, checksum-word + `FAKE_` shape 1 row. This
  matches the review's "5–7 cells depending on scan method" at the top
  of the range (7 rows under the broadest keyword set). These are
  descriptions or test labels, not credentials. Count only.
- **Long-run check:** 5 summary rows contain a ≥20-character non-URL
  alphanumeric run; 2 of them are also keyword rows. Length alone is
  not a key — slugs, hashes, and fragments share it. A long
  base64-alphabet run pattern matches 3 rows, but a match inside a
  URL is a locator fragment, not a standalone blob; no standalone
  encoded payload is established. No key-shaped value was found.
- **Epoch-suffixed names (34 names):** a 10-digit Unix-time-shaped
  suffix. Predictable, low-entropy, and in the name position — a
  timestamp marker / batch correlator, not a secret. 12 of the 34 sit
  in payload-string rows; the rest are marker-only.
- **Hex-suffixed probe names (18 names):** an 8-lowercase-hex suffix
  (32 bits). Too short for a key, in the name position, shared across
  probe families — a run/batch identifier, not a credential. 9 of the
  18 sit in payload-string rows.
- **Fuzz-list author (1 row):** a single author cell carrying 151
  tokens (next-longest author cell: 4 tokens). This is a fuzzer-input
  shape — a list blasted into one field — not a payload, not a secret,
  and not 151 authors. It is evidence of field-fuzzing behaviour in
  the metadata, nothing more.
- **Webhook-exfil summaries:** 6 summaries use the word "webhook";
  3 names use an exfil-related word; 1 summary uses a callback word.
  These are self-descriptions of a test ("this gem tests webhook
  exfiltration") — they assert an intent, they do not evidence an
  exfiltration event. A summary that SAYS exfiltration is weaker
  evidence than a receiver log and stronger evidence than nothing
  about claimed intent only.

## 4. What would upgrade each shape to observed behaviour

| Shape | Upgrade artifact (exact) | What it would show |
|---|---|---|
| OAST callback | Receiver-side interaction log for that OAST host/identifier: timestamped DNS query and/or HTTP hit, with source IP and requested path, from the OAST operator's own log | That SOMETHING resolved/fetched the identifier, when, and from where — still not by itself who or why |
| OAST callback (stronger) | The same log entry correlated to a renderer: e.g. a registry/mirror request log showing the gem page render that triggered the fetch, or a crawler log | That the fetch was caused by rendering/following the metadata, not by the publisher self-pinging |
| Webhook callback | Webhook.site bucket request log for that path token: timestamped POST with headers/body, or the bucket's "no requests received" state | Receipt (or its absence) — the single fact that decides QA-vs-exfiltration framing for that bucket |
| SSRF / internal target | Target-side or intermediary-side request log: a fetch from a registry/mirror/crawler IP to the internal address, or a cloud metadata service access log | That a server-side fetch was attempted and what it returned; without it, the URL is inert text |
| SSRF / internal target (stronger) | Response evidence: returned metadata content, or an error/timeout record for that fetch | Impact — whether the fetch succeeded, not merely that it was attempted |
| XSS markup | A rendered page capture (screenshot or DOM dump) showing the summary field rendered as live markup, or a victim-browser execution artifact | That the renderer failed to escape the field — the renderer is the vulnerability, the string is only the input |
| XSS markup (stronger) | An execution receipt: alert-dialog capture, exfiltrated-cookie arrival at a receiver, or a CSP/report log entry tied to the gem page | That code actually ran in a real browser |
| SSTI / template | A rendered output showing the evaluated result (e.g. the arithmetic computed) instead of the literal expression, from the page that displays the summary | That an engine evaluated the string |
| SSTI / template (stronger) | Engine error log or response timing/content proving evaluation server-side, with the gem summary as the input | Which engine and where evaluation happened |
| Author-field payload | Same as XSS/SSTI, but for the author render path specifically (author field rendered unescaped / evaluated) | Author-field rendering is a separate code path and must be proven separately — summary proof does not transfer |
| YAML / traversal / regexp (all 0 in CSV) | The artifact that could carry them: gem tarball bytes + gemspec for YAML/traversal; the consuming parser's input for regexp | These shapes cannot be upgraded from this CSV at all — the CSV is the wrong artifact. Fetch the gem bytes (read-only, never execute) and inspect statically |
| Epoch / hex name markers | Publication-time correlation: the suffix value against the row's first-published timestamp, and suffix reuse across rows/authors | Whether the suffix IS the publish time (batch marker) or an independent run ID — a correlator, never a behaviour proof |
| Keyword / FAKE_ / long-run rows | The gem's code or a receiver log, as applicable | Whether any token-shaped string was ever a live credential — the CSV alone cannot answer this, and the `FAKE_` row already answers itself (synthetic) |
| Name-only probe labels | A link, receipt, or code artifact tied to the named gem (see rows above) | Whether the label's claimed test ever ran |

## 5. Standing caveats for the integrated report

1. String presence is not execution, receipt, victim, or authorship —
   for EVERY shape in §1, without exception.
2. The strongest claim this file supports about the payload rows is:
   "someone published registry metadata carrying probe-shaped strings
   in July 2026, concentrated on July 7, in the tester probe family
   and adjacent rows." Agent authorship is not in this file: no model,
   harness, tool call, prompt, or session artifact exists in any of
   the 20 columns.
3. The QA-vs-malicious question is UNDECIDABLE from this file for the
   OAST/webhook rows. Both hypotheses predict exactly the same string.
   Only receiver logs break the tie, and they are not in evidence.
4. Do not quote the 24-row IP set as "24 internal targets" — 10 of the
   24 are public-IP homepages and 1 of the 24 is summary text, not a
   link field. Quote the split (§1, shapes 3/3a).
5. Do not quote the 6 OAST hosts as 6 independent operators — 1 host
   carries 22 of 29 rows and there are only 4 base domains. Host
   diversity here is low.
6. Do not treat the `*` in template arithmetic as a YAML alias, the
   `FAKE_` row as a leaked checksum, a probe name as a successful
   probe, or a long alphanumeric run as a key. Each is a known
   misreading this lane checked for and rejected.
