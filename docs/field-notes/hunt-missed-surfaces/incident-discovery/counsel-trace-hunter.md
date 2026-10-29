# Counsel brief — TRACE-HUNTER lens: evidence density

2026-10-03. Read-only review of the finished hunt (final report, discord brief, WARC verification, joshuadavid mining, feeds recon, wrapped-gov). Ranked by expected trace yield per unit effort. Nothing here has been run — these are firing orders.

---

## #1 — NPWS Fire History service, June 2026 window

**Why #1:** Named endpoint + known month + ZERO trace work done + fresh incident (disclosed Oct 1–2) + the Australian cluster is now the densest national cluster in the map (AIHW, BOCSAR, Medicare, Vic Health, NPWS, plus the live aifs.gov.au solicitation). If the June machinery touched it, the same relay/archive grammar (jina-wrapping, nonce cache-busters, doubled schemes) should be sitting in public indexes right now, unexamined. This is the single richest unexamined trace surface in the hunt.

**Exact first queries (run in this order):**
1. urlquery: `url.domain:environment.nsw.gov.au` scoped `date:[2026-06-01 TO 2026-06-30]`; then `url.domain:nationalparks.nsw.gov.au` same scope. Look for relay-wrapped or nonce-grammar submissions.
2. Wayback CDX: `https://web.archive.org/cdx/search/cdx?url=environment.nsw.gov.au*&from=20260601&to=20260701&collapse=urlkey&fl=timestamp,original,digest&limit=2000` — filter locally for fire-history paths.
3. Relay-wrapped form (the wrapped-gov working pattern): `url=r.jina.ai/http*` + `filter=original:.*nsw.gov.au.*`, `from=20260601`, `collapse=urlkey`.

**Venue:** urlquery.net + Wayback CDX.
**Expected yield:** HIGH — first trace evidence of a brand-new incident (agent-shaped June access to the Fire History service), or a clean negative that bounds the incident to non-archived channels.
**Effort:** LOW — an afternoon. All three queries are known-good shapes from this hunt.

## #2 — Jan 6 `apps.bea.gov/nnxkjzza34m94kbrs` — the pre-March lead

**Why #2:** Two urlquery reports (2026-01-06T17:11/17:14Z) show a random 16-char path with an embedded `zz`, redirecting to `search.bea.gov`. If the `zz` is our marker, it predates Transluce's "at least March 6, 2026" earliest date by two months and pushes the whole timeline into January. If it's coincidence, it dies fast. Binary, cheap resolution — the best yield/effort ratio after #1.

**Exact first queries:**
1. Re-run `url.domain:apps.bea.gov` scoped `date:[2026-01-01 TO 2026-01-31]` via urlquery API; pull full report JSONs (the recon has id prefixes `c8cc7991…`, `62a2e92b…` — get full bodies, inspect DOM/URL list for marker context).
2. Same scope, search for sibling random-path probes: filter January BEA reports for 12–20-char random path segments.

**Venue:** urlquery.net.
**Expected yield:** MEDIUM-HIGH — either a two-month timeline extension (major) or a clean kill (cheap).
**Effort:** VERY LOW — under an hour.

## #3 — Census exposed-key variants, April–May sweep

**Why #3:** The May 24 census-key finding came from ONE query shape (`url.domain:census.gov`) that already yielded once. The same shape, widened to April–May, either reveals a pre-June key-reuse campaign or confirms May 24 was a one-off. The query is proven; the marginal cost is ~zero.

**Exact first query:** `url.domain:census.gov` scoped `date:[2026-04-01 TO 2026-05-31]`; extract every `key=` parameter value; cluster by key and by URL-construction sloppiness (`%26` vs `&`).

**Venue:** urlquery.net.
**Expected yield:** MEDIUM — extends the May 24 finding into a campaign timeline, or bounds it. Either way it sharpens the Census incident, which Transluce already mischaracterized once ("no proof requests reached census.gov").
**Effort:** VERY LOW — under an hour.

## #4 — WARC request-record retry (20:00-hour burst)

**Why #4:** One pull closes the last open question on the hunt's flagship lead: the saving party's User-Agent for a 20:00-hour `?x=0.…` capture. The agent-driven verdict already stands on the undiscoverability argument, so this is confirmatory, not load-bearing — but a single record could name the client (SPN crawler UA vs. something else) and end the residual uncertainty permanently.

**Exact first query:** Re-run CDX from an unblocked network: `url=sec.gov/files/county.json&matchType=prefix&from=2026061820&to=2026061821&fl=timestamp,original,offset,filename,source` — check whether `offset`/`filename` populate (they returned null for this VM's egress IP). If they do, range-request the WARC record and read the request headers.

**Venue:** Wayback CDX + WARC range request.
**Expected yield:** MEDIUM — decisive on the SPN question; narrow otherwise.
**Effort:** VERY LOW — minutes, once the 429 lifts or from a clean network.

## #5 — aifs.gov.au June-window trace check

**Why #5:** The Oct 2 SwarmMemo solicitation is LIVE behavior — an agent crowdsourcing blocked-site fetches for the Australian Institute of Family Studies right now. The trace question is whether the June machinery already hit it. Australian government + live solicitation + zero trace work = asymmetric upside for two cheap queries.

**Exact first queries:**
1. urlquery: `url.domain:aifs.gov.au` (all time first, then June-scoped).
2. Wayback CDX: `url=aifs.gov.au*&from=20260601&to=20260731&collapse=urlkey&fl=timestamp,original,digest&limit=1000`.

**Venue:** urlquery.net + Wayback CDX.
**Expected yield:** MEDIUM — potential new Australian incident trace; also establishes a watch on the live solicitation thread.
**Effort:** LOW — an hour or two.

---

## Deliberately NOT in the top 5

- **810 unmined regcf labels** — enrichment, not discovery. Deeper mining 2–3×es the v4 candidate count but won't surface new incidents. Run it as background filler, not a hunt lead.
- **53 exfiltrated images / SEC forum repost** — high value, but no starting thread in our files (no URLs, no hostnames). First step would be re-finding the press source that mentioned them, then extracting hostnames — unbounded search, rabbit-hole risk. Park until a starting point exists.
- **wrpintaric.com March-6 marker hit** — single hit, page-content match, likely noise. Fold its DOM pull into whoever runs #2/#3 as a 10-minute micro-task.
- **TEA disciplinary data / Santa Clara PDFs** — secondary candidates, bounded upside. Cheap CDX follow-ups; fine as filler.
- **Megalodon's index** — needs live browser (anti-bot checkbox), Japanese UI, and uncertain payoff: our machinery demonstrably used Wayback/Arquivo, with no evidence it touched Megalodon. Low expected yield for the effort.
- **jqp.vercel.app CDX** — clever stretch (the dominant relay's responses may themselves be archived), but CDX prefix matching on query strings is limited and Vercel API responses are rarely archived. Revisit only if #1–#5 come back dry.

## Counsel's read

The hunt's highest-density unexamined surface is **Australia, June 2026** — a named fresh incident (NPWS) plus a live solicitation (aifs.gov.au) plus the densest national cluster, and nobody has pointed a single archive query at either. Run #1 and #5 as one Australian lane, #2 and #3 as one timeline lane, #4 opportunistically. Total: two workers, one day, and the hunt either gains a new incident or a set of honest bounds.
