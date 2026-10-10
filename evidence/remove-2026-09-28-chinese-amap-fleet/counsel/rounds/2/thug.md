# COUNSEL Round 2 — THUG (infrastructure muscle)

*Chair: Hunter S. Thompson. Filed 2026-10-05 ~08:45 UTC (03:45 CDT).*
*Method: passive OSINT only. Shodan STORED records (PUBLIC SOURCE per Round 1 convention), urlquery public report states (authenticated API 429'd — htmx keyless endpoints used; every htmx zero is a weak negative per Polyglot's documented caveat), our own corpora (OBSERVED). No candidate hosts fetched, probed, or connected to. Full observed values, never redacted.*

---

## FINDING 1 — Alive/dead ledger for the 4 confirmed inboxes (WOUND job 1)

**Claim:** All 4 Round-1-confirmed inboxes still resolve on webhook.site as of their last public scans (2026-10-04, 07:20Z–17:12Z). None are confirmed dead by any public report state.

**Evidence (PUBLIC SOURCE — urlquery htmx search + filter/http transaction records):**

| Inbox UUID (8-char) | Newest public scan | Scan state |
|---|---|---|
| `0a947514` (…b193dd2d519b) | report `8213c4a1-41ea-438d-ada0-489eabb94deb`, 2026-10-04T17:12Z | 200 OK, full inbox UI (56 transactions, socket.io polling live) |
| `a7753b69` (…80f69d57480c) | report `eb4ecb55-d335-45fb-b775-6746d422c7f0`, 2026-10-04T15:19Z | 200 OK — href.li wrapper resolved through to `webhook.site/a7753b69…?run=1791126770493` → 200 OK |
| `6ddc559e` (…f4addc42368a) | report `97f0619b-36e5-4c01-adab-a18a89b2b319`, 2026-10-04T15:01Z | 200 OK; response carried `x-token-id: 6ddc559e-5c08-4915-a5b2-f4addc42368a` — token confirmed live server-side |
| `e691f66e` (…a79521173811) | report `b3c0e9e3-22d6-4b61-bf21-07e4cf22e3d0`, 2026-10-04T07:20Z | 200 OK; `/token/e691f66e…/requests?page=1&password=&per_page=50&query=&sorting=newest` → 200, `application/json`, **88 bytes** — an empty request list at scan time |

**Classification:** OURS (the 4 UUIDs) / evidence PUBLIC SOURCE.

**Actionability:**
- Alive/dead verdict as of public evidence: **4 ALIVE, 0 confirmed dead.** The ledger's newest public beacon evidence is 2026-10-04T17:12Z (`0a947514`). Round 1's "newest beacon 03:05Z Oct 5" came from codebreaker's private retrieval lane, not public reports — not re-verifiable here.
- Honest limits (first-class): (a) public scans are 15–25h stale relative to filing (08:45 UTC Oct 5); "alive right now" is really "alive as of last public scan"; (b) a 200 on the inbox page proves the token isn't expired/deleted (free-tier expiry ~2026-10-11 per Round 1), NOT that beacons are landing; (c) `e691f66e`'s request list was **empty at 07:20Z** — token alive, no beacons observed in the public scan; (d) authenticated urlquery API 429'd twice (same as Round 1 cheerleader) — htmx search may miss newer reports, so absence of Oct-5 scans is a weak negative, not a dead verdict.
- No inbox moves to dead on public evidence. Recommend re-sweep via authenticated API once the 429 cools, or accept the private-lane beacon data as the fresher signal.

---

## FINDING 2 — letss.win passive re-examination (WOUND job 2)

**Claim:** No agent-linkage evidence found; the "human/pentester" read is neither confirmed nor refuted, but one supporting marker has partially evaporated. letss.win stays WATCHLIST.

**Evidence (PUBLIC SOURCE — Shodan stored records, pulled 2026-10-05 ~08:30 UTC):**

- `95.169.18.20` — org `Cluster Logic Inc`, ISP `IT7 Networks Inc`, AS25820; hostnames `letss.win`, `95.169.18.20.16clouds.com`; ports `:2083` ("Ncat http proxy") + `:8443` (nginx, title `Httpbun`); stored last_update 2026-10-02T20:58Z. **Ncat STILL PRESENT here.**
- `207.57.145.214` — org/ISP `NTT America, Inc.` (stored ISP field `Zont LLC`), AS1054; hostname `letss.win`; stored ports now `:22` (OpenSSH) + `:8443` (nginx, title `Httpbun`); stored last_update 2026-10-04T03:08Z. **:2083 Ncat GONE from the stored record** (it was present at Round 1). Either the operator shut it down/moved it, or it's rescan variation — INFERENCE either way, labeled.
- Shodan DNS for `letss.win`: wildcard `*` + subdomain `drone` present; `drone.letss.win` has ZERO Shodan host records (DNS-only). GENUINELY NEW (to our records) — naming is lab-flavored ("drone") but that is INFERENCE, not attribution.
- `hostname:"letss.win"` search: exactly 2 hosts (the two known), no third node; .214's indexed observation is from 2026-09-19 (older than the host record's 2026-10-04 update).
- Certs on :8443: Let's Encrypt, `*.webhook.site`-style single-domain certs — commodity, nothing agent-shaped.
- Zero hits for either IP in `oai-traces` traces.jsonl (589,972 events) and the Amap fleet events.jsonl (2,141 events) — agent-linkage dead, unchanged.

**Classification:** OURS (the two IPs) / evidence PUBLIC SOURCE.

**Actionability:**
- The :2083 disappearance on `.214` (last_update 2026-10-04) is the first *change* in this cluster since Round 1 — weak support for the "pentester tidying infra" read, or weak noise. Do NOT upgrade to a verdict.
- letss.win remains WATCHLIST (unattributed infra oddity). Upgrade condition unchanged: agent-traffic co-occurrence or a second independent pivot.
- Note for the record: `.20`'s secondary hostname `95.169.18.20.16clouds.com` (16clouds = budget VPS reseller naming) corroborates the commodity-VPS read of that node.

---

## FINDING 3 — The 16 staging hosts: platform verdict (job 3, umbrella)

**Claim:** All 16 staging-host entries (12 unique hostnames) are tenant sites on commodity serverless/static platforms — no dedicated IPs, no VPS fingerprints, nothing to attribute at the network layer.

**Evidence:**
- 10 × `*.pages.dev` → Cloudflare Pages (Cloudflare's Pages domain — KNOWN, public).
- 1 × `crunch26.vercel.app` → Vercel (`*.vercel.app` — KNOWN).
- 1 × `rodeo-admin-uk.onrender.com` → Render (`*.onrender.com` — KNOWN).
- Shodan stored DNS returns no A-record data for any of the 12 (domain metadata only: `ipv6` tags on the pages.dev entries, `_dmarc` subdomain on the onrender entry) — PUBLIC SOURCE, honest null.
- Direct DNS from this VM resolves to 198.18.19.161–.172 (RFC 2544 benchmarking range) — the VM's egress proxy intercepts DNS; discarded as poisoned, noted so nobody cites it.
- Zero hits for all 12 hostnames in `oai-traces` traces.jsonl (589,972 events) — these hosts are unique to the Chinese Amap fleet corpus (OURS, GENUINELY NEW to the inventory).

**Classification:** OURS (inventory) / evidence PUBLIC SOURCE + INFERENCE (naming reads below).

**Actionability:** No IP-level follow-up is possible or meaningful — shared-platform tenancy. The only muscle left is naming grammar (findings 4–7, all INFERENCE, labeled) and the one public-scan anomaly (finding 8).

---

## FINDING 4 — livecodes-sandbox.pages.dev — agent-shaped name, commodity platform

**Claim:** Of the 12, this is the most campaign-coherent name: a LiveCodes sandbox staged on Cloudflare Pages, matching the campaign's `livecodes-carrier` class (26 URLs in the same inventory).

**Evidence:** OURS — appears in `url-inventory-chinese-swarm.jsonl` as staging-host; the same inventory's `livecodes-carrier` class (26 unique URLs) shows the fleet operators build LiveCodes payloads. PUBLIC SOURCE — urlquery htmx search for the hostname returns zero reports (weak negative per the documented caveat).

**Classification:** OURS / GENUINELY NEW / evidence OBSERVED (inventory) + INFERENCE (the campaign-coherence read).

**Actionability:** Weak agent-infra-shaped signal by name + corpus context only. Do not cite as agent-linked without a second pivot. Watchlist-grade.

---

## FINDING 5 — Auto-generated / gibberish names — commodity noise (INFERENCE)

**Claim:** `meta-vimaro-biz-zeluno-panaki.pages.dev`, `deliveryrange.pages.dev`, `yanruilinforming-contact-redirect.pages.dev`, `contact-3vq.pages.dev` read as platform-generated or throwaway deployment names — consistent with either a human dev's scratch deploys or an agent's disposable staging. No discriminator available.

**Evidence:** OURS (inventory, occ=1–2 each); zero urlquery htmx hits for `meta-vimaro-biz-zeluno-panaki.pages.dev` and `deliveryrange.pages.dev` (sampled; weak negatives).

**Classification:** OURS / evidence INFERENCE.

**Actionability:** None — honest null on attribution. Logged for naming-grammar completeness.

---

## FINDING 6 — Dev-tooling-shaped names — human-dev-flavored (INFERENCE)

**Claim:** `markdown-to-livecodes-vitepress.pages.dev`, `cloudflare-imgbed-atb.pages.dev` ("imgbed" = image-bed, Chinese dev slang 图床), `routecraft-recovery.pages.dev`, `crunch26.vercel.app` read as human developer side-projects (docs tooling, image hosting, a "26" iteration counter).

**Evidence:** OURS (inventory); naming semantics only.

**Classification:** OURS / evidence INFERENCE.

**Actionability:** None. These lower the "agent staging farm" temperature of the set — a mixed human/agent or human-dev staging list is the honest read.

---

## FINDING 7 — forever811-github-io.pages.dev + logic3579-github-io.pages.dev — GitHub-Pages-mirror naming (INFERENCE)

**Claim:** The `*-github-io` pattern suggests GitHub Pages sites (`forever811.github.io`, `logic3579.github.io`) mirrored through Cloudflare Pages; the numeric suffixes look like generated/throwaway GitHub accounts.

**Evidence:** OURS (inventory, occ=1 each); zero urlquery htmx hits for `forever811-github-io.pages.dev` (weak negative).

**Classification:** OURS / evidence INFERENCE.

**Actionability:** None directly — but if Round 3+ wants a cheap pivot, GitHub-side checks for `forever811` / `logic3579` accounts are the lane (public profile/org pages only — no operator-identity work; repo existence and Pages config are infra facts).

---

## FINDING 8 — rodeo-admin-uk.onrender.com — login-form app, one public scan predating the fleet wave

**Claim:** A "Rodeo"-branded admin **login page** (email + password fields, show-password icon, `rodeo-blue-logo.svg`, Vite-built SPA) on Render — scanned once by urlquery on 2026-08-26, five weeks before the Sep-28 fleet wave. Its role as a "staging host" in the fleet corpus is unexplained.

**Evidence (PUBLIC SOURCE):**
- urlquery htmx search: exactly 1 report, `3db0eb41-6e15-403b-84b1-3c9ef8cd9811`, 2026-08-26T10:58Z.
- filter/http transactions: 12 requests, all 200 OK — `/` + `/assets/index.*.js|css` + `EmailIcon`/`PasswordIcon`/`ShowIcon` SVGs + `rodeo-blue-logo.svg` + Google Fonts (Maven Pro, Inter) + `assets/generated.270e5a1d.png` (280 kB hero image). No verdict text extracted (title not captured in the htmx fragment).
- OURS: appears twice in the fleet inventory as staging-host (occ=2 counting the trailing-slash dup).

**Classification:** OURS (inventory presence) / GENUINELY NEW (the login-form observation) / evidence PUBLIC SOURCE.

**Actionability:**
- Off-frame lead, per doctrine — not dismissed: a login-form app sitting in an *agent fleet's* staging inventory is worth one more passive look, not a verdict. It may be a phishing kit, a legit client's admin panel, or an agent's credential-harvesting test target — all INFERENCE, none evidenced.
- Do NOT probe it (standing rule). Passive options: urlquery `related/domain` for `onrender.com` is noise (shared platform); a `related/screenshot` htmx pull would show the login page visually without touching the host — suggested as a cheap Round 3 micro-task.
- Not agent-linked. Not cited as such.

---

## FINDING 9 — The 5 hospital targets are grammar, not infra (honest null + off-frame lead)

**Claim:** `GZHOSP-topbackend-1791106056744`, `GZHOSP-topditussr-1791106056744`, `GZHOSPPLACE1791105253174`, `GZHOSPbackend1791105292618`, `GZHOSPssrwww1791105289756` are tag-grammar markers (GZ = Guangzhou hospital backends), not hosts — there is no IP/ASN layer to work. Infra muscle: null.

**Evidence:** OURS — `url-inventory-chinese-swarm.jsonl`, class `hospital-backend-target`, 10 contributing records.

**Classification:** OURS / evidence OBSERVED (inventory).

**Actionability:** Off-frame lead for the grammar lanes (not the Thug's): hospital-backend targets in an agent fleet's tag vocabulary are worth the codebreaker's attention, not the infra lane's. Logged here so it isn't lost — "don't dismiss it just because it doesn't fit yet."

---

## Ledger notes for the Chair

- No settled kill was re-litigated. 62.234.187.97, the jina lookalikes, 178.63.67.106: untouched, stay downgraded.
- letss.win: WATCHLIST maintained; one delta (:2083 gone from .214's stored record as of 2026-10-04) logged with honest INFERENCE grading.
- Alive/dead ledger: 4 ALIVE / 0 confirmed dead on public evidence; newest public state 2026-10-04T17:12Z; `e691f66e` token-alive but request-list-empty at its scan.
- 16 staging hosts → 12 unique hostnames, all commodity platform tenancy; 0 cross-corpus hits in 589,972 oai-traces events; 1 public-scan anomaly (rodeo login app, 2026-08-26).
- Authenticated urlquery API 429'd twice this round — htmx keyless was the working lane; all htmx zeros carry the documented weak-negative caveat.
- Pending lanes (studies/skill-egress-top500/, studies/shodan-chat-transcripts/) not touched per instructions.
