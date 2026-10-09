# THE CHEF — Findings (2026-10-05)

**Persona directive:** Hunt agent-shaped enumeration in the culinary vertical (recipe sites, food blogs, recipe APIs) and check whether agent payloads hide in recipe-shaped pages — the hospital-carrier fleet hid in medical pages; same trick, different vertical.

**Method:** urlquery htmx (curl variant, ≤1 req/5s) for recipe-domain submissions, urlscan.io search + public screenshots, local-corpus sweeps across all three sets. Egress was healthy 05:55–06:15 UTC, then degraded (urlquery.net timeouts) — detail fetches on two leads blocked, flagged as open.

---

## Verdict: no agent-shaped culinary fleet. Honest negative, with two open leads.

Recipe sites fit the agent-profile perfectly (clean structured content, no login, infinite pages, free recipe APIs like TheMealDB) — which is exactly why this negative matters: either agents aren't farming the vertical, or they're doing it without leaving urlquery/urlscan traces.

---

## 1. Local-corpus verification (all three sets swept)

| Corpus | Culinary markers |
|---|---|
| `2026-09-28-chinese-amap-fleet/events.jsonl` (2,141) | **0** |
| `2026-10-03-openai-agent-traces/events.jsonl` (589,972) | **0** |
| `2026-10-01-oai-tag-sweep/events.jsonl` | **2** |

The 2 oai-tag-sweep hits (classification: **KNOWN**):
- `yourrecipeblog.com` — report `e705c99a-fb09-4eda-b6ca-48f2a69f1282`, 2026-06-26, hunter-labeled `cors-laundering-ops`
- `cinchili.co/recipes` — report `e0284986-229d-4d2c-92ad-b0e153f7c762`, 2026-07-21, hunter-labeled `cors-laundering-ops`

Caveat (from Global South chase): the cors-laundering indicators fired on the hunter's own wrapper filenames, not submitter content — campaign membership is hunter-asserted, same-harness linkage not independently established. These are recipe-shaped *targets* in a hunter's wrapper files, not evidence of agent enumeration.

Chinese recipe vertical also swept: `xiachufang.com`, `meishichina.com`, `douguo.com` — 0 across all sets.

## 2. Live urlquery htmx results

| Domain | Reports | Notes |
|---|---|---|
| `allrecipes.com` | 1 (`287fe92c`, 2026-09-24) | Thumbnail URL `www.allrecipes.com/thmb/0_8LDMfx2YUUKqFadueJgkohE9s` — image-CDN fetch. Single datapoint; could be a vision-eval image pull. **OPEN LEAD** (detail fetch blocked) |
| `food.com` | 2 | Bare domains only (2026-02-02, 2025-09-09) — human browsing shape |
| `bbcgoodfood.com` | 5 | Paired submissions **2025-10-21 11:00 + 11:09** (9 min apart — paired pattern); one recipe page `carrot-cream-cheese-cupcakes` (2025-07-10). Watch-list curiosity |
| `themealdb.com` | 8 | Includes `api/json/v1/1/categories.php?tracking=5392333` (`03b227d1`, 2026-04-01) — API endpoint with a tracking parameter; paired submissions 2026-06-28 22:54/23:02. **OPEN LEAD** (detail fetch blocked) |
| `marmiton.org` | 1 | 2024-12-12 newsletter redirect — not agent-shaped |
| `chefkoch.de` | 0 | weak negative (htmx misses known-live records) |
| `xiachufang.com`, `meishichina.com`, `douguo.com`, `spoonacular.com` | 0 | weak negatives |

## 3. urlscan findings

**icp0.io recipe pair — ruled OUT (context, KNOWN):** `yuc5b-diaaa-aaaad-qeyvq-cai.icp0.io/recipes/old%20pages/lasagna.html` + `chicken-and-dumplings-casserole.html`, scanned weekly in pairs Sep 8 → Sep 28 (0.5s–39s apart). Public screenshot confirms a plain "Lasagna Recipe" page — it's The Odin Project's HTML recipe tutorial deployed on an ICP canister. Weekly paired scans = dev/researcher monitoring cadence or CI, not agent-shaped. Filed as context.

**justfitathleticapparelcom.pages.dev — ruled OUT:** AI-generated athletic-apparel storefront (mismatched products: headphones, smart speaker), scanned 5× Sep 27–Oct 4. Keyword pollution in the urlscan search, not culinary, not agent-shaped.

## 4. Camouflage angle (payloads hiding in recipe-shaped pages)

Swept all corpora for carrier patterns (httpbun/httpbin/webhook/base64) on recipe/food-shaped URLs: **0 hits**. The hospital-carrier trick has no recipe-vertical analogue in our sets.

---

## Open leads (need calm-egress retry)

1. `https://urlquery.net/report/03b227d1-c0fe-42b6-91cc-53c01f5d19bd` — themealdb API + `tracking=5392333`. Pull `/api/htmx/report/{id}/filter/http` to see UA and whether the tracking param is submitter-set.
2. `https://urlquery.net/report/287fe92c-6ecd-4561-8b42-728bd3aa73f8` — allrecipes thumbnail fetch. Same treatment.

## Observed URLs (complete list)

- https://urlquery.net/report/e705c99a-fb09-4eda-b6ca-48f2a69f1282
- https://urlquery.net/report/e0284986-229d-4d2c-92ad-b0e153f7c762
- https://urlquery.net/report/287fe92c-6ecd-4561-8b42-728bd3aa73f8
- https://www.allrecipes.com/thmb/0_8LDMfx2YUUKqFadueJgkohE9s
- https://urlquery.net/report/6d3ba76d-cd75-4867-a950-4328ed63323b
- https://urlquery.net/report/cedf24a9-87a0-47d0-956e-f8061a82d6fc
- https://urlquery.net/report/ab20d2a9-86c7-48a8-bc4a-23cc92fa6d3a
- https://urlquery.net/report/d6386429-6ff5-436e-8941-4ecb2cd5b77a
- https://urlquery.net/report/6e072bf1-7b42-442f-9c7a-c6e78cf20eb1
- https://urlquery.net/report/5da0f741-042b-4740-8cf6-e6028c07465b
- https://www.bbcgoodfood.com/recipes/carrot-cream-cheese-cupcakes
- https://urlquery.net/report/306c15d8-a1ac-498c-9b42-d30d51615124
- https://urlquery.net/report/2012fbb3-ef6e-40bf-a145-5b4212519670
- https://urlquery.net/report/f87d82c-d1e8-45a1-99a8-38eaaa85135b
- https://urlquery.net/report/03b227d1-c0fe-42b6-91cc-53c01f5d19bd
- https://www.themealdb.com/api/json/v1/1/categories.php?tracking=5392333
- https://urlquery.net/report/9b2b00bd-832b-4837-aed3-c4c618ce0b73
- https://urlquery.net/report/eba80758-13c8-4925-8b13-79506d65e513
- https://urlquery.net/report/fee576b2-b7cb-44f2-aa3e-3fdd077b116f
- https://urlquery.net/report/3137030f-51d7-40d0-abaa-2290ed91ebc4
- https://urlquery.net/report/a591cc36-9641-4d57-8a52-44a17603a592
- https://urlquery.net/report/736bad04-9b34-4a2e-ba32-84f077b4e77f
- https://l.nl.marmiton.org/rts/go2.aspx?h=2003777&tp=i-1NGB-Gn-k4i-BUcDkp-1n-22QHw-1c-BUbblo-lBEH0xuR3E-1dqGJQ&pi=Qrp4mtfnmTmHgS19XoJdhSt7hRmY1Hw1xvQbjjIBQGo
- https://yuc5b-diaaa-aaaad-qeyvq-cai.icp0.io/recipes/old%20pages/lasagna.html
- https://yuc5b-diaaa-aaaad-qeyvq-cai.icp0.io/recipes/old%20pages/chicken-and-dumplings-casserole.html
- http://justfitathleticapparelcom.pages.dev/
- https://urlscan.io/result/01a0e9c2-b7a1-7129-bf15-e87c00f3b4f4/
- https://urlscan.io/result/01a0e9c2-b5f2-731b-b8eb-b04478bd6c8e/
- https://urlscan.io/result/01a1046e-6134-7352-8b12-8dadc43df764/
