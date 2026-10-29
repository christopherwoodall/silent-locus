#!/usr/bin/env python3
"""Build the site-captures Factum ingest bundle.

Reads data/lanes/site-captures/raw/<site>/surface_capture.json (+ body files),
emits bundle.site-captures.json: 1 source + 1 run + 33 web.capture observations
+ 1 summary claim. All tag values are strings. No values are invented: times
come from capture retrieved_at_utc, statuses/errors/sha256/bytes are verbatim.
"""
import json, os, hashlib, re, sys

LANE = "site-captures"
ACTOR = "agent:lane-ingest/site-captures"
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# agent-surfaces reachability.check probes of the same URL (status-only, no bytes)
OVERLAP = {
    "https://agentgateway.pythonanywhere.com/llms.txt":
        ("observation_1cf6e0041a364a0180ae00d3639dc5ca", "200", "2026-09-28T03:30:52.010985Z"),
    "https://agentsboard.org/llms.txt":
        ("observation_0668a5d48f4845fc96897585390c95ee", "200", "2026-09-28T03:25:36.881510Z"),
    "https://aiforum.grok.me/llms.txt":
        ("observation_5143d7842e0144a5a2b449cdd69d7191", "200", "2026-09-28T03:32:53.681742Z"),
    "https://bitily.in/llms.txt":
        ("observation_822de1aa94fd445dbe83bafd8c14f212", "200", "2026-09-28T03:42:30.781710Z"),
    "https://facehuggers.chain-of-thought.org/llms.txt":
        ("observation_a0da9ae1d612468194bad3e6005e343e", "404", "2026-09-28T03:23:06.929656Z"),
    "https://jotspot.io/llms.txt":
        ("observation_319e48323ad64f3fbc1d910e64586367", "404", "2026-09-28T03:34:32.378282Z"),
    "https://messageboardforaiagents.com/llms.txt":
        ("observation_52af8ef7420344cfa9a2ae14e79a2b13", "404", "2026-09-28T03:28:45.764722Z"),
    "https://nervesocket.com/llms.txt":
        ("observation_c3718654c1b34399a937143e4cb078b2", "200", "2026-09-28T03:41:46.013910Z"),
    "https://nullyard.net/llms.txt":
        ("observation_f0ba717c31374346ba2fe6504df5d9cc", "200", "2026-09-28T03:36:06.405684Z"),
    "https://pastebin.tarcseh.me/llms.txt":
        ("observation_19d34b2a39804c6aaae151adf3ab9848", "404", "2026-09-28T03:40:18.045568Z"),
    "https://she-llac.com/CROSS_SITE_CONNECTIONS.md":
        ("observation_b93fb34702e14311bbfef1525c506acb", "200", "2026-09-28T03:39:49.754499Z"),
}

def norm_ts(ts):
    # retrieved_at_utc carries +00:00; corpus convention is Z suffix
    return ts.replace("+00:00", "Z")

def slug(d):
    return re.sub(r"[^a-z0-9]+", "-", d.lower()).strip("-")

sites = sorted(os.listdir(RAW))
assert len(sites) == 33, f"expected 33 sites, found {len(sites)}"

captures = []
for d in sites:
    j = json.load(open(os.path.join(RAW, d, "surface_capture.json")))
    bpath = os.path.join(RAW, d, "surface_capture_body.txt")
    body = open(bpath, "rb").read() if os.path.exists(bpath) else None
    captures.append((d, j, body))

times = sorted(norm_ts(j["retrieved_at_utc"]) for _, j, _ in captures)

records = []

# 1. source
records.append({
    "ref": "src", "kind": "source",
    "body": {
        "source_type": "capture-set",
        "locator": "data/lanes/site-captures/",
        "title": "33-site agent-surface capture set (llms.txt sweep, 2026-09-28)",
        "platform": "33 agent-oriented web surfaces (message boards, agent communities, relays)",
    },
    "tags": {
        "lane": LANE,
        "grade": "OBSERVED",
        "legacy_path": "evidence/site-captures/",
        "capture_count": "33",
    },
})

# 2. run (the original capture sweep; bounds derived from capture metadata)
records.append({
    "ref": "run1", "kind": "run",
    "body": {
        "run_kind": "agent_surface_capture_sweep",
        "started": times[0],
        "ended": times[-1],
        "coverage": {
            "description": "33 agent-oriented web surfaces probed for agent-facing documents "
                           "(llms.txt, plus thecolony.ai/for-agents and "
                           "she-llac.com/CROSS_SITE_CONNECTIONS.md); 24 returned HTTP 200 with "
                           "retrievable bytes, 9 failed (7 HTTP 404, 2 connection failures)",
            "scanned": 33, "total": 33, "complete": True,
        },
        "params": {
            "source_dir": "evidence/site-captures/",
            "note": "Ingest of a pre-existing capture set; the collector tool is not named "
                    "in the capture metadata, so no tool claim is made.",
        },
    },
    "tags": {
        "lane": LANE,
        "grade": "OBSERVED",
        "timestamp_source": "min/max of capture retrieved_at_utc (collector clock)",
    },
})

# 3. web.capture observations
ok = 0
failed_hosts = []
for d, j, body in captures:
    url = j["url"]
    observed_at = norm_ts(j["retrieved_at_utc"])
    data = {"requested_url": url, "capture_kind": "http"}
    tags = {"lane": LANE, "grade": "OBSERVED",
            "capture_json": f"data/lanes/{LANE}/raw/{d}/surface_capture.json"}
    if j.get("http_status"):
        data["http_status"] = int(j["http_status"])
    if body is not None:
        h = hashlib.sha256(body).hexdigest()
        wire_ok = (h == j["sha256"])
        if not wire_ok:
            # agent-board.juleskreuer.eu: on-disk body is LF-normalized; the
            # capture hash describes CRLF wire bytes. Recover and verify.
            crlf = body.replace(b"\n", b"\r\n").replace(b"\r\r\n", b"\r\n")
            assert hashlib.sha256(crlf).hexdigest() == j["sha256"], f"unrecoverable bytes for {d}"
            assert len(crlf) == j["bytes"], f"size mismatch for {d}"
            tags["raw_file_note"] = (
                "on-disk body is LF-normalized (%d bytes); LF->CRLF reproduces the capture "
                "sha256 %s and %d wire bytes exactly; wire bytes fully recoverable"
                % (len(body), j["sha256"], j["bytes"]))
        tags["sha256"] = j["sha256"]
        tags["bytes"] = str(j["bytes"])
        tags["cached_path"] = f"data/lanes/{LANE}/raw/{d}/surface_capture_body.txt"
        ok += 1
    else:
        tags["error"] = j["error"]
        failed_hosts.append(d)
    if url in OVERLAP:
        rid, st, at = OVERLAP[url]
        note = (f"agent-surfaces lane reachability.check {rid} probed this URL {at} -> {st} "
                "(status only, no bytes preserved); this web.capture is a distinct acquisition "
                "with preserved bytes, kept per keep-all policy")
        if url in ("https://aiforum.grok.me/llms.txt", "https://bitily.in/llms.txt"):
            note += ("; STATUS DISCREPANCY: agent-surfaces saw 200 minutes apart while this "
                     "capture failed (%s) - host was flaky during the sweep window" % j["error"])
        tags["overlap.corpus"] = note
    if url == "https://thecolony.ai/for-agents":
        tags["overlap.corpus"] = (
            "observation_cfd2ce71c2ed4039885c806d331e681f (lane 2026-09-04-thecolony-ai) "
            "captured this URL 2026-09-28T03:18:02Z with different wire bytes (sha256 "
            "7a30465c78572cfd9fc16b6da4342e356be41dbfa5937bcb95dcd66e91ca5b89); this is a "
            "distinct later sighting (2026-09-28T03:20:21Z, sha256 "
            "05287d7423d01af4877a39f47499cff56d08ddb0f07f4a9a20b0c5ea3640b4ac), "
            "kept per keep-all policy")
    records.append({
        "ref": "cap-" + slug(d),
        "kind": "observation",
        "body": {
            "type": "web.capture",
            "source": "@src",
            "run": "@run1",
            "observed_at": observed_at,
            "time_basis": "collector_clock",
            "files": [],
            "data_schema": "urn:factum:web:web-capture:1",
            "data": data,
        },
        "tags": tags,
    })

# 4. summary claim on the run
cap_refs = ["@cap-" + slug(d) for d, _, _ in captures]
records.append({
    "ref": "claim1", "kind": "claim",
    "body": {
        "subject": "@run1",
        "property": "sweep_outcome",
        "value": {
            "probed": 33,
            "http_200_with_bytes": ok,
            "failed": len(failed_hosts),
            "failed_breakdown": {
                "http_404": sum(1 for _, j, _ in captures if j.get("error", "").startswith("HTTP Error 404")),
                "connection_failure": sum(1 for _, j, _ in captures
                                         if "error" in j and not j["error"].startswith("HTTP Error 404")),
            },
            "failed_hosts": sorted(failed_hosts),
            "note": "24 of 33 agent-oriented surfaces served a retrievable agent-facing document "
                    "(llms.txt or equivalent) at capture time 2026-09-28; 11 of the 33 URLs were "
                    "also probed status-only by the agent-surfaces lane (see overlap.corpus tags).",
        },
        "basis": "OBSERVED",
        "cites": cap_refs,
    },
    "tags": {"lane": LANE, "grade": "OBSERVED"},
})

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": "site-captures/2026-10-10/ingest-1",
    "records": records,
}

# every tag value must be a string
for r in records:
    for k, v in r["tags"].items():
        assert isinstance(v, str), f"non-string tag {k}={v!r} in {r['ref']}"

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bundle.site-captures.json")
json.dump(bundle, open(out, "w"), indent=1, sort_keys=True)
print(f"wrote {out}: {len(records)} records "
      f"({ok} captures w/ bytes, {len(failed_hosts)} failed, 1 source, 1 run, 1 claim)")
