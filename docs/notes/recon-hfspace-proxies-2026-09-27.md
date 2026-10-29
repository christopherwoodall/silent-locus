# Recon B — HF Spaces as disposable proxy infra (2026-09-27)

**Question:** one wiki revision used `thenacken-python-cors-proxy.hf.space` as a CORS
proxy. Is `*.hf.space` proxy infra a pattern — and is any of it swarm-tied?

## In-corpus ground truth

Exactly **one** `hf.space` host appears anywhere in the collusion-wiki corpus
(3 occurrences, 1 revision family):

```
https://thenacken-python-cors-proxy.hf.space/?url=https%3A%2F%2Fwww.sec.gov%2Ffiles%2Fcounty.json
```

It is a **generic open CORS proxy**: `GET /?url=<target>` fetches any URL server-side
and returns the bytes (FastAPI, docker SDK, plus redgifs/gofile token special-casing —
code read from the public repo: `app/routers/proxy.py`). Space created **2023-11-14**,
i.e. pre-existing public utility, not swarm-built. The swarm used commodity infra.

## Prevalence sweep (Hub API, read-only)

- **CORS-proxy-named Spaces: ~15.** `TheNacken/python-cors-proxy`,
  `tiagofelicia/cors-proxy` (updated 2026-09-17), `Yeheng0201/roche-cors-proxy`
  (created 2026-06-07), `convictionvtb/corsproxy` (2026-06-06), `sidimadtv/cors-proxy`
  (2026-04-19), `soiz1/CORS-PROXY` (+4 forks), `markmcfc/cors-proxy3`,
  `Serj566/python-cors-proxy`, `Serj566/cors-1-proxy`,
  `MrFortune94/proxypass-cors-bypass-wizard`. All docker SDK, all generic `?url=` shims.
- **jina-reader-shaped:** `yi94188/jina-reader-test` (explicit name, 2026-01-29),
  `moritalous/url-to-markdown` (+v2, gradio, 2024, forked 2×),
  `nyuuzyou/urltomarkdown` (2026-06-17 — inside the campaign window),
  `dwfwfwfwf/url-to-markdown-v2` (fork).
- **Web search:** the `?url=` proxy-on-`hf.space` idiom is widespread and generic
  (e.g. `missourimonster-vyla-v3.hf.space/api?url=...` for media streaming) —
  commodity pattern, not swarm tradecraft per se.
- **Broad "proxy" search:** dominated by LLM API proxies (`gemini-proxy`, etc.) —
  different beast, excluded.

## Verdict

- **Swarm-tied Spaces: exactly 1, and only as a consumer** — the wiki swarm pointed
  at a pre-existing public CORS proxy. No Space shows swarm fingerprints
  (no zz/epoch naming, no swarm-built deployments found).
- **The pattern is real but commodity:** ~20 proxy-shaped Spaces exist; agents
  reaching for a free `?url=` fetch shim will keep finding them. Worth a standing
  watch (re-run Hub `?search=cors-proxy` / `jina-reader` periodically), but this is
  not a swarm-operated infrastructure layer.
- Consistent with the escaped-evals framing: the launcher reuses public commodity
  tooling (jina, translate.goog, public CORS proxies) rather than building bespoke
  infra per run — except where it did (`jqp.vercel.app`, `md.succ.ai` are the
  bespoke ones from the IOC lane).

## Dataset

Staged as a **separate dataset**: `data/hfspace-proxies/` — `spaces.jsonl`
(15 Spaces with `tie_strength` labels), `PROVENANCE.md`. Keep-all + annotate;
no operator identity pursued.

## Follow-ups

- Standing re-sweep of Hub `cors-proxy` / `jina-reader` searches (cheap, scriptable).
- The 2026-06-created proxies (`roche-cors-proxy`, `corsproxy`, `urltomarkdown`)
  merit one code read each if the June-18/July-7 waves grow new HF links.
