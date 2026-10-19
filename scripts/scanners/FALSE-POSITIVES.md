# FALSE-POSITIVES.md — Lane 8: Database URL mining

## What the scanner flags

The scanner scores domains in our own database on six criteria:
programmability, low auth, persistence, observability, traffic,
prior agent contact. High-traffic benign domains will score on
traffic alone. This document tells them apart from true
agent-repurposable surfaces.

## The key discriminator: programmability

Traffic tells you where agent activity can hide. It does NOT tell you
what an agent can USE. A repurposable surface must take attacker-chosen
input and do something with it: store it, reflect it, execute it, or
forward it.

Rule of thumb: a domain is a prime target only if it scores on
programmability. Traffic without programmability is just a popular
website. The scanner requires target_score >= 2 (config
`dbmining.min_target_score`), but treat score-2 hits that are
"traffic + one flag" as leads, not findings.

## Known benign high-traffic domains in our corpus

These appear often in our records but score 1 (traffic only) or low.
They are correctly excluded or low-ranked:

| Domain | Mentions | Why it is benign here | Scores |
|---|---|---|---|
| github.com | 559 | Code host; we link to repos, agents cannot anonymously write | traffic only (1) — excluded |
| docs.google.com | 367 | Read links; creation needs a Google account | traffic only (1) — excluded |
| web.archive.org | 219 | Archive; read-only | traffic only (1) — excluded |
| huggingface.co | 168 | Model hub; uploads need login + review | traffic only (1) — excluded |
| www.sec.gov / query1.finance.yahoo.com | 139 / 42 | Data sources for lanes; JSON endpoints, no storage | traffic only (1) — excluded |
| arxiv.org | 56 | Paper links | traffic only (1) — excluded |
| www.anthropic.com | 66 | Vendor docs | traffic only (1) — excluded |

If one of these ever gains a programmability match (for example, a new
anonymous-submit endpoint), the scanner will promote it. That promotion
is the signal, not the raw traffic count.

## Grey zones

1. **University shorteners** (goto.unm.edu, u.ethz.ch, go.uvm.edu).
   Programmable, persistent, public-read — but creation needs a campus
   login. They score low_auth=false, which is the correct penalty.
   Agents with stolen campus credentials are a different hunt.

2. **ngrok.io tunnel subdomains.** Programmable in the sense that anyone
   can expose a local service, but each subdomain is attacker-controlled
   already. Scored for observability only. Do not treat as targets;
   treat as indicators when they appear in fleet traffic.

3. **discord.com.** Webhook receivers are programmable, but creation
   needs a server admin role. Off hunt-script scope (2026-10-11).
   Scored for documentation, deprioritized in practice.

## Low-occurrence / high-score edges

Some surfaces score 4-5 on a handful of mentions (baseline run:
catbox.moe 1 mention / score 5; pastebin.com 4 mentions / score 5).
The score is real — the surface IS repurposable — but the evidence
depth is thin. Rule: a score built mostly on config patterns with
fewer than 5 corpus mentions is a candidate for a probe, not a
finding. A score with 100+ mentions is an established pattern.

## How to clear a suspected false positive

1. Check the hit's `criteria` list. If it lacks programmability,
   it is traffic noise. Close it.
2. Check `evidence.example_urls`. If every URL is a read-only link
   (repo page, paper, archived copy), the surface pattern matched
   wrongly. Report the bad pattern so it can be narrowed.
3. Check `provenance.lanes`. If the domain appears only in one
   analyst's working lane and nowhere else, treat the prior-contact
   flag with suspicion.
4. If it survives: probe it. Can you create content with no login?
   Does the content get a stable public URL? Two yeses = real target.
