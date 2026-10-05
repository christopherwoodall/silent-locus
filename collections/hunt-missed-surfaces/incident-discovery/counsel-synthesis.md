# Counsel synthesis — where to hunt next (2026-10-03)

Four lenses deliberated. Verdict below, ranked.

## The counsel's picks

**Theorist (highest conviction):** Our dormancy finding never covered arquivo.pt — the one venue where agent traffic was actually proven. If Sep/Oct captures carry the nonce grammar, the machinery never went dormant; we watched the wrong feeds. Cheapest high-value query left; directly falsifies or confirms the hunt's biggest negative.

**Trace-hunter (#1):** NPWS Fire History service, June 2026. Named endpoint, two-day-old disclosure, zero trace work done, three known-good query shapes (urlquery domain search, CDX prefix, relay-wrapped CDX). One afternoon.

**Contrarian (highest surprise):** The long tail. Every team keys on bursts; single-capture nonce traces on unnamed hosts are missed by design. Arquivo.pt's full query-string index enumerates them with no burst threshold — structural yield, not contingent.

**Skeptic (weakest claim):** The "one operation's window" synthesis. Mid-June is peak activity; coincidence is expected. Shared grammar proves same toolkit, not same operation. Falsification test: interleaved multitasking timestamps on a shared relay from existing CDX data (free), or the WARC User-Agent retry (blocked by 429).

## Ranked hunt plan

1. **Arquivo.pt Sep–Oct 2026 nonce sweep** — falsifies/confirms dormancy. Cheapest query.
2. **NPWS Fire History trace sweep** (urlquery + CDX + relay-wrapped CDX, June 2026) — the named endpoint nobody has examined.
3. **Long-tail enumeration** — arquivo.pt query-string index, nonce grammar, no burst threshold.
4. **Interleaved-relay timestamp analysis** — existing CDX data; instance-level linkage test for the operation-window claim.
5. **Dork-hunt v2** — already running.

## Standing corrections from the skeptic
- "One operation's window" is demoted to toolkit-level linkage until instance-level evidence lands.
- All burst-keyed conclusions carry the long-tail blind spot.

Full briefs: `counsel-trace-hunter.md`, `counsel-skeptic.md`, `counsel-theorist.md`, `counsel-contrarian.md`.
