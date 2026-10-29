# Pastebin-cluster sweep — 2026-09-28

Sweep of the 8 pastebin venues referenced across the 51 new anna.fyi pastes
(`data/paste-archive-gap/`), dispatched per Christopher's "sick agents on this".

## Per-venue verdicts

| Venue | Status | Finding |
|---|---|---|
| nicepaste.com | live, listing swept | /search listing (paginated) checked; ~50 pastes all old spam, zero markers. Swarm-linked `/list-of-subdomains` paste is empty. |
| porkpad.com | **dead** | Domain parked/for sale. Not a pastebin. |
| pasteview.com | live, partial | Homepage recent widget (8 pastes, generic/spam titles) clean. Bodies JS-gated; API search needs paid key. |
| pastebox.to | live, no listing | No public listing discoverable (v3.0 delisted guest pastes). One indexed public paste checked — mundane. |
| pastebin.irixnet.org | live, no listing | "Recent Pastes" nav broken (resolves to forums site). Creation login-gated. |
| mcbin.dev | live, listing swept | Full 23-row recent table + 2 body samples — all mundane, zero markers. |
| gritpost.com | **not a pastebin** | Progressive news blog (2019 content). |
| gotit.pub | **not a pastebin** | Research-discussion platform (arXiv annotation). |

## Headline

**Zero swarm-marker hits across all 8 venues.** No `zz` labels, no epoch nonces,
no transfer-test grammar, no proxy-ladder URLs, no machine-grammar authors, no
NSI/stats references.

## Interpretation

Three of the eight "pastebins" were never paste venues (one dead domain, two
misidentified platforms) — the anna.fyi paste mentioning them was a link dump,
not a venue directory. Of the five real pastebins, the two with fully public
listings are clean, and the other three expose no enumerable surface. The
swarm's observable comms ponds remain anna.fyi and the Iowa Stikked instance.

## Data

`data/pastebin-cluster-sweep/` — `sweep.jsonl` (9 explicit-event docs),
`PROVENANCE.md`, `SHA256SUMS`, `progress.log` (DONE). Disk + git only; no
Elastic writes (freeze in effect).

## Residual gaps (passive-only, for later)

- nicepaste.com internal search query interface (JS form, not discoverable via
  text fetch).
- pasteview.com paste bodies (JS-rendered) and Discover section URL.
- pastebox.to public-paste enumeration (no listing surface; direct-URL only).
