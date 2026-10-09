# Trick sweep: TUNNELS + FILE DROPS

- Date: 2026-10-04 (sweep run)
- Trick classes: tunnel services (ngrok, cloudflared quick tunnels, bore/bore.pub, zrok, inlets, sish public instances) and file drops (transfer.sh, file.io, 0x0.st, catbox.moe, litterbox)
- Scope: AGENTS AND SWARMS only. Known-operator context excluded from "new": the Chinese Amap-map data-collection fleet on `<hex>.lhr.life` tunnels serving `uqcors.html`/`probe.html` (Jan–Oct 2026).
- Method: web search per service for public indexes/searches of active/past tunnel URLs and public file listings; marker searches (`uqscan=`, `uqcors.html`, `probe.html`, `lhr.life`, `pandalegacy`, tunnel-URL patterns); page-source inspection for undocumented XHR/fetch endpoints via `browser.open` text fetch; curl attempted from VM.
- Infrastructure caveat (2026-10-04): direct curl egress from this VM was broken during the sweep — `transfer.sh`, `0x0.st`, `catbox.moe`, `file.io`, `litterbox.catbox.moe`, `crt.sh`, and even `google.com`/`github.com` all timed out through the egress proxy. `browser.open` text fetch worked for `0x0.st` and `catbox.moe` homepages. Findings below distinguish "service dead" (corroborated by third-party uptime monitors) from "unreachable from this VM".

## TUNNELS

### ngrok (`*.ngrok-free.app`, `*.ngrok-free.dev`, legacy `*.ngrok.io`)
- Public index of active/past tunnel URLs? **No.** ngrok keeps the tunnel registry private; no public directory, search, or API for third-party tunnel URLs exists.
- Partial third-party surfaces: Certificate Transparency (crt.sh) lists *reserved/custom* ngrok domains, but free-tier subdomains sit behind ngrok's wildcard certs, so CT does not enumerate them. Shodan/Censys can match ngrok edge certs but not individual free tunnels.
- Marker results: web search for ngrok + `uqcors`/`probe.html`/`lhr.life` → no agent-fleet hits.
- Undocumented endpoints: none found; ngrok's public surface is docs + dashboard (auth-gated).
- Verdict: clean negative — no public index to mine.

### cloudflared quick tunnels (`*.trycloudflare.com`)
- Public index of active/past tunnel URLs? **No.** No search engine, directory, or public list of quick-tunnel URLs exists (verified via search: only tutorials and "pet URL" obituaries — e.g. Medium piece on ephemeral `fluffy-cat-47`-style names).
- Quick-tunnel names are 4 random words + digits (`alice-ion-married-knights`), rotate on restart; not guessable, not indexed.
- Partial third-party surfaces: CT may capture some `*.trycloudflare.com` issuances (Cloudflare edge certs), but no marker-keyed search is possible without enumerating the whole space; Cloudflare wildcards blunt this. Shodan `ssl:"*.trycloudflare.com"` is a known pivot but key-gated for bulk.
- Notable for agents: `cloudflared` now emits structured JSON (hostname/edge/health) on stdout specifically so coding agents can parse the URL without regexing logs (Prism Labs video, Sep 2026). Agent skill found: `themajc/agent-skills` `publish-to-trycloudflare` — agents publish local ports to trycloudflare as a matter of routine. So the *class* is agent-favored, but there is no index to sweep.
- Marker results: `"trycloudflare.com" "probe.html" OR "uqcors" OR "lhr.life"` → zero agent hits.
- Verdict: clean negative on public index; agent-usage confirmed via skill.

### bore / bore.pub
- Public index? **No, and structurally impossible for the public server**: bore is TCP-only; `bore.pub` hands out random *ports* (`bore.pub:32371`), not subdomains — nothing DNS-indexable, nothing to enumerate.
- Public bore *server* lists exist in awesome-tunneling repos (slimshizn/awesome-tunneling, securepeacock/awesome-tunneling), but those are server addresses, not active tunnels.
- Agent usage confirmed: `dtrhnet/manus-expose-endpoints` SKILL.md exposes SSH+VNC via `bore.pub:<assigned-port>`; `finddatatechnology/fd-vaas-skills` `fd-coding-bore-tunnel` skill; `anistark/wasmrun` added bore tunneling (`--expose`, default `bore.pub`) on 2026-09-28. Agents reach for bore.pub because it needs no account/card (a repo README documents switching from ngrok to bore specifically to avoid ngrok's credit-card requirement for TCP).
- Verdict: clean negative on index; high agent affinity documented.

### zrok (`*.share.zrok.io`)
- Public index of active shares? **No.** Private shares create no DNS record at all (token-based, `zrok access private <token>`). Public shares get `https://<name>.share.zrok.io`; no public directory.
- Note: zrok 2.0 (early 2026) renamed binary to `zrok2`, env dir `~/.zrok2`, replaced reserved shares with namespaces — older tutorials are stale.
- Self-hostable (OpenZiti overlay) → operator-run zrok instances are invisible.
- Verdict: clean negative.

### inlets
- Public index? **No.** inlets is now a commercial self-hosted product (inlets.dev); there is no shared public relay and no URL index. The old OSS `inlets` is archived.
- Verdict: clean negative, low fleet relevance (paid, self-hosted).

### sish public instances
- Public *instance* lists exist (awesome-tunneling repos list e.g. `tuns.sh` — pico.sh's sish backend, `ssh -R dev:80:localhost:3000 tuns.sh` → `https://{user}-dev.tuns.sh`), but **no index of active tunnel URLs**.
- sish typically front-ends with wildcard certs, so CT does not enumerate per-user subdomains.
- localhost.run is covered by a sibling lane — not redone here.
- Verdict: clean negative on active-tunnel index.

### Adjacent lead (not in assigned set, noted): pinggy.io
- SSH-based, free tier (`*.a.pinggy.link`), no download — surfaced repeatedly in awesome-tunneling lists alongside sish. Same index-less profile. Worth a sibling sweep if SSH-tunnel lanes expand.

## FILE DROPS

### transfer.sh — DEAD
- Service is **down/shut down**. Third-party monitors: notopening.com shows `Down` continuously 2026-07-30 → 2026-10-02; websitedown.info (2026-10-02) reports unavailable for everybody; javier-lopez/learn commit (2026-09-13): "transfer.sh talked to a file sharing service that shut down" — tooling dropped it.
- This VM's timeout is consistent with the service being gone, not just VM egress.
- Verdict: not a viable current drop; historical URLs (`transfer.sh/<id>/<file>`) may still appear in old corpora — worth grepping existing datasets, not the live web.

### file.io
- Public file listing/searchable index? **No.** Files are unguessable URLs, auto-deleted after first download; no directory, no search.
- API is documented (POST upload → JSON with link). No undocumented XHR endpoints found (homepage unreachable from VM during sweep; API shape is public knowledge).
- Note: `qianhuisunny/storyboard` (2026-04-10) evaluated file.io for an agent media pipeline and rejected it (first-download deletion breaks retries) — agents have considered it.
- Verdict: clean negative on public listing.

### 0x0.st — no public listing; operator metadata exists but is private
- Public listing? **No.** Upload API fully documented on the homepage (fetched live via browser.open 2026-10-04): `curl -F'file=@f' https://0x0.st`; fields `file`/`url`/`secret`/`expires`; management via `X-Token` response header (POST token+delete to file URL).
- Undocumented XHR endpoints: none — the whole API is on the static homepage; no JS frontend to mine.
- Metadata note (per its privacy policy): uploader **IP address and User-Agent are stored with each file** for moderation, not shared with third parties. Tor exits are firewall-blocked; browser-masquerading UAs are auto-blocked. So the operator *has* attribution metadata, but it is not publicly queryable — a lead only via abuse-report/legal channel, not OSINT.
- Also runs `hole.0x0.st` (WebWormhole instance, no TURN relay).
- Verdict: clean negative on public listing; operator-side metadata is the only attribution surface.

### catbox.moe / litterbox.catbox.moe
- Public listing/searchable index? **No.** Unguessable URLs (`files.catbox.moe/<id>.ext`, `litter.catbox.moe/<id>.ext`); no directory, no search.
- Upload API is documented (`https://catbox.moe/user/api.php`, `reqtype=fileupload`); litterbox adds `time=1h/12h/24h/72h`. No undocumented XHR endpoints found via text fetch (homepage fetched live; JS-heavy, no endpoint strings in text).
- Agent usage confirmed and notable: litterbox is the temp-file host baked into multiple agent browser skills — `padmanabhansb08/brozer-v2` and `webbrain-one/webbrain` `temporary-file-share-litterbox.md` skills (upload via page, read link from `.responseText`), and `qianhuisunny/storyboard` chose litterbox over 0x0.st/file.io/catbox for an agent video pipeline (ephemeral, multi-fetch, network-reachable). Litterbox stores uploader IP with the upload (per skill docs).
- Verdict: clean negative on public listing; highest agent affinity of the file drops in this set.

## MARKER SEARCHES (web index)
- `"pandalegacy"` → only Fortnite Creative map creator noise (fchq.io, fortnitecreativehq.com). Clean negative for agent relevance.
- `"uqcors.html"` → zero indexed hits. The known Amap fleet's probe pages are invisible to web search.
- `"uqscan="` → zero relevant hits.
- `"trycloudflare.com" "probe.html" OR "uqcors" OR "lhr.life"` → zero agent hits.
- `bore.pub` + probe/agent → only the agent-skill usage above, no fleet.

## THIRD-PARTY INDEX SURFACES (partial coverage)
- **crt.sh (Certificate Transparency)**: the canonical public index for *issued subdomains* (`%.trycloudflare.com`, `%.ngrok-free.app`, `%.share.zrok.io`). Wildcard certs blunt per-tunnel enumeration for ngrok free tier and sish. Direct query from this VM timed out (egress); query shape is `https://crt.sh/?q=%25.<domain>&output=json`.
- **Shodan/Censys**: `ssl.cert.subject.cn` pivots for tunnel domains; bulk use is key-gated.
- **urlscan.io**: tunnel/filedrop URLs appear when researchers submit them; search API is key-gated (public UI only).
- **Common Crawl**: monthly URL index is a public historical-URL source; Sep 2026 index is `CC-MAIN-2026-39` (verified live via collinfo.json). A `*.trycloudflare.com` + `filter=url:.*probe.*` query returned HTTP 503 from the index API during the sweep — dropped per no-retry rule; retry from a healthier network later.
- **Wayback CDX**: `web.archive.org/cdx/search/cdx` domain query for trycloudflare.com returned upstream 500 — dropped per no-retry rule; this is a sibling lane (Wayback CDX incident-window sweep) anyway.

## UNDOCUMENTED ENDPOINTS FOUND
- None. All five file drops expose only their documented upload APIs; no hidden XHR/fetch endpoints were discoverable through homepage text fetch. (curl-based page-source mining was blocked by VM egress failure, not by the services; 0x0.st and catbox.moe homepages were still inspected via browser.open.)

## NEW LEADS (not findings — for parent to route)
1. **Agent skills as the tunnel/drop census**: the strongest signal this sweep produced is that agent *skill repos* document which tunnels/drops agents actually use (bore.pub ×3 skills, trycloudflare ×1 skill, litterbox ×4 skills). A skill-repo sweep keyed on tunnel/drop hostnames would enumerate agent-facing usage far better than any URL index. Overlaps the skill-tracer project.
2. **0x0.st operator metadata**: IP+UA stored per file, Tor blocked, browser-UA spoofing auto-blocked — if a fleet used 0x0.st, the attribution trail exists operator-side only.
3. **transfer.sh is dead** — any fleet still referencing it is stale; historical `transfer.sh/<id>/` URLs in existing corpora may still be worth grepping.
4. **pinggy.io** (`*.a.pinggy.link`) — SSH-tunnel free tier adjacent to the assigned set; suggest adding to a future sweep.
5. **Common Crawl retry**: `CC-MAIN-2026-39-index?url=*.trycloudflare.com&output=json&filter=url:.*probe.*` 503'd once; worth one retry from healthy egress, plus `files.catbox.moe` and `0x0.st` URL enumerations.
