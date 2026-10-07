# HTMX-FIX patches — applied 2026-10-06 (CDT)

Worker: htmx-fix patch-and-rerun. Reference verification:
`../verification/VERIFICATION.md` — `HX-Current-URL: https://urlquery.net/search?q=<query>`
ALONE restores 200 + report rows; `HX-Request` alone does NOT fix it.
Reference-good pattern: `~/workspace/skills/urlquery/bin/uq_htmx_curl.py`.

## Test outcomes (BEFORE swap, against live endpoint, known-positive query `webhook.site`)

- Patched `fetch()` of **both** scripts: `status=200`, `report_rows=49` (rows = `href="/report/"` occurrences).
- Negative control (headerless, same query): `status=204`, 0 bytes — confirms the bug and that the fix is what flips it.
- Patched copies were tested as the actual shipped code (`/tmp/reverse_tunnels_htmx_search.py`,
  `/tmp/dse_wiki_verification_expand_search.py`), then copied byte-identical into place
  (sha256 verified: reverse_tunnels=`b75f64b5...`, dse_wiki=`404428e8...`).
- Inter-request pacing in both scripts raised 2s → 5s to match the ≥5s lane rule.

## Frozen duplicates — NOT touched (known-broken by design)

- `muse-home/projects/swarmtraces-hf-corpus/data/reverse-tunnels/htmx_search.py`
  — same code as the BROKEN script, lives in the FROZEN untouched archive. Left alone.
- `muse-home/projects/swarmtraces-hf-corpus/data/dse-wiki-verification-2026-09-27/expand_search.py`
  — same code as the UNKNOWN script, lives in the FROZEN untouched archive. Left alone.

Any future use of these frozen copies must add `HX-Current-URL` first, or their "zero results" are 204 artifacts.

---

## Patch 1 — `scripts/archive/collectors/urlquery/reverse_tunnels_htmx_search.py` (BROKEN → fixed)

```diff
--- scripts/archive/collectors/urlquery/reverse_tunnels_htmx_search.py (BEFORE)
+++ scripts/archive/collectors/urlquery/reverse_tunnels_htmx_search.py (AFTER)
@@ -13,9 +13,17 @@
     "label_handle": "ResearchHelperNovOne",
 }
 
-def fetch(url):
+def fetch(url, current_url):
     try:
-        r = urllib.request.Request(url, headers={"User-Agent": "swarmtraces-hunt/lane-c"})
+        r = urllib.request.Request(url, headers={
+            "User-Agent": "swarmtraces-hunt/lane-c",
+            # HTMX fix (2026-10-06): HX-Current-URL is the header that flips
+            # /api/htmx/search/ from 204 No Content to 200 + rows. Verified live
+            # (see data/2026-10-06-wikimedia-rogue-agents/htmx-fix/workers/verification/VERIFICATION.md);
+            # HX-Request alone does NOT fix it. Mirrors the skill pattern
+            # (~/workspace/skills/urlquery/bin/uq_htmx_curl.py).
+            "HX-Current-URL": current_url,
+        })
         with urllib.request.urlopen(r, timeout=60) as resp:
             return resp.status, resp.read().decode("utf-8", "replace")
     except urllib.error.HTTPError as e:
@@ -26,14 +34,15 @@
 summary = {}
 for name, q in QUERIES.items():
     url = "https://urlquery.net/api/htmx/search/?q=" + urllib.parse.quote(q) + "&limit=50&offset=0"
-    status, body = fetch(url)
+    current_url = "https://urlquery.net/search?q=" + urllib.parse.quote(q)
+    status, body = fetch(url, current_url)
     uuids = sorted(set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", body)))
     fn = f"{BASE}/htmx_{name}.html"
     open(fn, "w").write(body)
     summary[name] = {"query": q, "http_status": status, "html_bytes": len(body),
                      "uuid_count": len(uuids), "uuids": uuids}
     print(f"{name}: status={status} uuids={len(uuids)}", flush=True)
-    time.sleep(2)
+    time.sleep(5)
 
 open(f"{BASE}/htmx_summary.json", "w").write(json.dumps(summary, indent=2))
 print("done")
```

## Patch 2 — `scripts/archive/collectors/dse-wiki/dse_wiki_verification_expand_search.py` (UNKNOWN → fixed)

```diff
--- scripts/archive/collectors/dse-wiki/dse_wiki_verification_expand_search.py (BEFORE)
+++ scripts/archive/collectors/dse-wiki/dse_wiki_verification_expand_search.py (AFTER)
@@ -21,10 +21,17 @@
     "prng_seed": "random.Random",
 }
 
-def fetch(url):
+def fetch(url, q):
+    # HTMX fix (2026-10-06): HX-Current-URL is the header that flips
+    # /api/htmx/search/ from 204 No Content to 200 + rows. Verified live
+    # (see data/2026-10-06-wikimedia-rogue-agents/htmx-fix/workers/verification/VERIFICATION.md);
+    # the prior HX-Request-only set did NOT fix it. Mirrors the skill pattern
+    # (~/workspace/skills/urlquery/bin/uq_htmx_curl.py).
+    current_url = "https://urlquery.net/search?q=" + urllib.parse.quote(q)
     req = urllib.request.Request(url, headers={
         "User-Agent": "Mozilla/5.0 (research; read-only)",
         "HX-Request": "true",
+        "HX-Current-URL": current_url,
         "Referer": "https://urlquery.net/search",
     })
     try:
@@ -39,13 +46,13 @@
     summary = {}
     for name, q in QUERIES.items():
         url = "https://urlquery.net/api/htmx/search/?q=" + urllib.parse.quote(q) + "&limit=50&offset=0"
-        status, body = fetch(url)
+        status, body = fetch(url, q)
         # extract report UUIDs from the htmx HTML
         import re
         uuids = sorted(set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", body)))
         summary[name] = {"query": q, "http_status": status, "html_bytes": len(body), "uuids": uuids, "count": len(uuids)}
         print(f"{name}: status={status} uuids={len(uuids)}")
-        time.sleep(2)
+        time.sleep(5)
     with open(os.path.join(OUT, "search_summary.json"), "w") as f:
         json.dump(summary, f, indent=2)
 
```

## Net change

- Script 1 (BROKEN, sent no HX headers): now sends `HX-Current-URL` = the `/search` URL with the query.
- Script 2 (UNKNOWN, sent `HX-Request` + `Referer`): now additionally sends `HX-Current-URL`.
- Both: `HX-Current-URL` value is built as `https://urlquery.net/search?q=<quote(query)>`,
  exactly mirroring the skill's `uq_htmx_curl.py`.
- Both: inter-request sleep 2s → 5s.
