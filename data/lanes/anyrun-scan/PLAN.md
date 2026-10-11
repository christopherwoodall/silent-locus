# anyrun-scan PLAN — shape-based hunt on any.run public tasks

Branch: `anyrun`. Status: PLAN (recon complete, awaiting marching orders).

## Objective
Find rogue AI-agent eval-run traces in any.run's public sandbox submissions using
metadata SHAPES derived from our collected data. No long n-gram string searches —
that method has failed repeatedly (urlquery: 0 for "deepsearchqa"; GitHub: harness
code only; pastes: 0).

## Surface (verified 2026-10-07)
- TI Lookup: https://intelligence.any.run/ — SPA, **free tier requires registration**
  (no payment, but no anonymous access). Query syntax:
  `fieldName:"value" [AND|OR|NOT] fieldName:"value"`, `*` wildcards.
- Free tier limits: 11 fields, AND-only, **20 most recent results per query**.
  Premium: 44 fields, full operators, full history, API key.
- Shape-relevant fields: `taskType` (url|file), `url`, `domainName`, `destinationIP`,
  `submissionCountry`, `threatName`, `commandLine`, `suricataMessage`.
- XHR backend: `https://api-gb.any.run/lookup/search-with-updates/` (POST, bearer
  token from login). No unauthenticated JSON access — 401 verified.
- Public task pages render (200) but data loads via auth-gated DDP/REST.
- This is a **targeted pivot tool, not a corpus dump**: 20 results/query on free tier.

## Shape pipeline (ranked, from SHAPES inventory)
1. **S1 tag grammar** — `taskType:"url" AND url:"*zz=*"` style probes for harness
   param grammars (`zz=`, `_oai=`, `uq*=`, `mark=`, `validation=`, epoch nonces).
   Group hits by tag value; one value = one run.
2. **S6 staging/dead-drop hosts** — tasks whose network IOCs touch webhook.site,
   httpbun.com, httpbin.org, *.lhr.life, *.pinggy.io, is.gd, *.trycloudflare.com.
   Prioritize tasks hitting 2+ categories.
3. **S2 cartesian sweep** — cluster tasks by (host, path); flag groups where 2+
   numeric params each carry 50+ distinct values with count ~= product.
4. **S3/S9/S10 timing** — volley bursts (Δt ≤ 5s chains) vs serialized scripted
   loops (uniform gaps, no overlap); reject metronomic cadences (gap CV < 0.3).
5. **S5 proxy laundering** — tasks submitted via r.jina.ai / translate.goog /
   fanyi.baidu.com / markdown.new; extract embedded target host.
6. **S7 fuzz ladder** — param anomalies (negatives, >2^31 ints, SQL fragments,
   empty, duplicated params) on one host within minutes.
7. **S4 run labels** — mined per-cluster only, never pre-seeded.
8. **S8 cross-host walk** — same ID on 3+ hosts of one service family in 15 min.
9. **S11/S12** — corroboration only (self-ID strings, stock UAs).

## Method notes
- Query cheap/high-precision shapes first (S1, S6); expand via pivots.
- Cache every hit: task UUID, query, timestamp, raw metadata, sha256.
- Grade claims OBSERVED / INFERENCE / UPSTREAM. Reviewers hold kill authority.
- The amap-fleet probe playbooks are operator-injected (self-generated) — use
  their geometries, not their tags, against unknown actors.

## Open questions
1. Which 11 fields are free-tier (in-UI check needed)?
2. Does `url:` match the *submitted* URL for url-tasks, or only in-session URLs?
3. Is 180-day date range free-tier or premium-gated?
4. Do public task pages expose submitter country/metadata without login?

## Marching orders needed
- M1: one free any.run account (registration). Nothing works without it.
- M2: decision — free-tier pivot hunting (20 results/query, AND-only) vs premium
  trial for full history + API.
- M3: confirm scope — any.run only, or also tria.ge / hybrid-analysis in the same
  branch?
