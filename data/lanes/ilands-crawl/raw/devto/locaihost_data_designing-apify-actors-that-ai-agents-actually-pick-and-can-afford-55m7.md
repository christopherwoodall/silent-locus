---
title: Designing Apify Actors that AI agents actually pick (and can afford)
url: https://dev.to/locaihost_data/designing-apify-actors-that-ai-agents-actually-pick-and-can-afford-55m7
published_at: 2026-10-10T13:21:05Z
edited_at: None
author: locaihost_data
tags: apify, ai, mcp, webscraping
reactions: public=0 positive=0 comments=2
---

---
title: "Designing Apify Actors that AI agents actually pick (and can afford)"
published: true
description: "What changes when your Actor's user is an AI agent calling it over MCP: input schemas, descriptions, failure modes, charge limits and pay-per-event accounting, with real code and a real call."
tags: apify, ai, mcp, webscraping
---

Most Apify Actors are built for a person who opens the Store page, reads the README, fills in a form and clicks **Start**. That person can scroll, guess and retry when something goes wrong.

More and more callers are no longer people. An agent in Claude, Cursor or a custom loop connects to the Apify MCP server, searches the Store, reads one short card about your Actor, builds a JSON input from your input schema and runs it with a spending cap. It never sees your README screenshots. It can't ask what "Max results" means. If the run fails, it may simply move on to someone else's Actor.

I'm Ryan Low. I publish pay-per-event Actors on the Apify Store as **locaihost**: SEC EDGAR financials and insider trades, careers-page jobs from Greenhouse/Lever/Ashby/Personio/Teamtailor, UK/EU/Canada government tenders, and a couple of others. This post walks through one real agent call against my SEC EDGAR Actor, then the design decisions that make an Actor usable (and affordable) for an agent. All the code below is from the Actors as they ship. I've left out anything I haven't measured myself.

## 1. Setup: one command

Apify hosts an MCP server. In Claude Code you add it with a single command:

```bash
claude mcp add apify https://mcp.apify.com/ -t http
```

The first time you use it, a browser OAuth flow opens and asks you to sign in to Apify, so there is no token to paste. After that the agent has tools such as `search-actors`, `fetch-actor-details`, `call-actor` and `get-dataset-items`.

To pin an agent to specific Actors, you can pass them in the URL instead (`https://mcp.apify.com?tools=locaihost/sec-edgar,...`). Each listed Actor then appears as its own tool.

## 2. What the agent actually sees

Before writing anything for agents, I read the source of [apify-mcp-server](https://github.com/apify/apify-mcp-server). Three findings shaped everything else:

- **`search-actors` is a thin wrapper over the Store search API** (`GET /v2/store?search=...`). The MCP server does no re-ranking of its own, so agent ranking *is* Store ranking: relevance plus the quality and popularity signals Apify uses for the Store (reliability, usage, reviews and so on).
- **The default `limit` is 5.** Agents are told to search with 1–3 keywords like "SEC filings" or "insider trades". Only five cards come back.
- **The card is built from your Actor's description, verbatim**, plus the input field list. Whatever you wrote in `description` in `.actor/actor.json` is the pitch an agent reads.

I need to be honest about the first two points. My Actors are a few weeks old, with almost no usage. When I ran agent-style queries against the Store API, **none of them appeared in the top 5 for any query I tested.** A brand-new Actor will not get picked through `search-actors` no matter how clean its schema is. Usage builds rank, and rank builds usage, and there's no shortcut I've found.

So why bother? Because search is only one way in. An agent can still reach a new Actor when:

1. the user names it ("use locaihost/sec-edgar"),
2. it is pinned in the MCP URL with `?tools=`,
3. it shows up in a README, a blog post or a published task that the user or agent has already read.

In all three cases the agent skips the search and goes straight to `fetch-actor-details` and `call-actor`. From there, the input schema, the failure modes and the charge floor decide whether the call works. That part you control on day one.

## 3. A real call

Here is the call Claude made against [locaihost/sec-edgar](https://apify.com/locaihost/sec-edgar), via the MCP `call-actor` tool, when I asked for NVIDIA's recent insider trades:

```json
{
  "actor": "locaihost/sec-edgar",
  "input": {
    "companies": ["NVDA"],
    "modes": ["insiderTrades"],
    "maxResults": 5,
    "onlyNew": false
  },
  "callOptions": {
    "maxTotalChargeUsd": 0.1,
    "memory": 1024
  }
}
```

The agent made two good choices on its own. It set `maxResults` to the number of rows it actually needed, and it capped the run's total spend at ten cents with `maxTotalChargeUsd`. Both of those only work if the Actor respects them, which I come back to below.

The result, abridged:

```text
status:        SUCCEEDED
runtime:       4.24 s
compute units: 0.0012
items:         5
fields (29):   recordType, cik, ticker, companyName, form, filingDate,
               accessionNumber, insiderName, insiderCik, insiderType,
               insiderRole, isDirector, isOfficer, isTenPercentOwner,
               officerTitle, is10b51Plan, securityTitle, transactionDate,
               transactionCode, transactionLabel, acquiredDisposed, shares,
               pricePerShare, value, sharesOwnedAfter, directOrIndirect,
               ownershipNature, filingUrl, scrapedAt
```

Five rows, each one a Form 4 transaction, in about four seconds. The field names do most of the explaining. An agent working out "who sold, and how much" filters on `acquiredDisposed: "D"` with `transactionCode: "S"` and sums `value`. It doesn't need a README for that.

One field deserves a closer look: **`insiderName` is null for people.** Form 4 filings name the individual filer, but the Actor deliberately never outputs a natural person's name. An insider is identified by role (`insiderRole: "Officer (CFO)"`, `isDirector`, `isTenPercentOwner`). Names are output only for organisations such as funds, LLCs and holding companies:

```typescript
// Legal-entity markers. A name matching none of these is treated as a person and is never output.
export const isEntityName = (name: string): boolean =>
    ENTITY.test(name.trim()) && !/\b(FAMILY|REVOCABLE|IRREVOCABLE|LIVING)\b/i.test(name);

// ...inside toTradeRecords():
const entities = owners.filter((o) => isEntityName(o.name));
insiderName: entities.length ? entities.map((o) => o.name).join('; ') : null,
insiderType: entities.length === owners.length && owners.length ? 'entity' : entities.length ? 'mixed' : 'individual',
insiderRole: owners.map(roleLabel).filter(Boolean).join('; '),
```

Family and revocable trusts count as people. Reporting-owner addresses are never read at all. For agents this matters more than for human users: an agent will happily copy whatever you return into a CRM, an email or a report. If personal data is never in the dataset, it can never leak from there. I made "business data only" a hard rule for all my Actors (I'm in Singapore, and PDPA is the obvious concern). For insider trading analysis, role and size are what you need anyway.

## 4. Input schema: one obvious required field

The input schema becomes the agent's tool definition. Mine has eleven fields, but an agent only has to understand one:

```json
"companies": {
    "title": "Companies",
    "type": "array",
    "description": "One per line: a US ticker (AAPL, BRK.B), an SEC CIK number (320193) or a company name (Microsoft). Any company that files with the SEC. Up to 500.",
    "editor": "stringList",
    "prefill": ["AAPL", "MSFT", "NVDA"]
}
// ...
"required": ["companies"]
```

Every other field has a sensible `default`: all three modes, the last 90 days, 8 periods, newest filings first. A minimal valid call is `{"companies": ["NVDA"]}`.

Note the **`prefill`, not `default`**, on the required field. This is the easiest trap to fall into. A required field that also has a `default` silently loses its `required` flag in the tool schema the agent receives. To the agent, the field looks optional. It then calls the Actor without it, the platform fills in your default, and the agent gets data for AAPL, MSFT and NVDA when it asked about something else. `prefill` fills in the form for humans in the console and still shows an example value, but `required` survives. [Apify's own write-up on making Actors visible to agents](https://blog.apify.com/fixing-actors-invisible-to-agents/) puts it bluntly: a required field with a default is always a bug.

A few smaller rules I follow in every schema:

- **Descriptions under 500 characters.** Field and Actor descriptions end up in the tool definition and the search card. Long ones get truncated or eat the agent's context. Put the essentials first: what to type, in what format, with one example.
- **Accept what a model is likely to send.** `companies` takes tickers, CIKs *or* names. `sinceDate` takes `2026-07-01` *or* `"90 days"` *or* `"6 months"`. A model will try the natural phrasing first, so treat it as valid.
- **Arrays stay arrays.** `modes` is an enum array with `enumTitles`, not a comma-separated string the agent has to guess the format of.

## 5. Bad input should not mean FAILED

What should happen when an agent sends `{"companies": ["NVIDIAA"]}`, or a list where every entry is junk?

My first versions called `Actor.fail()` with a clear message. That seemed right until I ran a robustness pass and noticed two problems. A FAILED run counts against the Actor's success rate, which feeds the quality score, which feeds search rank (the same rank agents see). And to an agent, FAILED looks like "this tool is broken", not "you sent a bad ticker".

So invalid input now ends **SUCCEEDED, with nothing charged and a message that says how to fix it**:

```typescript
if (unresolved.length) log.warning(`Not found on EDGAR (use the ticker or CIK): ${unresolved.join(', ')}`);
if (!refs.length) {
    // Unknown tickers are an input problem, not a crash: exit SUCCEEDED with nothing charged.
    await Actor.setValue('SUMMARY', { since, modes: [...modes], pushed: 0, notFound: unresolved, companies: [] });
    await Actor.exit(`No companies to look up${unresolved.length ? ` — not found on EDGAR: ${unresolved.slice(0, 20).join(', ')}` : ''}. Add tickers (AAPL), CIKs (320193) or company names (Microsoft).`);
}
```

The exit message becomes the run's status message, which is part of the run details an agent can read back. An agent that reads "not found on EDGAR: NVIDIAA. Add tickers (AAPL)…" corrects itself on the next call. `Actor.fail()` is kept for real failures only: if *every* company lookup hit an upstream error, the run fails, because then something really is broken.

The careers-jobs Actor goes one step further and rejects junk before fetching anything (sentences, markup, 300-character pastes), so prompt-injected garbage in the `companies` array never turns into outbound requests or charges.

## 6. Pay-per-event charging you can trust

All my Actors use pay-per-event pricing: a tiny start fee plus one event per record. For sec-edgar that's $2 per 1,000 records at the base tier, so the five-row NVIDIA call above cost about a cent. Agents work well with this model: they pay for exactly what they used, and `maxTotalChargeUsd` gives them a hard ceiling.

There is a catch in the SDK. Under pay-per-event, `Actor.pushData(items, eventName)` returns a `ChargeResult` telling you how many items were charged, and therefore stored. When the user's charge limit is reached mid-batch, the SDK drops the rest. My Actors batch pushes (100 items per API call), and for batches **the returned ChargeResult can undercount or overcount**. I don't fully understand why, though the client chunking requests internally is the likely cause. That matters because my "only new since last run" mode remembers which items were delivered. Trust a wrong count, and a user either pays for an item they never got or never sees it again.

The fix is to stop trusting the return value and measure the charging manager's counter before and after. This is the actual push function from the careers-jobs Actor (sec-edgar uses the same one with `EVENT = 'record'`):

```typescript
// Measure the charged-event counter delta; the per-call ChargeResult is unreliable for batches.
const charging = Actor.getChargingManager();
const isPpe = charging.getPricingInfo().isPayPerEvent;
const emitter = new BatchEmitter<Job>(
    async (items) => {
        if (!isPpe) {
            await Actor.pushData(items);
            return undefined;
        }
        const before = charging.getChargedEventCount(EVENT);
        await Actor.pushData(items, EVENT);
        return {
            chargedCount: charging.getChargedEventCount(EVENT) - before,
            eventChargeLimitReached: charging.calculateMaxEventChargeCountWithinLimit(EVENT) <= 0,
        };
    },
    cap,
    (keys) => seenList.push(...keys),
);
```

The `BatchEmitter` then treats `chargedCount` as the truth: only that many items are counted as emitted, only their keys go into the "seen" list, and the run stops cleanly once the limit is hit:

```typescript
const res = (await this.push(batch.map((b) => b.item))) || {};
const stored = Math.min(res.chargedCount ?? batch.length, batch.length);
this.emitted += stored;
this.onStored(batch.slice(0, stored).map((b) => b.key));
if (res.eventChargeLimitReached || stored < batch.length) this.stopped = true;
```

So an item dropped by an agent's ten-cent cap is not marked as seen, and it comes back on the next run. Note that the `!isPpe` branch matters too: outside pay-per-event (local runs, for example) the ChargeResult reports zero charged even though everything was stored.

One more thing to know while testing: a run's `chargedEventCounts` and the dataset `itemCount` lag a few seconds behind the end of the run. Re-fetch before deciding you've found a billing bug.

## 7. Let small budgets in

Pay-per-event Actors have a pricing setting called `minimalMaxTotalChargeUsd`. It's the lowest `maxTotalChargeUsd` a caller may set when starting a run. If an agent's budget is below your floor, the run doesn't start.

Agents tend to use small budgets on purpose. Claude chose $0.10 for a five-row lookup, which is a sensible thing for an agent to do. A floor of a dollar would have blocked that call. When I repriced my Actors I lowered the floor to **$0.05** on all of them.

```json
"minimalMaxTotalChargeUsd": 0.05
```

Two related details. First, when changing pay-per-event pricing through the API, you **append** a new `pricingInfos` entry; replacing the existing ones fails. Second, the default run memory is set to 1 GB in `actor.json`, because the Actor-start event is charged per GB of memory. Agents rarely override memory, so whatever default you pick is what they pay.

## 8. Other guardrails worth having

- **A free-plan cap that's documented.** On Apify's free plan my Actors return at most 100 records per run, and the run log says so. An agent that sees 100 rows and a warning can explain the reason to the user instead of guessing.
- **Respect upstream limits.** sec-edgar sends every request through one global rate limiter (8 requests per second, under SEC's fair-access limit), with a declared User-Agent and backoff when SEC throttles. Agents run in loops; your Actor should not let a loop hammer the source.
- **Official, public sources.** EDGAR data is public domain. That's one less thing an agent (or its user) has to worry about before using the output.
- **A SUMMARY record.** Every run writes a `SUMMARY` key-value record with per-company counts, notes and "not found" lists. An agent that gets zero rows can read *why*.

## Checklist

If you want an agent to be able to use your Actor, and afford it:

- [ ] Actor `description` starts with a verb, says what comes back, and stays under 500 characters. It is the agent's tool card.
- [ ] One obvious required field, with `prefill` and **no `default`**. Everything else optional with sensible defaults.
- [ ] Field descriptions under 500 characters, essentials first, one example each.
- [ ] Accept the natural formats a model will try (tickers *and* names, `"90 days"` *and* ISO dates).
- [ ] Invalid input ends SUCCEEDED, charges nothing and says how to fix it. `Actor.fail()` only for real outages.
- [ ] Honour `maxResults` and the caller's `maxTotalChargeUsd`, and stop cleanly when either is reached.
- [ ] Count charges with `getChargedEventCount()` deltas, not the batched `pushData` ChargeResult.
- [ ] `minimalMaxTotalChargeUsd` low enough for small agent budgets (I use $0.05).
- [ ] No personal data in the output. Identify people by role, not name.
- [ ] Expect `search-actors` to ignore you at first. Get in front of agents through names, `?tools=` URLs, READMEs and published tasks while usage builds.

None of this makes a new Actor show up in an agent's top five. That takes usage, and I don't have much yet. What it does is make sure that when an agent does reach your Actor, the first call works, costs what it should, and gives the agent something it can use.

More about what I'm building is at [locaihost.org](https://locaihost.org).
