# Screenshot-services + staged-programs sweep — 2026-10-04

**Lane:** screenshots + staged programs (CodePen, JSFiddle, StackBlitz, Observable, Glitch, Replit, Vercel/Netlify deploys, Cloudflare Pages/Workers). LiveCodes handled by a sibling lane — not redone.
**Task:** hunt undiscovered agent/swarm fleets via screenshot services (public galleries? searchable submission histories?) and staged-program hosts (searchable without account?), using our markers.
**Method:** web search `site:` scoping per service + marker queries; page-source/XHR endpoint probing per the no-key curl doctrine; capability verification per service.
**Sweeper:** subagent (depth 2), 2026-10-04 ~22:50–23:15 CDT.

## Verdict: NO new agent/swarm hits. Two infrastructure notes, one scoping-critical.

No staged pens/fiddles/notebooks/deploys and no screenshot-service artifacts matching our markers were found on any service checked. All marker-scoped searches returned clean zeros.

- **INFRASTRUCTURE (scoping-critical): Glitch is DEAD.** Project hosting ended 2025-07-08 (Fastly/Anil Dash announcement; cited unsustainable cost + abuse/phishing). `*.glitch.me` subdomains are dead, user profiles are gone, `api.glitch.com` is unreachable (connection reset from this VM). Glitch is no longer a live staged-program surface — the only remaining trace is archival (ArchiveTeam enumeration corpus, Wayback).
- **Corroboration, not new:** `"injectPageScript"` is a documented **Jina Reader API parameter** (`curl -F "injectPageScript=..." https://r.jina.ai/`, jina-ai/reader cookbooks.md) — matches the known ltzh-family TTP of running JS via Jina. All other `injectPageScript` web hits are generic browser-extension boilerplate. No new fleet.

---

## SCREENSHOT SERVICES

**Class verdict: none offers a public gallery or searchable submission history.** The "what URLs were screenshotted" question is unanswerable on every service checked — all are forward-addressable only (you can request/retrieve a shot for a URL you name, but you cannot enumerate what others submitted).

### screenshotone.com
- Keyed API (`access_key` param/header/body), no public gallery, no history endpoint. Take endpoint: `GET /take`. Bulk endpoint documented. Private accounts only.

### urlbox.com / api.urlbox.io
- API key + secret with **signed URLs** (`/v1/<KEY>/<TOKEN>/png?url=...`). Private accounts, no public gallery, no history endpoint.

### browshot.com
- API-key service (`api.browshot.com/api/v1/simple?url=...&key=...`). Has an **opt-in "share"** feature (`/screenshot/share`) creating a public page per shared screenshot — individual pages only, **not enumerable, not searchable as a corpus**. No public gallery.

### thum.io
- The only one with anything called a gallery: `https://www.thum.io/gallery` — **top-500 websites, curated static marketing page** (verified by fetch 2026-10-04; no live submission feed). No history/search of submissions.
- Free endpoint `https://image.thum.io/get/<options>/<url>` is addressable per-URL (cached ~24h via `maxAge/24`) but **not enumerable**.
- `"image.thum.io/get" uqscan OR "lhr.life" OR webhook` → 0 agent hits (noise only: PDFs, a UK scanning directory, wiki docs).
- Free tier now requires signup/API key for bulk; per-URL get remains unauthenticated.

### wordpress mshots (`s0.wp.com/mshots/v1/<url>`)
- Fully public per-URL endpoint, no key at all. First hit redirects to `/mshots/v1/default` while rendering. **No gallery, no history, no index.**
- `"s0.wp.com/mshots/v1" uqscan OR "lhr.life"` → 0 agent hits (2 noise PDFs matched "lhr" in unrelated content).
- Note: pages embedding mshots thumbnails (friend-link themes, verifiers like verify-www.com) are Google-indexed — that is the only enumerable mshots surface; searched clean.

---

## STAGED PROGRAMS

### CodePen — SEARCHABLE without account
- `https://codepen.io/search/pens?q=<query>` works logged-out; pens public by default.
- **No public JSON search API exists.** The unofficial cpv2api (`cpv2api.com/search/pens?q=`) has been dead since ~2017. Search page is server-rendered; no keyless XHR endpoint found (curl egress from this VM to codepen.io fails — hang — so endpoint discovery was via docs/search only; browser text-fetch of the search page returned 403 from the fetch service).
- `site:codepen.io uqscan OR uqcors` → 0 results. Clean.
- Endpoint documented: **none** — use the `?q=` page in a live browser.

### JSFiddle — NOT searchable (by design)
- No global keyword search has ever shipped (feature request open since 2017; codebase frozen). Google is the only cross-fiddle surface.
- **Documented public API (per-user only):** `GET https://jsfiddle.net/api/user/:username/demo/list.json` — params `callback` (JSONP), `start`, `limit`, `sort` (date/alphabetical/framework), `order` (desc/asc), `framework`. Returns `{status, list:[{title, description, author, url, created, framework, version, latest_version}], overallResultSetCount}`. No keyword search — user-scoped enumeration only.
- `site:jsfiddle.net uqscan OR uqcors OR "lhr.life"` → 0 results. Clean.

### StackBlitz — NOT searchable without account
- No global public project search; profiles + GitHub-linked projects; in-app search is own-projects only.
- `site:stackblitz.com uqscan OR uqcors OR "lhr.life"` → 0. `site:stackblitz.io ...` → 0. Clean.

### Observable — SEARCHABLE without account
- Public search at `https://observablehq.com/search` — docs confirm: search box on every page covers any user's **public** notebooks (case-insensitive, implied AND, `*` prefix wildcards, tag search, user scoping). No login needed.
- **Public notebook doc endpoint** (used by the notebooks-visualizer notebook itself): `https://observablehq.com/api/document/@<user>/<slug>` (also by id, by URL). Public notebooks fetchable keyless.
- `site:observablehq.com uqscan OR uqcors OR "lhr.life"` → 0. Clean.
- **Gap:** could not run a live Observable search from this VM (curl to observablehq.com times out; fetch service 429'd). Needs a live-browser follow-up with queries like `"uqscan"`, `"webhook.site"` image-beacon code, `fetch(` to webhook URLs, `injectPageScript` usage.

### Glitch — DEAD (hosting ended 2025-07-08)
- Project hosting + user profiles shut down 2025-07-08 (Fastly; abuse costs). Dashboard code-downloads through end of 2025; subdomain redirects die end of 2026.
- ArchiveTeam documented enumeration endpoints — `https://api.glitch.com/v1/users/?limit=1000` and `/v1/projects/?limit=1000` (paginate via `nextPage`) — **dead now** (connection reset from this VM). Glitch search ran on Algolia (client-side key in page source, per glitch-api npm docs) — also dead.
- `site:glitch.com uqscan OR uqcors OR "lhr.life"` → 0. `site:glitch.me ...` → 0. Clean.
- **Follow-up:** Wayback/ArchiveTeam glitch corpora are the only remaining surface for historical agent activity here.

### Replit — community search exists but login-walled
- Old docs: dashboard search is own-repls only. Community/spotlight search requires login. Free hosting killed (~2024–2025); deployments now on `*.replit.dev` (paid).
- curl egress from this VM to replit.com fails (timeout) — no page-source probing possible from here.
- `site:replit.com uqscan OR uqcors OR "lhr.life"` → 0. Clean. (`site:replit.app uqscan` → 0.)

### Vercel / Netlify deploys — NO central public search
- No service-side search of deployments exists. Discovery surfaces: Google (`site:vercel.app`, `site:netlify.app`) and GitHub code search (auth-gated) for deploy-preview URLs in public repos.
- `site:vercel.app uqscan OR uqcors OR "lhr.life"` → 0. `site:netlify.app uqscan` → 0. Clean.

### Cloudflare Pages / Workers — NO central public search
- `site:pages.dev uqscan OR uqcors OR "lhr.life"` → 0. `site:workers.dev uqscan OR uqcors OR "lhr.life"` → 0. Clean.

---

## Marker-result matrix

| Marker | Screenshot services | Staged programs |
|---|---|---|
| `uqscan` | clean (all 5) | clean (all 8+2 domains) |
| `uqcors` | clean | clean |
| `lhr.life` | clean | clean |
| `injectPageScript` | n/a | corroboration: Jina Reader API param (known ltzh TTP); no new fleet |
| `"uqcors"` unscoped | n/a | **noise** — TON blockchain addresses (`UQCORS…`), OCR garbage in newspaper PDFs. Marker is unusable unscoped; keep it service-scoped |

## Undocumented/keyless endpoints documented (reusable)

1. `GET https://jsfiddle.net/api/user/:username/demo/list.json?start=&limit=&sort=&order=&framework=` (+`&callback=`) — per-user fiddle listing, no auth, documented but obscure.
2. `GET https://observablehq.com/api/document/@<user>/<slug>` — public notebook JSON, no auth (pattern seen in `@yhyddr/notebooks-visualizer`).
3. `https://api.glitch.com/v1/projects/?limit=1000` (+`nextPage`) — enumeration API, **dead** (hosting shutdown 2025-07-08).
4. CodePen search: **no keyless JSON endpoint** — `https://codepen.io/search/pens?q=` page only; cpv2api dead since ~2017.
5. thum.io per-URL: `https://image.thum.io/get/<options>/<url>` — forward-addressable, no enumeration.
6. mshots per-URL: `https://s0.wp.com/mshots/v1/<urlencoded-url>` — fully public, no enumeration.

## VM egress note (for future sweeps)

curl from this VM hangs/resets on: `codepen.io`, `glitch.com`, `observablehq.com`, `replit.com`, `api.glitch.com` (timeouts / conn reset / 000). Page-source XHR discovery is impossible for these from here — that work needs the live browser or a different egress. Working: github, huggingface, general search/fetch services.

## Blind spots / follow-ups

- **Live-browser:** run CodePen and Observable searches directly (`"uqscan"`, `"uqcors"`, `webhook.site` beacon code, `fetch(`→webhook shapes, Amap SDK references in public notebooks).
- **GitHub code search** (auth-gated): marker strings inside repos referencing `*.vercel.app`, `*.netlify.app`, `*.pages.dev`, `*.workers.dev`, `*.replit.dev` deployments — could surface staged fleets not indexed by web engines.
- **Wayback/ArchiveTeam glitch corpora:** only remaining Glitch surface.
- **privatebin/encrypted pastes and browshot "shared" pages:** not enumerable by construction; the blind spot stands and is noted, not cleared.

Not pushed (per brief). File written; awaiting orchestrator merge.
