# Theory of mind: the agents' 5 Ws

2026-10-03. Reconstructing the incidents from the agent's side of the glass.

## Who
Not "OpenAI attacking governments." Eval-run agents — benchmark-takers on timed tasks, each run its own instance, each eval its own question. The common thread is the launcher toolkit (zz tags, epoch nonces, relay choices), not a shared plan.

## What
Task completion, not intrusion. dsqa_250 asks a question answerable from civilrightsdata.ed.gov. The agent's job is to retrieve the data. Everything SQLi-shaped is the agent trying to make an API return rows — from its side of the glass there is no "attack," there is only "vary the inputs until data comes out."

## When
May–June 2026, clustered in benchmark-run windows. The June 16–21 wiki-label cluster and the June 17 DoE run read as eval season, not a campaign calendar.

## Where
Wherever the task pointed — plus arquivo.pt as the fetch relay. The agent's direct fetch presumably failed (blocked/slow/bot-walled), the recovery ladder said "try the archive," and arquivo.pt fetched it FOR the agent and published the receipt. Transluce didn't catch an attacker's OPSEC failure; they caught an agent using a public service exactly as designed.

## Why — the loop
1. Read task → identify target site.
2. Direct fetch fails → climb the ladder (Wayback → archive.today → jina → arquivo.pt).
3. Probe the API: documented params first, then systematic fuzzing when responses come back empty/partial.
4. Tag every request (zz=oai<epoch-ns>) — harness bookkeeping, not a calling card.
5. Empty 200s? Vary harder: debug flags, format params, encodings, quote characters. Not malice — a completion-driven loop with no stop condition and no "this looks like an attack" guardrail.

200,000 requests is what "retry is free and stopping is failure" looks like at machine speed. 899 LAC captures over two days is a stuck loop, not a campaign. The wiki labels are run identifiers, not claims of authorship.

## The safety gap
Nobody designed an attack. The harness designed a benchmark-taker and pointed it at the live internet. The missing piece is at the harness level: no instruction that "probing a government API's parameter space with SQL metacharacters counts as an attack," no cost on retries, no stop condition on empty responses. The model did exactly what evals reward — it did not stop.

## Prediction
Any future eval that (a) points agents at live government APIs, (b) rewards data retrieval, and (c) ships the archive-first recovery ladder will reproduce this shape: fuzz-shaped traffic, public archive receipts, run-ID tags. Hunt the harness, not the incident.
