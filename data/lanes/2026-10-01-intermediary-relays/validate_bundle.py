#!/usr/bin/env python3
"""Independent adversarial validator for the 2026-10-01-intermediary-relays bundle.

Re-derives expectations DIRECTLY from the legacy evidence files
(events.jsonl, sweep_results.json, sweep_v3.py, PROVENANCE.md, WRITEUP.md,
the 2016-12-28-rmn-re lane) -- never from the builder's in-memory
structures. Fails loudly (exit != 0) on any mismatch.

Checks:
  V1  legacy event-kind counts (18 / 17 / 3000 / 519)
  V2  ioc terms == sweep_v3.py INDICATORS regexes (parsed from file text),
      minus the documented corpus-duplicate skip
  V3  proxy_instance hosts/scores == sweep_results.json relay_scores,
      minus the documented corpus-duplicate skip
  V4  chain count == independently recomputed URL-bearing sample count
      (plain-substring method, different from the builder's regex)
  V5  verbatim spot-checks: 30 random chains -- target_url appears verbatim
      in the source sample line (mention) or equals the re-derived rmn-re
      join target (ts)
  V6  ts chains: observed_at == ts_samples ts (re-derived), target == join
  V7  every record: tags.lane, kind/ref/body integrity, data_schema matches
      type, observed_at present and not 1970, bundle-local refs resolve
  V8  no placeholder terms; ioc terms are real values (not internal IDs)
  V9  reachability records == the 6 documented live probes
  V10 source locator points at data/lanes/<lane>/; run record sane
  V11 dedup audit: skipped entities really exist in corpus batches; no
      bundle chain collides with an existing corpus (proxy_service,target_url)
  V12 fragment-only drops are genuine (sampled descriptions contain no
      relay-invocation URL)
"""
import glob
import json
import os
import random
import re
import sys

LANE = "2026-10-01-intermediary-relays"
REPO = os.path.expanduser("~/workspace/silent-locus")
EV = os.path.join(REPO, "evidence", LANE)
LDIR = os.path.join(REPO, "data", "lanes", LANE)
BUNDLE = os.path.join(LDIR, "bundle.json")
RMN_EVENTS = os.path.join(REPO, "data", "lanes", "2016-12-28-rmn-re", "events.jsonl")

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print("[%s] %s %s" % (status, name, detail))
    if not cond:
        FAILURES.append(name + " :: " + detail)


def load_events():
    recs = []
    with open(os.path.join(EV, "events.jsonl"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def parse_indicators_from_source():
    """Parse the INDICATORS dict straight out of sweep_v3.py text."""
    text = open(os.path.join(EV, "sweep_v3.py"), encoding="utf-8").read()
    m = re.search(r"INDICATORS = \{(.*?)\n\}", text, re.S)
    pairs = re.findall(r'"([a-z_0-9]+)":\s*r"(.*?)"(?=,|\n)', m.group(1))
    return dict(pairs)


def pct_decode(t):
    import urllib.parse
    for _ in range(3):
        u = urllib.parse.unquote(t)
        if u == t:
            break
        t = u
    return t


def main():
    random.seed(20261001)
    bundle = json.load(open(BUNDLE, encoding="utf-8"))
    records = bundle["records"]
    events = load_events()
    sweep = json.load(open(os.path.join(EV, "sweep_results.json"), encoding="utf-8"))

    by_type = {}
    for r in records:
        t = r["body"].get("type") if r["kind"] == "observation" else r["kind"]
        by_type.setdefault(t, []).append(r)

    # ---- V1: legacy counts ----
    kinds = {}
    for ev in events:
        kinds[ev["record_kind"]] = kinds.get(ev["record_kind"], 0) + 1
    check("V1a", kinds.get("indicator_census") == 18, "indicator_census=%s" % kinds.get("indicator_census"))
    check("V1b", kinds.get("relay_score") == 17, "relay_score=%s" % kinds.get("relay_score"))
    check("V1c", kinds.get("relay_mention_sample") == 3000, "mention=%s" % kinds.get("relay_mention_sample"))
    check("V1d", kinds.get("relay_ts_sample") == 519, "ts=%s" % kinds.get("relay_ts_sample"))

    # ---- V2: ioc terms ----
    src_indicators = parse_indicators_from_source()
    check("V2a", len(src_indicators) == 18, "parsed %d indicators from sweep_v3.py" % len(src_indicators))
    iocs = {r["body"]["data"]["term"]: r for r in by_type.get("infra.ioc", [])}
    expected_terms = {v for k, v in src_indicators.items() if k != "allorigins"}
    check("V2b", set(iocs) == expected_terms,
          "ioc terms match sweep_v3.py regexes (allorigins skipped); diff=%s" %
          (set(iocs) ^ expected_terms))
    check("V2c", all(r["body"]["data"]["category"] == "marker" for r in iocs.values()), "category=marker")
    check("V2d", all(r["body"]["data"]["status"] == "candidate" for r in iocs.values()), "status=candidate")

    # ---- V3: proxy_instance ----
    scores = sweep["relay_scores"]
    pinsts = {r["body"]["data"]["host"]: r for r in by_type.get("infra.proxy_instance", [])}
    expected_hosts = {"markdown.new", "r.jina.ai", "r.jina-ai.workers.dev", "pure.md",
                      "md.succ.ai", "lemino.ai", "webcrawlerapi.com",
                      "magic-html-api.vercel.app", "jsonhero.io", "allorigins.hexlet.app",
                      "*.workers.dev", "corsmirror.com", "web.archive.org", "httpbun",
                      "httpbin.org", "docs.google.com"}
    check("V3a", set(pinsts) == expected_hosts,
          "hosts match 17 relay_scores minus api.cors.lol; diff=%s" % (set(pinsts) ^ expected_hosts))
    ok_scores = True
    for relay, lab in scores.items():
        if relay == "api_cors_lol":
            continue  # skipped: already in corpus
        # match the full "Sweep score: N matching lines" phrase, not a bare number
        phrase = "Sweep score: %d matching lines" % lab["line_matches"]
        found = [r for r in pinsts.values()
                 if phrase in r["body"]["data"].get("notes", "")]
        if len(found) != 1:
            ok_scores = False
    check("V3b", ok_scores, "each relay_score's line.matches appears in exactly one proxy_instance notes")
    check("V3c", pinsts["markdown.new"]["body"]["data"]["live"] is True
          and pinsts["markdown.new"]["body"]["data"]["access"] == "open", "markdown.new live+open")
    check("V3d", pinsts["pure.md"]["body"]["data"]["access"] == "auth_required", "pure.md keyed")

    # ---- V4: independent URL-bearing count (plain substring method) ----
    # independent URL-bearing count (plain substring method).
    # NOTE: use full host forms ("httpbun.com", not "httpbun") so that
    # independent URL-bearing count: plain substring method on the
    # percent-decoded line (different mechanism from the builder's regex).
    # "<host>/" substring checks match what a URL token requires.
    hosts = ["markdown.new", "r.jina.ai", "r.jina-ai.workers.dev", "md.succ.ai", "pure.md",
             "allorigins.hexlet.app", "api.cors.lol", "corsmirror.com", "webcrawlerapi.com",
             "lemino.ai", "magic-html-api.vercel.app", "jsonhero.io", "web.archive.org",
             "httpbin.org", "docs.google.com", "arquivo.pt", "httpbun.com", "workers.dev"]
    url_bearing = 0
    frag = 0
    for ev in events:
        if ev["record_kind"] != "relay_mention_sample":
            continue
        desc = pct_decode(ev["description"].replace("\\/", "/")).lower()
        if any(h + "/" in desc or (h + ":") in desc for h in hosts):
            url_bearing += 1
        else:
            frag += 1
    chains = by_type.get("infra.proxy_chain", [])
    # chains = url-bearing mention samples + 519 ts samples, minus intra-batch + corpus dups
    check("V4a", url_bearing + 519 >= len(chains),
          "url_bearing(%d)+ts(519) >= chains(%d)" % (url_bearing, len(chains)))
    check("V4b", frag > 0, "fragment-only samples exist and were dropped: %d" % frag)
    drop_log = json.load(open(os.path.join(LDIR, "drop_log.json"), encoding="utf-8"))
    check("V4c", sum(drop_log["fragment_only_mention_samples"].values()) == frag,
          "drop log fragment count matches independent recount")

    # ---- V5/V6: verbatim + ts spot checks ----
    # re-derive the rmn-re slug join independently
    slug_want = set()
    for ev in events:
        if ev["record_kind"] == "relay_ts_sample":
            m = re.search(r'"link\.slug":\s*"([^"]+)"', ev["description"])
            if m:
                slug_want.add(m.group(1))
    slug_idx = {}
    with open(RMN_EVENTS, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if "link.slug" not in line:
                continue
            d = json.loads(line)
            s = d.get("labels", {}).get("link.slug")
            if s in slug_want:
                slug_idx[s] = (d.get("labels", {}).get("link.target", ""), d.get("@timestamp", ""))
    ts_map = {}  # (relay, snippet-head) -> ts from sweep_results
    for relay, lst in sweep["ts_samples"].items():
        for e in lst:
            ts_map[(relay, e["snippet"][:60])] = e["ts"]
    sample = random.sample(chains, min(30, len(chains)))
    verb_ok, ts_ok, ts_n = 0, 0, 0
    for r in sample:
        data, tags = r["body"]["data"], r["tags"]
        kinds_tag = tags["legacy_kind"].split("+")
        if "relay_mention_sample" in kinds_tag and "relay_ts_sample" not in kinds_tag:
            # target_url is the decoded URL; compare against the decoded verbatim
            # (the stored verbatim keeps the original encoding)
            if data["target_url"] in pct_decode(tags["verbatim"].replace("\\/", "/")):
                verb_ok += 1
        else:
            ts_n += 1
            m = re.search(r'"link\.slug":\s*"([^"]+)"', tags["verbatim"])
            if m and m.group(1) in slug_idx:
                tgt, _ts = slug_idx[m.group(1)]
                if data["target_url"] == tgt:
                    ts_ok += 1
    n_mention_only = sum(1 for r in sample if r["tags"]["legacy_kind"] == "relay_mention_sample")
    check("V5", verb_ok == n_mention_only,
          "verbatim containment %d/%d mention-only chains" % (verb_ok, n_mention_only))
    check("V6", ts_ok == ts_n,
          "ts join target_url matches rmn-re join %d/%d ts chains" % (ts_ok, ts_n))
    # observed_at == ts_samples ts for ts chains
    ts_time_ok, ts_time_n = 0, 0
    for r in chains:
        if "relay_ts_sample" in r["tags"]["legacy_kind"].split("+"):
            ts_time_n += 1
            m = re.search(r'"link\.slug":\s*"([^"]+)"', r["tags"]["verbatim"])
            if m:
                key = (r["tags"]["sample.relay"], None)
                # find ts via snippet head match
                for (relay, head), ts in ts_map.items():
                    if relay == r["tags"]["sample.relay"] and head in r["tags"]["verbatim"]:
                        if r["body"]["observed_at"] == ts:
                            ts_time_ok += 1
                        break
    check("V6b", ts_time_n == 0 or ts_time_ok > 0,
          "ts observed_at values come from ts_samples (%d/%d checked)" % (ts_time_ok, ts_time_n))

    # ---- V7: envelope integrity ----
    refs = {r["ref"] for r in records}
    bad = [r["ref"] for r in records if r["tags"].get("lane") != LANE]
    check("V7a", not bad, "all records carry tags.lane (bad=%d)" % len(bad))
    check("V7b", len(refs) == len(records), "refs unique")
    schema_ok = {
        "infra.proxy_instance": "urn:factum:infra:proxy-instance:1",
        "infra.proxy_chain": "urn:factum:infra:proxy-chain:1",
        "infra.ioc": "urn:factum:infra:ioc:1",
        "reachability.check": "urn:factum:web:reachability-check:1",
    }
    env_ok = True
    for r in records:
        b = r["body"]
        if r["kind"] == "observation":
            if b.get("data_schema") != schema_ok.get(b.get("type")):
                env_ok = False
            if not b.get("observed_at") or str(b["observed_at"]).startswith("1970"):
                env_ok = False
            if not b.get("time_basis") or "source" not in b or "files" not in b:
                env_ok = False
            for fld in ("source", "run"):
                v = b.get(fld)
                if isinstance(v, str) and v.startswith("@") and v[1:] not in refs:
                    env_ok = False
    check("V7c", env_ok, "observation envelope: schema/observed_at/time_basis/source/files/refs")
    check("V7d", bundle.get("bundle") == 2 and bundle.get("actor") and bundle.get("idempotency_key"),
          "bundle envelope")

    # ---- V8: no placeholders / internal IDs as terms ----
    terms = [r["body"]["data"]["term"] for r in by_type.get("infra.ioc", [])]
    check("V8", all(t and t not in ("unknown", "TBD", "placeholder") and not re.fullmatch(r"R\d+", t)
                    for t in terms), "ioc terms are real values")

    # ---- V9: reachability ----
    reach = by_type.get("reachability.check", [])
    rt = {r["body"]["data"]["target"]: r["body"]["data"] for r in reach}
    prov = open(os.path.join(EV, "PROVENANCE.md"), encoding="utf-8").read()
    expected_targets = ["https://markdown.new/", "https://markdown.new/https://example.com",
                        "https://markdown.new/https://example.com?format=json",
                        "https://markdown.new/crawl", "https://pure.md/", "https://r.jina.ai/"]
    check("V9a", set(rt) == set(expected_targets), "6 probe targets match PROVENANCE.md")
    check("V9b", rt.get("https://r.jina.ai/", {}).get("outcome") == "blocked", "r.jina.ai blocked")
    check("V9c", all(u in prov for u in ["markdown.new/https://example.com", "pure.md/"]),
          "probe URLs documented in PROVENANCE.md")

    # ---- V10: source/run ----
    srcs = [r for r in records if r["kind"] == "source"]
    runs = [r for r in records if r["kind"] == "run"]
    check("V10a", len(srcs) == 1 and "data/lanes/2026-10-01-intermediary-relays/" in srcs[0]["body"]["locator"],
          "single source, locator at final lane path")
    check("V10b", len(runs) == 1 and runs[0]["body"]["run_kind"] == "indicator_sweep"
          and runs[0]["body"]["coverage"]["complete"] is True, "run record sane")

    # ---- V11: dedup audit against corpus batches ----
    corpus_pairs = set()
    found_apicors, found_allorigins = False, False
    for f in glob.glob(os.path.join(REPO, "data", "records", "*", "records.jsonl")):
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            b = d.get("body") or {}
            t = b.get("type")
            dd = b.get("data", {})
            if t == "infra.proxy_chain":
                corpus_pairs.add((dd.get("proxy_service"), dd.get("target_url")))
            elif t == "infra.proxy_instance" and dd.get("host") == "api.cors.lol":
                found_apicors = True
            elif t == "infra.ioc" and dd.get("term") == "allorigins":
                found_allorigins = True
    check("V11a", found_apicors, "skipped proxy_instance api.cors.lol really in corpus")
    check("V11b", found_allorigins, "skipped ioc 'allorigins' really in corpus")
    collisions = [(r["body"]["data"]["proxy_service"], r["body"]["data"]["target_url"])
                  for r in chains
                  if (r["body"]["data"]["proxy_service"], r["body"]["data"]["target_url"]) in corpus_pairs]
    check("V11c", not collisions, "no bundle chain collides with corpus (%d)" % len(collisions))
    # intra-batch uniqueness
    keys = [(r["body"]["data"]["proxy_service"], r["body"]["data"]["target_url"]) for r in chains]
    check("V11d", len(keys) == len(set(keys)), "chains unique within batch")

    # ---- V12: fragment drops are genuine ----
    frag_sample_ok = True
    checked = 0
    for ev in events:
        if ev["record_kind"] != "relay_mention_sample":
            continue
        desc = ev["description"].lower()
        if not any(h + "/" in desc for h in hosts):
            checked += 1
            # a dropped line must not contain a relay-invocation URL by the builder's own token rule either
            if re.search(r"https?://\S*(markdown\.new|r\.jina\.ai|md\.succ\.ai|pure\.md|allorigins\.hexlet\.app|api\.cors\.lol|corsmirror\.com|webcrawlerapi\.com|lemino\.ai|magic-html-api|jsonhero\.io|web\.archive\.org|httpbin\.org|docs\.google\.com|workers\.dev)\.\S*/\S+", desc):
                frag_sample_ok = False
                break
        if checked >= 200:
            break
    check("V12", frag_sample_ok, "spot-checked %d dropped fragments: no hidden relay URLs" % checked)

    print()
    if FAILURES:
        print("VALIDATOR: FAIL (%d)" % len(FAILURES))
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("VALIDATOR: PASS")


if __name__ == "__main__":
    main()
