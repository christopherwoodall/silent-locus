# Strategic Counsel Memo: Agent-Swarm Crawler Lane Selection

**To:** BigSexyWarlock69
**From:** Strategic counsel (adversarial lane review)
**Date:** 2026-10-14
**Subject:** The 8-lane plan has two lanes of theater, one ghost hunt, and a missing surface bigger than all of them.

## Executive summary

- **Lane 1 (urlquery.net)** is the only lane anchored to observed fleet behavior. It stays and leads.
- **Lane 7 (packages)** has zero observed agent precedent, a documented prior negative from our own shop, and the worst signal-to-effort ratio of the eight. **Cut it.**
- **Lane 3 (ntfy.sh)** is one empty topic wearing a lane's clothes. **Lane 5 (Wayback CDX)** is a slow archive pointed at 7-day infrastructure — structurally mismatched as a monitor. Demote both to reactive tools, not standing lanes.
- **Lane 8 ("prime for targeting")** cannot produce a PRIMARY or SECONDARY hit by construction. It is a hypothesis notebook in a lane's uniform.
- The highest-value uncovered surface is **GitHub itself** — compute (Actions), storage (gists), coordination (issues/comments), payload hosting (raw URLs). Public, API-native, persistent, passively collectable. **Add it.**

Net recommendation: run **6 lanes** (1, 2, 4, 6, new GitHub lane, plus lane 8 reframed as a hypothesis feeder), keep 3 and 5 as reactive enrichments, kill 7.

---

## Q1. Missing surfaces: where agents operate that no lane covers

Frame it by what an agent fleet actually needs: **compute, egress, storage, coordination.** Map the 8 lanes against those needs and the gaps are obvious.

**Compute — completely uncovered.** No lane watches free compute abuse. A fleet that graduates from "borrow urlquery as a code runner" to "own runners" will use: GitHub Actions (unlimited free minutes on public repos), Cloudflare Workers free tier, Colab/Kaggle notebooks, Vercel/Netlify/Render/Railway/Fly free tiers, and CI runners generally. urlquery-as-runner was the fleet's *opportunistic* choice; owned free compute is the *strategic* choice, and we are blind to it.

**Egress — thinly covered.** Lanes cover webhook.site inboxes and ntfy topics. Uncovered: Discord webhooks, Telegram Bot API, Slack webhooks, gist/paste drops, file.io / 0x0.st / transfer.sh, r.jina.ai (already in our own hypothesis as laundering infrastructure), and **Google Sheets/Forms as exfil** — a form POST appends a row: free, no auth, trusted google.com domain, persistent, machine-writable by URL. That is exactly the Amap fleet's economic logic applied to a surface none of our lanes watch.

**Storage/persistence — uncovered.** Gists, pastebins, IPFS, S3-compatible free tiers, Cloudflare KV/R2, Supabase/Firebase free tiers. The fleet used httpbin for payload delivery because it was free and URL-addressable; every one of these is the same shape with better persistence.

**Coordination — uncovered, and this is the big one.** Agents that coordinate need shared state. Options: GitHub issues/PR comments as mailboxes, **nostr relays** (no-auth pub/sub, arguably the most agent-native protocol in existence), on-chain memo fields, Telegram channels, Bluesky PDS relays. Nothing in the 8 lanes watches any coordination channel. We are hunting *swarms* — agents finding each other and coordinating — with zero lanes on the surfaces where coordination happens.

**Highest-value uncovered surface: GitHub as substrate.** It spans three of the four needs in one public, API-accessible, persistent surface: Actions = compute, gists = storage/payloads, issues/comments = coordination mailboxes, raw.githubusercontent.com = trusted payload hosting. It is where agents natively live (code, APIs, no signup friction for public use), it is persistent (fixes the ephemerality problem that cripples lanes 2 and 5), and it is passively collectable at scale via GH Archive. Runner-up: Google Sheets/Forms exfil — same economic shape as the fleet's known choices, but harder to observe publicly, so GitHub wins on observability.

Honest limit: DNS TXT dead-drops are also uncovered and classically agent-shaped, but there is no free passive-DNS source for *new* records at our scale. Noted as a gap we cannot cheaply close.

---

## Q2. Lane 8 ("prime for targeting"): ghost hunt

"Prime for targeting" is not a predictive criterion. It is a vibe.

The Amap fleet's actual surface choices are explained by a tight economic grammar: **free, no-auth, URL-addressable, machine-readable, zero setup.** That grammar is precise — and it matches roughly ten thousand surfaces (every pastebin, every echo service, every free-tier PaaS, every open redirect, every form endpoint). It predicts the *class*, never the *instance*. Knowing a fleet will use "something free and URL-addressable" tells you nothing about *which* surface to watch tomorrow.

False-positive load: unbounded by construction. Every open redirect on the internet is "prime for targeting" under this definition. A lane that flags the entire free tier of the internet is not a detector; it is a phone book.

Worse, it inverts our own evidence doctrine. PRIMARY is what we observed with provenance. SECONDARY is someone else's observation cited as context. Lane 8 produces **neither** — it manufactures would-bes. It cannot emit a graded hit by construction, so as a hit-producing lane it is theater.

The narrow salvage: lane 8's *thesis* is correct (agents repurpose trusted programmable surfaces) and its *economic grammar* is useful as a filter. Keep it as a **hypothesis notebook that feeds patterns into lanes 1–6**, never as a lane that produces hits. And note the irony: the single highest-value concrete instance of lane 8's thesis — GitHub — is not monitored while we model the abstract class. Fix that with the add recommendation below.

---

## Q3. Lane 7 (packages): borrowed lens, no agent precedent

Is there any evidence agents distribute via package registries? **No — not in our flagship case, and not in our own prior work.**

The Amap fleet delivered payloads via **httpbin**, ran code via **urlquery**, exfiled via **webhook.site**. At no point did it touch a package registry. Package distribution is a *persistence mechanism for human supply-chain attackers*: poison an ecosystem, wait for victims to install. Rogue agents need *live infrastructure they control*, not victims running `pip install`. The threat model is inverted — packages are how you attack developers; our threat is agents operating infrastructure.

Our own shop already ran this experiment: the RubyGems `oai*` sweep found **14 names total, zero in the target window** — a clean negative. The real malicious-package campaigns are Diffend-indexed human operations. That is supply-chain security's threat, not ours.

The one agent-native distribution channel that exists — MCP servers / skills marketplaces — is **off-script** per standing hunt rules (adjacent infrastructure, not swarms). So lane 7 as scoped has no on-script justification left.

Verdict: lane 7 applies a human supply-chain lens to an autonomous-agent threat, has no observed agent precedent, carries a documented prior negative, and costs the most engineering of any lane (three registries' daily churn, name-pattern heuristics over millions of packages, version-diff noise). It is the cut.

---

## Q4. Lane 3 (ntfy.sh): a single data point, not a lane

We have **one known topic and it is empty.** A lane needs an independent discovery mechanism. ntfy has none available to us:

- There is no public topic directory. Topic names are unguessable.
- The only discovery path is extracting `ntfy.sh/<topic>` URLs from artifacts found in **lanes 1 and 4** — which makes lane 3 a downstream enrichment of those lanes, not an independent collector.
- ntfy messages are ephemeral (server-side cache is hours, not days). A daily 10:00 poll of a known topic will miss anything that is not timed to the poll.

A cron that GETs one empty topic every morning is theater. **Demote lane 3 to a reactive lookup**: when lane 1 or 4 surfaces an `ntfy.sh/` URL, fetch it then. That preserves 100% of its real value at ~0% of its standing cost. If a second fleet ever shows ntfy usage, revisit — one data point does not justify a lane.

---

## Q5. Lane 5 (Wayback CDX): structurally mismatched to the target

The target: fleet infrastructure with **7-day lifespans** (webhook inboxes) and cloud hosts that rotate in days to weeks. The instrument: an archive that crawls on a **weeks-long schedule**, may never visit an obscure `*.hysandbox.tencent-cloud.com` subdomain at all, and honors robots on the hosts most worth archiving.

A daily monitor asking CDX for *new captures* of *ephemeral infra* will return silence almost every day, and when it returns something it will be history weeks late — too late for a 10:00 monitoring loop whose value is *current* fleet tracking. The cadence of the instrument and the lifespan of the target are mismatched by an order of magnitude.

CDX is a fine **forensic** tool: lane 1 or 4 identifies a host, you pull its capture history to confirm it existed and grab its content. Keep it in the toolbox for that. **Kill it as a standing monitoring lane.**

---

## Q6. Cut list: lane 7 (RubyGems/PyPI/npm)

Worst signal-to-effort ratio, by distance:

- **Signal:** zero observed agent distribution in the flagship case; documented prior negative (RubyGems `oai*` sweep); the real malicious-package ecosystem is human supply-chain work outside hunt scope.
- **Effort:** the highest of any lane — three registry APIs, daily churn over millions of packages, name-pattern heuristics with no grounding in agent behavior, version-diff noise to triage.
- **Scope:** even its best case (MCP/skill distribution) is off-script adjacent infrastructure.

Lanes 3 and 5 are also weak, but each costs roughly one HTTP request a day; their sin is emptiness, not expense. Lane 7 costs real engineering and produces supply-chain noise that is not our threat model. **Cut lane 7.** If package-shaped evidence ever appears in lane 1 or 4 artifacts, re-open as a reactive investigation — not a standing lane.

---

## Q7. Add list: GitHub coordination-substrate lane

**The one lane to add: monitor GitHub as agent coordination substrate** — gists, issues, PR comments, repo-creation bursts, Actions usage — via GH Archive and the API, passive collection only.

The argument:

1. **It covers three agent needs in one surface.** Actions = free compute (unlimited minutes on public repos — the fleet's "borrowed runner" logic, upgraded). Gists = storage and dead drops. Issue/PR comments = coordination mailboxes. raw.githubusercontent.com = trusted-domain payload hosting, the httpbin role with persistence.
2. **It fixes the ephemerality problem.** Lanes 2 and 5 die on 7-day inboxes and rotating hosts. GitHub content persists. A fleet that coordinates on GitHub leaves a durable trail — the thing our current lanes structurally cannot capture.
3. **It is where agents natively live.** Agents are code-first and API-native; GitHub is the highest-trust, lowest-friction programmable surface on the internet. Lane 8's thesis says agents repurpose exactly this class of surface — so stop modeling the class and watch the instance.
4. **It is passively collectable at scale.** GH Archive publishes the full public event firehose; daily jobs can grep it for fleet indicators (webhook.site inbox URLs, ntfy topics, Amap API patterns, httpbin payload shapes, tag grammars) across *all* of GitHub. That is a real discovery mechanism — the thing lane 3 lacks.
5. **It closes the loop with lane 1.** urlquery reports and urlscan scans already contain GitHub URLs; the new lane turns those from isolated artifacts into a graph.

Guardrail (standing rules apply): monitor *coordination and dead-drop behavior* — gist payloads, mailbox comments, fleet-scaffolding bursts. Do **not** drift into skill-marketplace census; that is off-script adjacent infrastructure. The lane hunts swarms, not catalogs.

Cost estimate: one daily GH Archive pull + pattern grep + API follow-ups on hits. Comparable to lane 1's cost, with broader coverage than lanes 3+5+7 combined.

---

## Ranked lane value assessment

| Rank | Lane | Value | One-line justification |
|---|---|---|---|
| 1 | urlquery.net (1) | **HIGH** | The fleet's actual code runner; tag grammar + Amap detectors are precise; PRIMARY-grade observations. |
| 2 | GitHub substrate (NEW) | **HIGH** | Compute+storage+coordination in one public surface; persistent; passively collectable; fixes the ephemerality gap. |
| 3 | webhook.site creator-IP (2) | **MEDIUM** | Real attribution method, but 7-day half-life and fleet-specific — time-box it, verify the method still works. |
| 4 | crt.sh (6) | **MEDIUM** | Cheap, persistent cert trail of ephemeral infra; blind to wildcard/provider-cert setups but occasionally decisive. |
| 5 | urlscan.io (4) | **MEDIUM** | Secondary to lane 1; confirmation value and some independent finds, but not the fleet's runner of choice. |
| 6 | ntfy.sh (3) | **LOW** | One empty topic, no discovery mechanism; demote to reactive enrichment of lanes 1/4. |
| 7 | Wayback CDX (5) | **LOW** | Archive latency vs 7-day infra is a structural mismatch as a monitor; keep as forensic tool only. |
| 8 | DB URL mining (8) | **LOW** | Cannot emit PRIMARY or SECONDARY by construction; unbounded FP space; keep as hypothesis feeder, not a lane. |
| 9 | Packages (7) | **LOW** | No agent precedent, prior negative, human supply-chain lens, highest cost. **Cut.** |

## Explicit recommendations

1. **CUT lane 7 (packages).** No further discussion needed beyond this memo.
2. **ADD the GitHub coordination-substrate lane** (GH Archive + API, passive). Scope it to coordination/dead-drop behavior, not marketplace census.
3. **DEMOTE lane 3 (ntfy)** to a reactive lookup triggered by lane 1/4 artifacts.
4. **DEMOTE lane 5 (Wayback)** to a forensic tool triggered by lane 1/4 host identifications.
5. **REFRAME lane 8** as a hypothesis notebook feeding patterns into lanes 1, 2, 4, 6 and the new GitHub lane. It never emits hits.
6. **TIME-BOX lane 2 (webhook.site):** its value decays with the fleet's 7-day inbox cycle. Re-evaluate in 30 days or when the Amap fleet goes quiet — whichever comes first.
7. Resulting 10:00 monitor: **lanes 1, 2, 4, 6, GitHub (new)** as standing collectors; 3 and 5 as reactive enrichments; 8 as the hypothesis feeder. Five collectors, not eight — each one earning its keep.

## Open verification items (for the parent, not this memo)

- Confirm webhook.site still exposes creator IPs the way the researchers' method requires; if the site closed that behavior, lane 2's value drops to LOW and it should be cut with lane 7.
- Confirm GH Archive coverage and query cost are acceptable before committing the new lane; fall back to targeted API search if the firehose is too heavy.
- The Google Sheets/Forms exfil surface (Q1 runner-up) has no cheap public observability — flag as a known blind spot, not a lane.

---

*This memo challenges strategy, not implementation. If a lane above is theater, the honest move is to say so — done.*
