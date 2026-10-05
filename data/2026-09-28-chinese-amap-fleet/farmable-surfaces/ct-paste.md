# CT + paste-venue sweep — amap-fleet farmable surfaces
**Operator:** subagent worker, 2026-10-04 ~22:05–22:20 CDT. Read-only. No pastebin logins, no bulk scraping of pastebin.com (per the 2026-09-28 pastebin-pivot lane's standing constraint — bulk scraping blocks). No commits/pushes.

## A. Certificate Transparency (crt.sh, free, no auth)

### Queries (all `%<pattern>%`, `output=json`, via curl)
| # | Pattern | Result | Notes |
|---|---|---|---|
| 1 | `%uqprobe%` | **0 certs** (`[]`) | distinct campaign marker — absent |
| 2 | `%uqscan%` | **0 certs** | distinct campaign marker — absent |
| 3 | `%sub_poi%` | **0 certs** | tag grammar — absent |
| 4 | `%httpbun%` | **0 certs** (first attempt: crt.sh 404, retry clean) | staging host — absent |
| 5 | `%poinavi%` | **0 certs** (first attempt: crt.sh 502, retry clean) | amap tag — absent |
| 6 | `%navi%` | 3,391 rows pulled (stream truncated by curl timeout ~1.2MB), **0 with not_before in 2026** (crt.sh sorts newest-first: first row 2025-06-20) | pure noise: satnav/navigation sites, vercel deploys, restaurants; zero agent-shaped names |
| 7 | `%uq%` | 2,459 rows; 89 with 2026 not_before → 29 unique names | all noise: **UQ Communications Inc.** (Japanese ISP: uqwimax.jp, uqc.co.jp, uq-kensetsu.jp), oshop24/workers.dev junk; zero agent-shaped |
| 8 | `%amap%` | 517 rows; 17 with 2026 not_before → 5 unique names | all noise: amapspa.it (Italian spa chain), pamaprosvetleni.cz; **no Alibaba AMAP / amap.aliyun certs at all** |

`%lhr.life%` was not queried: it is localhost.run's apex — millions of tenant certs, unusable, per brief.
is.gd-adjacent custom shortener domains: not answerable via CT — no operator-owned shortener domain name is known, and is.gd itself is a public utility, not operator infra. No query possible without a pattern.

### Verdict: **CT is a dead end for this operator.**
Every distinctive campaign marker (`uqprobe`, `uqscan`, `sub_poi`, `httpbun`, `poinavi`) returns **zero certs**. The broader `%uq%`/`%amap%`/`%navi%` hits are unrelated noise (Japanese ISP, Italian spa, navigation sites) — nothing operator-shaped, no random-looking subdomains, no probe/scan/relay/tunnel/cors/agent grammar. This is expected: the operator's infra is **ephemeral lhr.life tunnels** (certs belong to localhost.run's wildcard — unusable for fingerprinting) plus **public utilities** (is.gd, httpbun — they own no certs of their own). The operator never mints certs on owned domains, so CT has nothing to index. CT only helps if/when the operator stands up non-tunnel infra under a name containing our markers — worth a cheap re-run in future sweeps, but do not budget real effort here.

## B. Pastebin archives — agent program drops

### B1. pastebin.com/archive (public listing)
- Fetched 2026-10-04 ~22:06 CDT: 50 most-recent public pastes, spanning 2026-10-04 back to ~2026-09-28 (6 days).
- Titles: "Halo Evolutions 7–46" fanfic spam series (dominates the listing), crypto-scam titles ("+12,000$ in 2 days", "Free Crypto Method", "Crypto admin access"), Dutch Office-license spam, Korean web-security tutorial, powershell snippets, stock/firewall snippets.
- **Zero titles matching `uqscan`, `sub_poi_navi`, `lhr.life`, or base64/httpbun program drops.** The listing is dominated by a single spam source; effective recent-archive coverage is thin.
- One body read attempted ("Rare Scanner Bug Report 10/04/2026", most marker-adjacent title) — the archive's link mapping shifted and it opened an unrelated Dutch Office-license spam paste. No marker content. Bulk body scraping deliberately avoided (prior lane constraint: pastebin.com blocks scrapers).

### B2. ix.io
- **Down as of 2026-10-04**: front page returns "ix.io is taking a break 🍺" + under-construction gif. No pastes retrievable, no index exists. Nothing to hunt.

### B3. termbin.com
- **No public listing exists**: netcat-only pastebin (URL-keyed, `nc termbin.com 9999`), landing page has no archive/recent/browse/index. Only discoverable via known URLs or search-engine caches — same blind spot as before.

### B4. Search-engine caches (our markers × paste venues)
- `"uqscan" OR "sub_poi_navi" pastebin OR ix.io OR termbin` → zero real hits (junk SEO PDFs on a compromised Nigerian vaccination site only).
- `"lhr.life" pastebin OR paste OR "ix.io" OR termbin` → zero real hits (same junk).
- Prior lane `data/2026-09-28-pastebin-pivot/` (2026-09-28): grepped all local paste corpora (2026-05-27-paste-archive bodies, paste-archive-gap, iowacollab, linuxiarz) + search-engine caches for ExploitGym markers → **zero paste-body hits**. I read its PROVENANCE.md and did not redo that work; my markers here (`uqscan`, `sub_poi_navi`, `lhr.life`) are orthogonal and also zero.

### Verdict: **paste venues are a dry surface for this campaign right now.**
No marker content on pastebin.com's recent public archive, in search-engine caches, or in any local paste corpus. ix.io is down (no surface); termbin.com has no indexable surface. If the agents do stage programs on pastes, they aren't using public-indexed pastes or memorable titles — but CT's zero-marker finding suggests they stage on httpbun (public utility, no paste drop needed). Do not budget repeat sweeps of these surfaces without a new lead.

## Bottom line
Both surfaces honest zeros. The operator's infra choice — ephemeral tunnels + public utilities, no owned domains, no minted certs, no public paste drops — is *designed* (or at least functions) to be invisible to both CT and paste-venue indexing. The fingerprints that survive are elsewhere: is.gd short links (see `isgd-resolutions.md`), urlquery.net scan sessions, and public shortener stats pages.
