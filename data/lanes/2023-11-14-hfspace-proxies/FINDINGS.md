# Findings — 2023-11-14-hfspace-proxies

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## OBSERVED

- 38 proxy-shaped public HF Spaces were enumerated in two passes
  (2026-09-27/28: 15 Spaces; 2026-09-29: 23 more).
- 1 Space has a direct corpus link: `TheNacken/python-cors-proxy`
  (3 uses in the collusion-wiki corpus as `?url=<sec.gov/files/county.json>`).
  This is the only `in_corpus` record. The Space code was read: FastAPI,
  `GET /?url=<target>`, open access.
- 37 Spaces are `pattern_match`: they match the proxy shape by name or
  function only. No evidence links them to swarm use.
- Fork families exist: soiz1/CORS-PROXY has 5 forks (AndiGr, Jynx88, alx1880,
  markmcfc, public-soiz1); bobwatcherx and darenx each host 6 cors-anywhere
  clones; moritalous/url-to-markdown has 2 forks.
- 9 of the 23 refresh Spaces had app code read to confirm fetch-proxy
  behavior (not name-only matching).

## INFERENCE

- The soiz1 fork family and the bobwatcherx/darenx cors-anywhere fleets look
  like bulk deployments of one template, not organic one-off Spaces. This is
  a shape judgment, not evidence of swarm operation.
- None of the 37 `pattern_match` Spaces should be treated as swarm
  infrastructure without further evidence.

## Exclusions (recorded in source PROVENANCE.md)

- `JannisJulian/tts-web-reader`: TTS backend, not a fetch proxy.
- `Zangtungtung/mediaflow-proxy`: media-stream proxy, not web-fetch shape.
- `openai-reverse-proxy` / `oai-proxy` family: API-key proxying, different
  tradecraft.
