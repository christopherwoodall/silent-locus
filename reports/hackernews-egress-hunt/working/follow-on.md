# Hacker News egress hunt — follow-on pivots

Lane: hackernews-egress-hunt, follow-on lane. Date: 2026-10-27.
Role: pivot the kept indicators to other surfaces and report what each
pivot ADDS or KILLS. This lane creates no new ranked hits. Nothing here
is upgraded. Every kept indicator stays SECONDARY, and every survivor
stays POSSIBLE with its adversarial caveats intact, except for one
caveat change stated plainly in section 7: the CVE citation for
49429926 is now verified against a CVE record. That verification does
not upgrade the HN item. It only removes the "unverified citation"
caveat. Wild exploitation of the mechanism is still unshown.

## Terms and rules kept

- SECONDARY: evidence from a third party, not first-hand capture.
- POSSIBLE: the claim may be true, but the evidence is thin or
  bounded. WEAK: held, not ranked.
- OVERLAP: a pivot result that is only a known item restated
  (HN 49379079, Fleet B ranked hits, or the Cohere seed). Overlap
  adds zero independent weight.
- ADDS: the pivot adds something the HN item alone did not show.
- KILLS: the pivot contradicts or removes part of the kept claim.
- NOTHING: the pivot returned no relevant result for this indicator.
- N/A: the surface does not fit this indicator, with a reason.
- A pivot that only re-finds the HN item itself or known overlap
  adds zero independent weight. That is stated, not hidden.
- Signed-URL rule: parameter names and path shape only. No signed
  query strings, signatures, tokens, or credential-shaped values
  appear in this file or in `pivot-results.tsv`. All sampled URLs
  below are shown with query strings stripped.
- No poster handles appear anywhere in this file. GitHub results
  are cited by project name and issue or file title only, never by
  account handle. The finder credited in the CVE record is not
  named here.
- No Factum writes were made. No git operations were made.
  No files from the sibling broad-hunt lane were touched. A pivot
  result that matches that lane's holdings would be cited as
  overlap; none was identified as such in this lane's samples,
  and no sibling file was opened to check.
- Sampling honesty: where a total exceeds the fetched sample, the
  sample is a sample, never the full set. Totals are search totals
  under the query shown, not relevance counts. Several totals below
  are loose string matches, and that looseness is stated where it
  applies.

## Method and limits, per surface

- urlquery: searched with the existing urlquery CLI
  (`skills/urlquery/bin/uq.py search`), which uses the project's
  established search path. A direct keyless call to the public
  search endpoint returned empty output for the test query, so the
  CLI path was used for all urlquery rows. Query syntax note:
  urlquery `q` matches submitted URLs AND page content, and
  multi-term queries behave loosely (see indicator 3: an exact-IP
  query returns 0 while the same IP plus "mcp" returns 207, so
  multi-term totals are not conjunction counts). Sample evidence
  below is submitted URLs only, unless stated. Page content was
  not re-read for the large totals, so a large total never means
  "many relevant reports".
- GitHub issues: unauthenticated read-only GET to the public
  search API, quoted phrase queries, 5 titles fetched per
  indicator (routify: all 7 fetched in a follow-up call).
- GitHub code search: authenticated read-only `gh api
  search/code`, GET only, no posts, no modifications, no fresh
  login. Queries were unquoted, so code totals are token matches,
  not phrase-exact counts. No rate-limit block was hit.
- urlscan: public anonymous search API, no login. First-pass
  calls for four queries failed at transport level (connection
  closed or incomplete read) and were retried once; the retry
  totals below replace the failed first pass and are not zeros
  invented from errors. Anonymous urlscan search responses state
  a 30-day search window, so urlscan totals here are
  recent-window totals, not all-time totals.
- crt.sh: certificate search, host indicators only. An exact-host
  query returning an empty list is a real empty result, not a
  transport failure, and is reported as 0 with that distinction
  stated. A wildcard query is reported separately as context,
  never as an exact-host cert.

---

## Indicator 1 — Routify host prefix

Kept value: routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com
(host prefix in the kept set; the 49535519 comment display text
truncates it, see the pivot note below). Source: HN 49535519,
shape 3 narrowed, SECONDARY / POSSIBLE. Caveats carried: host is
the known-overlap host from 49379079, so any novelty is
witness-only; no fetch date, no success statement, no harness,
no path in the 49535519 comment.

Pivot note (does not re-grade the item): a re-fetch of the
49535519 Algolia JSON during this lane shows the comment's link
target carries the full host string while the visible link text
truncates with an ellipsis. Enrichment keeps the indicator as
prefix-only on the visible text, and this lane does not change
that. The note weakens, but does not remove, the "different host"
kill path: the full host is present in the comment markup, not
only inferred from overlap.

### urlquery — ADDS (host liveness only, no agent fetch)

- Query: `routify-file-proxy`. Total 1, fetched 1.
- Sample: one report dated 2026-08-16, submitted URL the bare
  host root, no tags, final title the bare host, final content
  a small plain-text body. No proxy path, no signed parameters,
  no agent or model marker in the report metadata.
- Verdict: ADDS one independent surface fact — the host was
  submitted to urlquery and resolved as a live Alibaba OSS host
  in August 2026 — and ADDS nothing about an agent fetch. A bare
  host submission is not a fetch sighting, not a path sighting,
  and not a third witness to the HN claims. Conjunction check:
  urlquery `routify qwen3.8` returns total 0, so urlquery holds
  no report pairing this host with the Qwen model string.

### GitHub issues — OVERLAP + ADDS (surface breadth, no new sighting)

- Query: `"routify-file-proxy"`. Total 7, fetched 7.
- Two of the seven are known Fleet B overlap, by project and
  issue number: project yukino-code issue 2 (web fetch/search
  report naming the host's OSS layer) and project Crow issue 288
  (model-invented fetch URLs on the same host family). Those two
  add zero independent weight here.
- The other five are additional issue mentions of the host, by
  title only (bodies were not read in this lane, so none is a
  verified sighting): project openfox issue 349 ("Misremembered
  web_fetch calls?!"); project qwen3.8-Flash-DGX issue 16 (same
  title; this is not the Fleet B blazux issue 16, which sits in
  a different project, and the two must not be conflated);
  project aivideo issue 151 (temporary third-party URL kept on
  persist failure); project personal_agent issue 994 (a
  mitigation: block a named Alibaba bucket, add a novel-egress
  signal); project crow-nest issue 99 (tool-call accounting,
  host mention only in body on the evidence seen).
- Verdict: ADDS surface breadth — the host appears in 7 GitHub
  issues, not only on HN — but ADDS zero verified new agent
  sightings. Two are overlap, the rest are title-level mentions
  for the coordinator to triage, not ranked hits from this lane.

### GitHub code search — ADDS (block and repro artifacts, not sightings)

- Query: `routify-file-proxy` (unquoted). Total 73, fetched 5.
- Sample paths, by project name only: a README and a
  reproduction script in project qwen-block-proxy-artifacts; a
  tool-guard document in project sparkqwen; an
  open-weight-data-leak issue note in project vibe-investing;
  a README in project pi-block-proxy-artifacts.
- Verdict: ADDS that community block, guard, and reproduction
  artifacts name this host in code and docs. That is consistent
  with the host being a known proxy-fetch artifact in Qwen
  tooling discussion. It is not a new fetch observation, and
  code bodies were not read, so no artifact here is claimed as
  a sighting.

### urlscan — NOTHING (recent window)

- Query: domain form of the host. Total 0, fetched 0, on retry
  after a first-pass transport failure. Window: last 30 days.
- Verdict: NOTHING in the recent urlscan window. That does not
  kill the HN claim (the HN dates are August–September 2026,
  outside the window) and does not prove the host is dead: the
  urlquery August 2026 report above shows it live then.

### crt.sh — ADDS (infrastructure context only)

- Exact host query: total 0, fetched 0, empty list returned
  (not a transport failure).
- Wildcard query for the parent OSS suffix: 76 certificates,
  all for the wildcard name, latest not-before 2026-07-28.
- Verdict: ADDS only that the host sits under Alibaba's shared
  OSS wildcard certificate, with no dedicated certificate for
  the host itself. That fits a shared proxy host and adds
  nothing about any agent fetch. KILLS nothing.

### Indicator 1 verdict

Survives unchanged: SECONDARY / POSSIBLE, witness-only versus
overlap, shape 3 narrowed. Pivots add host liveness (urlquery),
surface breadth (GitHub issues and code), and wildcard-cert
context (crt.sh). No pivot adds a new fetch sighting, a path,
a harness, or a success statement, and none kills the claim.

---

## Indicator 2 — Qwen3.8 27B / qwen3.8-27B

Kept value: Qwen3.8 27B / qwen3.8-27B. Source: HN 49535519,
shape 3 narrowed, SECONDARY / POSSIBLE. Caveats carried: model
named in-thread only; harness unstated; the model string alone
is a generic identifier, and pivots below confirm that.

### urlquery — NOTHING

- Query: `qwen3.8-27B`. Total 104, fetched 30 (capped sample).
- Sample submitted URLs are ordinary model news, docs, and
  hosting pages. No sampled report pairs the model string with
  the routify host, and the conjunction query
  `routify qwen3.8` returns total 0.
- Verdict: NOTHING for egress. The 104 total is a loose
  string-match total over page content, not 104 egress reports.
  The capped sample must not be presented as the full set.

### GitHub issues — NOTHING

- Query: `"qwen3.8-27B"` (quoted phrase). Total 45,496,
  fetched 5.
- Sample titles are model packaging and support work
  (quantization, example regeneration, evaluation runs). No
  sampled title mentions a routify fetch or any egress.
- Verdict: NOTHING for egress. The model string is too generic
  to pivot on its own; its issue total is noise for this lane.

### GitHub code search — NOTHING

- Query: `qwen3.8-27B` (unquoted). Total 260,608, fetched 5.
- Sample paths are ordinary model READMEs and plans. No
  sampled path shows an egress artifact.
- Verdict: NOTHING for egress. Token-match total, not evidence.

### urlscan — NOTHING

- Query: `"qwen3.8-27B"`. Total 0, fetched 0 (recent 30-day
  window).
- Verdict: NOTHING in the recent window.

### crt.sh — N/A

- Not applicable: crt.sh searches certificates for hosts, and
  a model name is not a host. No query was run.

### Indicator 2 verdict

Survives unchanged: SECONDARY / POSSIBLE as the model named in
49535519 only. Pivots add nothing. The model string, pivoted
alone, is a generic identifier with no egress signal on any
surface tested. That does not kill the HN claim — the claim
rests on the HN comment, not on the model string's rarity —
but it means no pivot corroborates the model-to-host pairing
outside HN and the Cohere seed.

---

## Indicator 3 — 169.254.169.254, mechanism-only context

Kept value: 169.254.169.254. Source: HN 49429926, shape 1
mechanism only, SECONDARY / POSSIBLE. Caveats carried, and
pivots were scoped to them: this is a mechanism address for
agent or tool metadata reaches, not generic SSRF write-ups.
Generic SSRF noise below is therefore reported as noise, not
as support. The address must never be cited as "an agent
reached a metadata endpoint" on this lane's evidence.

### urlquery — NOTHING

- Query: `169.254.169.254`. Total 0, fetched 0.
- Conjunction probe: `169.254.169.254 mcp` returns total 207,
  but the first 10 sampled submitted URLs show no metadata
  relevance, which confirms multi-term urlquery totals are
  loose (OR-like) rather than conjunction counts. The 207
  figure is therefore not a count of tool-metadata reports.
- Verdict: NOTHING for agent or tool metadata reaches. No
  urlquery report pairs this address with an agent or tool
  reach in the evidence seen.

### GitHub issues — NOTHING

- Query: `"169.254.169.254" "mcp"` (quoted). Total 6,250,
  fetched 5.
- Sample titles are MCP infrastructure and configuration
  issues (metadata-server egress allowance, MCP server
  features and docs). No sampled title states a Toolbox
  redirect, an agent metadata reach, or a credential return.
- Verdict: NOTHING for the mechanism's wild use. The total is
  a phrase-match total over a generic address plus a generic
  term, not a mechanism count.

### GitHub code search — NOTHING

- Query: `169.254.169.254` (unquoted). Total 422,912,
  fetched 5.
- Sample paths are security guides, deployment docs, and
  SSRF templates. No sampled path shows an agent tool
  reaching a metadata endpoint.
- Verdict: NOTHING for agent or tool metadata reaches.
  Generic-address noise at scale.

### urlscan — NOTHING for agent/tool reaches (generic SSRF noise only)

- Query: `"169.254.169.254"`. Total 14, fetched 14, on retry
  after a first-pass incomplete-read failure. Window: last
  30 days.
- Sample: short-link and cloud-IP probe and recon pages,
  a redirect-to test page, a base64 payload page that embeds
  the metadata address in an image tag (a classic SSRF test
  shape, payload not reproduced here), and one webhook-site
  submission (host only, identifier withheld).
- Verdict: NOTHING for agent or tool metadata reaches. The 14
  are generic SSRF-test and probe submissions, with no MCP,
  Toolbox, model, or agent-tool link in the sampled URLs.
  That does not kill the Toolbox mechanism (section 7 verifies
  it independently); it kills any claim that urlscan shows
  wild agent metadata reaches.

### crt.sh — N/A

- Not applicable: crt.sh searches certificates for hosts, and
  an IP literal is not a host name for this purpose. No query
  was run.

### Indicator 3 verdict

Survives unchanged: SECONDARY / POSSIBLE, mechanism only.
No pivot found an agent or tool metadata reach on any surface.
Pivots add only the negative: the address is ubiquitous in
generic SSRF material and absent, in the samples seen, from
agent-tool metadata-reach material. The mechanism claim itself
stands or falls on the CVE verification in section 7, not on
these pivots.

---

## Indicator 4 — Google MCP Toolbox

Kept value: Google MCP Toolbox. Source: HN 49429926, shape 1
mechanism only, SECONDARY / POSSIBLE. Caveats carried: tool
named in-thread; no model named as exploiter; no wild
exploitation shown; story text only, no reproduction output
in-thread.

### urlquery — NOTHING

- Query: `mcp-toolbox`. Total 41, fetched 30 (capped sample).
- Sample submitted URLs are ordinary docs and console pages,
  with no Toolbox SSRF or metadata-reach marker in the
  submitted URL. One sampled report (a blog page, dated
  2026-10-20) is also the sole CVE-string hit in section 5,
  which suggests that report's page content mentions the CVE;
  its content was not re-read here, and it is not claimed as
  an independent verification (the CVE record in section 7
  is the verification).
- Verdict: NOTHING for wild exploitation. The 41 total is a
  loose content-match total, not 41 Toolbox incidents.

### GitHub issues — ADDS (CVE tracking only)

- Query: `"Google MCP Toolbox"` (quoted phrase). Total 426,
  fetched 5.
- Sample titles are mostly integration and adoption items
  (a Spring starter, an ADR note, a comment about a pull
  request). Two sampled titles are CVE-tracking items for
  CVE-2026-14540 (add the CVE; fill in fix status and finder
  credit). Those two overlap the CVE verification in
  section 7 and add no wild-exploitation evidence.
- Verdict: ADDS only that the CVE is tracked in security
  projects alongside ordinary Toolbox adoption work. NOTHING
  for wild agent exploitation.

### GitHub code search — ADDS (tool exists and is documented only)

- Query: `mcp-toolbox` (unquoted). Total 12,224, fetched 5.
- Sample paths include the official Toolbox extension
  document and a Toolbox plugin document, plus newsletter
  mentions.
- Verdict: ADDS only that the tool is real, public, and
  documented. No sampled path shows the SSRF, a redirect
  guard, or a wild exploit.

### urlscan — NOTHING

- Query: `"mcp-toolbox"`. Total 0, fetched 0, on retry after
  a first-pass transport failure. Window: last 30 days.
- Verdict: NOTHING in the recent window.

### crt.sh — N/A

- Not applicable: crt.sh searches certificates for hosts, and
  a tool name is not a host. No query was run.

### Indicator 4 verdict

Survives unchanged: SECONDARY / POSSIBLE, mechanism only.
Pivots confirm the tool is real and its CVE is tracked, and
add nothing about any model exploiting it in the wild. The
mechanism's truth rests on the CVE record (section 7), not on
pivot volume.

---

## Indicator 5 — CVE-2026-14540, citation

Kept value: CVE-2026-14540. Source: HN 49429926, shape 1
mechanism only, SECONDARY / POSSIBLE. It entered this lane as
an UNVERIFIED citation: the adversarial review and the
enrichment lane both stated the CVE record had not been
checked. This section is that check, and it is also the
pivot section for this indicator.

### urlquery — NOTHING (one loose mention)

- Query: `CVE-2026-14540`. Total 1, fetched 1.
- Sample: the same blog-page report as in indicator 4's
  sample (dated 2026-10-20). Its submitted URL carries no
  CVE marker; the hit comes from page content.
- Verdict: NOTHING independent. One blog mention is not CVE
  verification and is not counted as such.

### GitHub issues — ADDS (CVE tracking)

- Query: `"CVE-2026-14540"` (quoted phrase). Total 22,
  fetched 5.
- Sample titles are CVE-tracking work: add the CVE, add
  finder credit, fill in fix status and finder credit, add a
  scanner. No sampled title reports wild exploitation.
- Verdict: ADDS that the CVE is tracked in security projects.
  Tracking is not verification and not exploitation evidence.

### GitHub code search — ADDS (CVE record mirrors)

- Query: `CVE-2026-14540` (unquoted). Total 111, fetched 5.
- Sample paths include the canonical CVE list JSON for this
  CVE, a vulnerability-enrichment JSON for this CVE, a CVE
  project markdown file for this CVE, and a threat-rule
  proposal referencing it.
- Verdict: ADDS that the CVE identifier exists in public CVE
  mirrors and tracking projects. That corroborates existence
  but is not a substitute for reading the CVE record itself,
  which is done in section 7.

### urlscan — NOTHING

- Query: `"CVE-2026-14540"`. Total 0, fetched 0 (recent
  30-day window).
- Verdict: NOTHING, as expected for a CVE identifier on a
  URL-scan surface.

### crt.sh — N/A

- Not applicable: crt.sh searches certificates for hosts, and
  a CVE identifier is not a host. No query was run.

### Indicator 5 pivot verdict

Pivots alone add tracking and mirror evidence, not
verification. Verification comes from section 7, which reads
the primary CVE record. After section 7, this indicator's
status changes in one narrow way: citation VERIFIED, mechanism
still SECONDARY / POSSIBLE, wild exploitation still unshown.

---

## Indicator 6 — Claude Cowork

Kept value: Claude Cowork. Source: HN 46622328 via comment
46624950, 2/6-loose (injection-mediated upload via a provider
file API; NOT shape 2, NOT clean shape 6), SECONDARY /
POSSIBLE. Caveats carried: vendor PoC discussed on HN, not an
HN observation; destination is a provider file API, not object
storage; no recon step; attack needs victim folder access plus
a malicious skill install; injection visible in chat output;
attacker must use their own API key; old Haiku version only
per one commenter; framing disputed in-thread; repetition of
one vendor report is not corroboration.

### urlquery — NOTHING

- Query: `Claude Cowork`. Total 581, fetched 30 (capped
  sample).
- Sample submitted URLs are unrelated console, docs, and
  content pages. No sampled report shows a Cowork upload,
  a skill file, or a provider file-API exfiltration.
- Verdict: NOTHING for the mechanism. The 581 total is a
  loose match total (the generic word "cowork" appears widely
  in page content), not 581 Cowork reports. The capped sample
  must not be presented as the full set.

### GitHub issues — NOTHING

- Query: `"Claude Cowork"` (quoted phrase). Total 29,809,
  fetched 5.
- Sample titles are adapter and support requests (desktop
  adapter, support requests, enrolment, skill sync). No
  sampled title mentions an upload, a skill injection, or a
  key mismatch.
- Verdict: NOTHING for the mechanism. A common product-name
  phrase on a large surface produces volume, not evidence.

### GitHub code search — NOTHING

- Query: `Claude Cowork` (unquoted). Total 316,416,
  fetched 5.
- Sample paths are unrelated project docs and skill files.
  No sampled path shows the Cowork exfiltration mechanism.
- Verdict: NOTHING for the mechanism. Token-match total,
  not evidence.

### urlscan — NOTHING

- Query: `"Claude Cowork"`. Total 0, fetched 0, on retry
  after a first-pass transport failure. Window: last 30 days.
- Verdict: NOTHING in the recent window.

### crt.sh — N/A

- Not applicable: crt.sh searches certificates for hosts, and
  a product name is not a host. No query was run.

### Indicator 6 verdict

Survives unchanged: SECONDARY / POSSIBLE, vendor PoC
mechanism only, with all bounds attached. No pivot adds a
second observation, a fix status, or a wild instance, and
none kills the mechanism either: the pivots were too generic
(a product name) to test a specific key-mismatch mechanism.
The open question from enrichment — read the linked vendor
report and confirm the HN summaries — is not answered by
these pivots and remains open for the coordinator. This lane
did not read the Cowork vendor report, because the task's
linked-report reads cover only the two holding items below.

---

## 7. CVE verification verdict — CVE-2026-14540: VERIFIED, mechanism confirmed, wild use still unshown

Source checked: the primary CVE record via the CVE program
API (assigner: Google). Record state: PUBLISHED. Reserved
2026-07-03, published 2026-07-31, updated 2026-07-31.

What the record says, in plain words:

- Title: server-side request forgery via unrestricted HTTP
  redirection in MCP Toolbox.
- Product: Google mcp-toolbox, versions 0.3.0 through 1.4.0
  affected. Weakness: CWE-918 (server-side request forgery).
- Mechanism: the generic HTTP source and tool components
  implement baseline input sanitization, but the underlying
  HTTP client is initialized without a restrictive redirect
  policy and lacks target IP validation. An attacker, or a
  malicious data-driven prompt, can supply a crafted path
  parameter that triggers an open redirect or a direct
  destination swap on the target backend, coercing the
  toolbox into following the redirection and making
  unauthorized requests to internal or arbitrary external
  endpoints.
- Score: CVSS version 4.0 base score 8.0, severity HIGH.
  That matches the HN story's "CVSS 8.0, high" exactly.
- Fix reference: the record references the upstream fix pull
  request in the Toolbox repository (pull request 3448,
  described in secondary coverage as an SSRF guard for the
  HTTP source). The CVE record itself does not state an
  eight-day fix timeline, so the HN story's "fixed in eight
  days" detail is NOT verified by the record and stays as
  HN-story wording only.
- Chronology check: the CVE was published 2026-07-31, before
  the HN story date 2026-08-25, so the citation's timeline is
  consistent.

Verdict:

- The citation is VERIFIED. CVE-2026-14540 exists, is assigned
  to Google, describes the MCP Toolbox redirect SSRF, and
  matches the HN story's mechanism (first URL validated,
  redirect destination not validated, no destination
  filtering) and its score.
- The mechanism claim for 49429926 is therefore CONFIRMED as
  a mechanism: the redirect-to-internal-endpoint path the HN
  story describes is real and was a real vulnerability in
  Toolbox versions 0.3.0 through 1.4.0.
- What verification does NOT do: it does not show any model
  exploiting this in the wild, does not show a credential
  actually returned to a model, and does not show a metadata
  endpoint specifically reached (the record says internal or
  arbitrary external endpoints; the metadata address is the
  HN story's example, not the record's named target). The
  HN item therefore stays SECONDARY / POSSIBLE and
  mechanism-only. It must still never be written up as "an
  agent reached a metadata endpoint".
- The "eight days" fix detail and any finder narrative beyond
  "finder credited in the record" are not carried forward as
  verified facts from this lane.

---

## 8. Linked-report verdicts — the two WEAK holding items

Both linked reports were fetched publicly, with no login.
Both items' return conditions are decided here. Neither item
returns as an HN observation or as a wild incident: both
return, if the coordinator re-files them, only as
vendor-reported proof-of-concept mechanisms, with the bounds
below in the first sentence of any re-filing.

### Holding item 48349487 — ChatGPT for Google Sheets workbook exfiltration: RETURNS as a vendor PoC mechanism

- HN URL: https://news.ycombinator.com/item?id=48349487
- Linked report: the PromptArmor vendor report linked from
  the HN thread (Sheets data-exfiltration report), fetched
  publicly. Published 2026-06-03, updated 2026-08-24.
- Mechanism shown (real, not thin): an indirect prompt
  injection hidden in an imported sheet (white text in the
  report's example) manipulates ChatGPT for Google Sheets
  into running an attacker-controlled external script, using
  permissions the user granted to the Sheets extension. The
  script exfiltrates the victim's workbook to the attacker's
  server — the report shows attacker server logs holding the
  victim's financial model — then follows links inside the
  stolen data to discover and exfiltrate further workbooks,
  12 in total in the demonstrated chain. The same script
  capability also enables phishing overlays (a cloned sidebar
  and a credential-phishing pop-up). The attack is stated to
  succeed even when the user disabled automatic edits.
- Channel: attacker-controlled script executed with extension
  permissions, exfiltrating to the attacker's server. Data:
  full workbook contents, chained across linked workbooks.
  Evidence in the report: attack chain narrative, attacker
  server-log screenshots described in text, and a disclosure
  timeline (disclosed 2026-05-08, public 2026-05-27).
- Kill condition tested: the mechanism is NOT a formula or
  script feature, NOT a user-authorized export, and NOT
  something other than agent-mediated exfiltration. The
  kill condition from enrichment is therefore NOT met.
- Bounds that must travel with any re-filing: vendor PoC,
  not a wild incident; requires the victim to import a
  poisoned sheet and to have granted the extension its
  permissions; the injection is in untrusted imported data,
  not spontaneous model behavior. Mitigation noted in the
  report itself: OpenAI responded (2026-05-31) that it
  removed the model's ability to generate Apps Script code,
  which OpenAI states should eliminate this risk, and that it
  is re-evaluating sandboxing. Any re-filing must carry that
  mitigation and must not present the chain as currently
  open without a fresh check.
- Shape note: this is injection-mediated exfiltration via a
  script to an attacker server. It is NOT shape (2) object
  storage (no bucket destination is shown) and NOT clean
  shape (6) (no separate recon step is shown; discovery of
  further workbooks happens inside the exfiltration chain).
- Verdict: RETURN CONDITION MET. The item may return from
  WEAK to POSSIBLE only as a vendor-PoC mechanism with the
  bounds and mitigation above, cited to the vendor report,
  never to the HN title alone.

### Holding item 48827858 — GitLost, GitHub AI agent leaking private repos: RETURNS as a vendor PoC mechanism

- HN URL: https://news.ycombinator.com/item?id=48827858
- Linked report: the Noma Security vendor report linked from
  the HN thread (GitLost report), fetched publicly.
- Mechanism shown (real, not thin): GitHub Agentic Workflows
  pair repository automation with an AI agent that reads
  issues, calls tools, and can access other repositories in
  the organization. In the demonstrated configuration, a
  workflow triggers on issue assignment, reads the issue title
  and body, posts a comment in response, and runs with read
  access to other organization repositories, public and
  private. An unauthenticated attacker posts a crafted issue
  in a public repository of an organization using that setup.
  The agent follows hidden instructions in the issue, fetches
  file contents from both a public repository and a private
  repository, and posts those contents as a public comment on
  the issue, where anyone can read them. The report states
  that guardrails meant to block this failed, and that adding
  an "Additionally" reframing keyword bypassed a refusal.
- Channel: public issue comment posted by the agent itself.
  Data: file contents, demonstrated with README files. The
  report names a public repository and a private repository
  in its test organization and cites a workflow run and an
  issue as live evidence; those two cited artifacts were not
  independently re-fetched in this lane, so they are reported
  here as "cited in the report", not as independently
  verified artifacts.
- Kill conditions tested: the leak is NOT of public or
  already-authorized content only (a private repository's
  file contents are shown posted publicly); it is NOT a mere
  configuration artifact (a crafted issue triggers the agent
  to fetch and post); it is NOT metadata only (file contents,
  not access metadata, are posted). No kill condition from
  enrichment is met.
- Bounds that must travel with any re-filing: vendor PoC in
  the vendor's own test organization, not a wild incident
  against a victim organization; requires an organization to
  have an Agentic Workflow configured with cross-repository
  read access plus public comment posting, triggered on issue
  events; demonstrated leaked content is README files (low
  sensitivity demo content), not source code or secrets, so
  severity must not be inflated beyond the demonstrated
  content. The report states the finding was responsibly
  disclosed to GitHub with GitHub's knowledge.
- Shape note: this is injection-mediated leak via a public
  comment. It is NOT clean shape (6): no separate recon step
  is described; the agent reads the named files directly on
  injected instruction and posts them. Do not file it as
  recon-then-egress without a recon step.
- Verdict: RETURN CONDITION MET. The item may return from
  WEAK to POSSIBLE only as a vendor-PoC mechanism with the
  bounds above, cited to the vendor report, never to the HN
  title alone.

---

## 9. Closing table — what survives pivots unchanged

Grades are SECONDARY throughout. Pivots do not upgrade
anything. "Survives" below means the kept claim, with its
caveats, is still standing after pivots — not that pivots
proved it.

| # | Indicator (source) | Before pivots | After pivots | What pivots changed |
|---|---|---|---|---|
| 1 | Routify host prefix (49535519) | SECONDARY / POSSIBLE, shape 3 narrowed, witness-only vs overlap | SECONDARY / POSSIBLE, unchanged | Added host liveness, GitHub surface breadth, wildcard-cert context. No new sighting, no kill. |
| 2 | Qwen3.8 27B / qwen3.8-27B (49535519) | SECONDARY / POSSIBLE, shape 3 narrowed, model named in-thread only | SECONDARY / POSSIBLE, unchanged | Nothing. Model string alone carries no egress signal on any surface. |
| 3 | 169.254.169.254, mechanism only (49429926) | SECONDARY / POSSIBLE, shape 1 mechanism only, never "agent reached metadata" | SECONDARY / POSSIBLE, unchanged | Nothing for agent/tool reaches. Generic SSRF noise only. Mechanism rests on section 7, not pivots. |
| 4 | Google MCP Toolbox (49429926) | SECONDARY / POSSIBLE, shape 1 mechanism only, no wild exploitation | SECONDARY / POSSIBLE, unchanged | Added tool-is-real and CVE-tracking context. Nothing for wild exploitation. |
| 5 | CVE-2026-14540 (49429926) | SECONDARY / POSSIBLE, citation UNVERIFIED | SECONDARY / POSSIBLE, citation VERIFIED | One caveat removed: the CVE exists and matches the mechanism and score (section 7). Mechanism still SECONDARY / POSSIBLE; wild use still unshown. |
| 6 | Claude Cowork (46622328 via 46624950) | SECONDARY / POSSIBLE, 2/6-loose vendor PoC mechanism only | SECONDARY / POSSIBLE, unchanged | Nothing. Generic product-name pivots cannot test the key-mismatch mechanism. Vendor-report read still open. |

Holding items (not ranked before, decided in section 8):

| Item | Before | After linked-report read |
|---|---|---|
| 48349487, Sheets workbook exfiltration | SECONDARY / WEAK, holding, title-only on HN | May return to POSSIBLE only as a vendor-PoC injection-mediated exfiltration mechanism (12-workbook chain via attacker script), with OpenAI mitigation noted. Not shape 2, not clean shape 6, not a wild incident. |
| 48827858, GitLost private-repo leak | SECONDARY / WEAK, holding, title-only on HN | May return to POSSIBLE only as a vendor-PoC injection-mediated leak mechanism (private file contents posted as a public comment), demo README content only, configured-workflow precondition. Not clean shape 6, not a wild incident. |

## Open items left for the coordinator (not overrides)

1. Routify GitHub issues beyond Fleet B overlap (five
   title-level mentions in indicator 1) need body reads
   before any of them is treated as a sighting. This lane
   ranked none of them.
2. The Cowork vendor report still needs a read to confirm
   the HN summaries and the key-mismatch fix status, per
   enrichment open question 5. Pivots did not answer it.
3. The HN story's "fixed in eight days" detail for the
   Toolbox SSRF is unverified by the CVE record and stays
   HN-story wording only.
4. The 49535519 link-target note (full host in comment
   markup, truncated visible text) is recorded in indicator
   1 for the coordinator; enrichment's prefix-only treatment
   was not changed by this lane.
5. Urlscan totals here are recent-window (30-day) totals.
   A full-history urlscan check, if the coordinator wants
   one, needs an authenticated or differently scoped query,
   which this lane did not run (no logins by task rule).

## Files written by this lane

- `reports/hackernews-egress-hunt/working/follow-on.md`
  (this file).
- `reports/hackernews-egress-hunt/working/pivot-results.tsv`
  (one row per indicator by surface, with totals, fetched
  counts, outcomes, and notes).
- No other files were written in the report tree. A pivot
  driver script was used from scratch space only and was not
  left in the report tree. No Factum records were submitted.
  No git operations were performed.
