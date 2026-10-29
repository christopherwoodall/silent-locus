#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-10-01-intermediary-relays.

Reads the legacy lane evidence (evidence/2026-10-01-intermediary-relays/)
and emits a Factum bundle v2 JSON:

  - 1 source record  (sweep outputs + PROVENANCE.md + WRITEUP.md)
  - 1 run record     (sweep_v3.py indicator sweep)
  - 16 infra.proxy_instance  (relay_score -> relay entity; api.cors.lol skipped:
                              already in corpus from proxy-fresh-blood)
  - 17 infra.ioc             (indicator_census -> marker regex; 'allorigins'
                              skipped: already in corpus from
                              2026-09-05-termina-digital)
  - N infra.proxy_chain      (relay_mention_sample + relay_ts_sample lines that
                              carry a concrete relay-invocation URL; deduped
                              within batch on (proxy_service, target_url);
                              ts samples joined to full URLs via the
                              2016-12-28-rmn-re shortener_link records)
  - 6 reachability.check     (live probes documented in PROVENANCE.md/WRITEUP.md)

Fragment-only mention lines (no invocation URL, e.g. '"wrapper":
"markdown.new"') are NOT turned into structured records: they carry no
structured information beyond the relay_score aggregates. They remain in the
preserved raw events.jsonl; the drop is logged to drop_log.json.

No edges are created during ingest (standing rule). Every record carries
tags.lane = "2026-10-01-intermediary-relays".
"""
import json
import os
import re
import sys

LANE = "2026-10-01-intermediary-relays"
ACTOR = "agent:lane-ingest/" + LANE
IDEMPOTENCY_KEY = "lane-ingest-" + LANE + "-v1"
REPO = os.path.expanduser("~/workspace/silent-locus")
EV = os.path.join(REPO, "evidence", LANE)
RMN_EVENTS = os.path.join(REPO, "data", "lanes", "2016-12-28-rmn-re", "events.jsonl")
OUT_BUNDLE = os.path.join(REPO, "data", "lanes", LANE, "bundle.raw.json")
OUT_DROPLOG = os.path.join(REPO, "data", "lanes", LANE, "drop_log.json")
SWEEP_DATE = "2026-10-01T00:00:00Z"  # sweep execution date (documented)

# --- existing corpus pairs (dedup): (proxy_service, target_url) already ingested ---
EXISTING_CHAINS = set()
for _rec_f in __import__("glob").glob(os.path.join(REPO, "data", "records", "*", "records.jsonl")):
    for _ln in open(_rec_f, encoding="utf-8", errors="replace"):
        try:
            _d = json.loads(_ln)
        except Exception:
            continue
        _b = _d.get("body") or {}
        if _b.get("type") == "infra.proxy_chain":
            _dd = _b.get("data", {})
            EXISTING_CHAINS.add((_dd.get("proxy_service"), _dd.get("target_url")))

# --- relay entity table (from WRITEUP.md; keyless/live status live-verified 2026-10-01) ---
# host: Factum infra.proxy_instance host value. None => skip (already in corpus).
RELAYS = {
    "markdown.new": dict(host="markdown.new",
        shape="https://markdown.new/<target-url> (?format=json, ?method=auto|ai|browser, ?retain_images=true; POST {\"url\": ...}; crawl via markdown.new/crawl/<url>)",
        access="open", live=True, last_checked="2026-10-01",
        agent_use_grade="CONFIRMED",
        grade_note="CONFIRMED agent-use, multiple vantages: 11 urlquery reports 2026-05-11..2026-09-24 (incl. 5 scans of tinyurl.com/282hbk6j in 22s on 2026-05-11); 776 occurrences in collusion-wiki records.jsonl; Transluce 2026-09-30 OMB MAX.gov incident (16 ?uniqN versions in 27s, JSON extraction)."),
    "r.jina.ai": dict(host="r.jina.ai",
        shape="https://r.jina.ai/<target-url>",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="CONFIRMED (prior lanes)",
        grade_note="CONFIRMED in prior lanes; live keyless status NOT re-verified this lane (sandbox fetch policy blocked the probe; do not retry). 44 inner domains via jina laundering in wiki corpus (nsi-venue-sweep)."),
    "jina_workers": dict(host="r.jina-ai.workers.dev",
        shape="https://r.jina-ai.workers.dev/<target-url> (jina reader redeployed on workers.dev, pointed at sec.gov)",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed (low volume)",
        grade_note="5 docs in wiki corpus; 20 line matches, 2 distinct co-occurring indicators."),
    "pure.md": dict(host="pure.md",
        shape="https://pure.md/<target-url> (uppercase-tolerant)",
        access="auth_required", live=True, last_checked="2026-10-01",
        agent_use_grade="CONFIRMED (keyed)",
        grade_note="CONFIRMED agent-use; keyed not keyless: signup required, Starter $0/mo pay-as-you-go with $1 free credit, rate-limited without subscription (live homepage read 2026-10-01). 753 hits / 723 distinct URLs in proxy-primitives lane, first-seen 2026-05-26..2026-06-20; 152 hits wrap another proxy. Markets antibot evasion (browser fingerprints, per-request egress IP rotation)."),
    "md.succ.ai": dict(host="md.succ.ai",
        shape="https://md.succ.ai/<url> (+/extract, /batch, /async, /job/{id})",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="CONFIRMED",
        grade_note="CONFIRMED agent-use: 483 wiki agents reference it, 1763 occurrences (md.succ.ai/https://www.investor.gov/files/county.json shape), 16 zzmasscounty* shortener slugs with ?dummyagent=<12-digit> nonces; not live-probed this lane (keylessness deployment-dependent; self-hostable open-source)."),
    "lemino_url2md": dict(host="lemino.ai",
        shape="lemino.ai/api/url2md/<url>",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed (low volume)",
        grade_note="1 wiki ref (lemino.ai/api/url2md/https%3A%2F%2Fmarkdown.new%2Fwww.investor.gov%2Ffiles%2Fcounty.json); stacked with markdown.new."),
    "webcrawlerapi": dict(host="webcrawlerapi.com",
        shape="webcrawlerapi.com/api/playground/content?url=<url>",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed (low volume)",
        grade_note="1 wiki ref; stacked on agent link-bridge pages."),
    "magic_html_api": dict(host="magic-html-api.vercel.app",
        shape="magic-html-api.vercel.app/api/extract?url=<url>",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed (low volume)",
        grade_note="Live scan sample: .../api/extract?url=https://r.jina.ai/https://www.sec.gov/files/county.json (stacked with r.jina.ai)."),
    "jsonhero": dict(host="jsonhero.io",
        shape="jsonhero.io shared doc IDs (JSON viewer used to share JSON docs)",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed (low volume)",
        grade_note="17-18 shared doc IDs in wiki corpus; dedicated lane data/2022-03-01-jsonhero."),
    "allorigins_relay": dict(host="allorigins.hexlet.app",
        shape="https://allorigins.hexlet.app/<target-url> (stacks: allorigins -> markdown.new -> r.jina.ai -> sec.gov)",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="Live urlquery incidents laundering sec.gov/investor.gov county.json with ?x=<nonce>."),
    "cors_workers": dict(host="*.workers.dev",
        shape="https://<name>.workers.dev/<target-url> (CORS-proxy family)",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="7 known hostnames per WRITEUP: cors.bwa, cors.hypnguyen, cors-get-proxy.sirjosh, cloudflare-cors-anywhere.hanpengchen, test.cors, cf-cors.findme-19, r.jina-ai. Keyless generic infra, fungible; test.cors.workers.dev served portal.max.gov SF133 (8) + markdown.new (16)."),
    "api_cors_lol": None,  # SKIP: infra.proxy_instance for api.cors.lol already in corpus (proxy-fresh-blood)
    "corsmirror": dict(host="corsmirror.com",
        shape="https://corsmirror.com/<target-url>",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="161 hits / 81 distinct URLs in proxy-primitives lane."),
    "wayback": dict(host="web.archive.org",
        shape="https://web.archive.org/<target-url>",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="Wayback relay mentions in corpus."),
    "httpbun_relay": dict(host="httpbun",
        shape="httpbun (relay/utility host; invocation shape not documented this lane)",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="Caveat: self-match inflates the httpbun relay x httpbun indicator pair."),
    "httpbin_relay": dict(host="httpbin.org",
        shape="https://httpbin.org/... (relay/utility host)",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="Relay/utility host; co-occurs broadly."),
    "gview": dict(host="docs.google.com",
        shape="docs.google.com/gview|viewerng wrapping target URLs",
        access="unknown", live=False, last_checked=None,
        agent_use_grade="observed",
        grade_note="290 hits / 187 distinct in proxy-primitives; wraps bwa (8x) and is wrapped by it (6x)."),
}

# --- indicator regexes: copied from sweep_v3.py INDICATORS (final run) ---
INDICATORS = {
    "zz_label":         r"zz[a-z]{1,4}[0-9]{0,20}|ZZ[A-Z]{2,8}|A000\b",
    "github_remote_cache_zz": r"github-remote-cache/zz",
    "oai_tag":          r"oai[a-z]{0,24}[0-9]{2,20}",
    "epoch_nonce":      r"\b1[67][0-9]{8}(\.[0-9]+)?\b",
    "uniq_nonce":       r"[?&]uniq[0-9]*=",
    "httpbun":          r"httpbun",
    "httpbin":          r"httpbin",
    "allorigins":       r"allorigins",   # SKIP: infra.ioc term 'allorigins' already in corpus (2026-09-05-termina-digital)
    "dagd":             r"da\.gd",
    "tinyurl":          r"tinyurl",
    "go_import":        r"go-import",
    "arquivo_pt":       r"arquivo\.pt",
    "disposable_email": r"mailinator|guerrillamail|tempmail|10minutemail|yopmail|sharklasers|trashmail|getnada|fakeinbox|mohmal",
    "apikey_reuse":     r"api[_-]?key",
    "double_slash":     r"(?<=gov)//|//files/",
    "antibot_suffix":   r"[?&](output|raw|url|format|debug|f)=",
    "direct_ip":        r"https?://[0-9]{1,3}(\.[0-9]{1,3}){3}(:[0-9]+)?",
    "collusion_wiki":   r"collusion\.wiki",
}
SKIP_IOC = {"allorigins": "infra.ioc term 'allorigins' already in corpus (lane 2026-09-05-termina-digital)"}
DOUBLE_SLASH_NOTE = ("rg census blind spot: ripgrep default engine does not support the "
    "lookbehind, so the rg census recorded 0 lines/0 files; the Python pass found "
    "124x //www.sec.gov//files//county.json, 17x //www.sec.gov//files/county.json, "
    "6x //www.investor.gov//files//county.json (verified separately with zgrep).")

# --- chain extraction: relay hosts in URL order ---
# Extraction runs on a percent-decoded copy of the sample line (relay URLs are
# often URL-encoded inside wrapper-service query strings, e.g.
# jqp.vercel.app/api/v0?...&url=https%3A%2F%2Fmd.succ.ai%2F...). The verbatim
# original line is preserved untouched in tags.verbatim by the caller.
import urllib.parse

HOST_PATTERNS = [
    ("markdown.new", r"markdown\.new"),
    ("r.jina.ai", r"r\.jina\.ai"),
    ("r.jina-ai.workers.dev", r"r\.jina-ai\.workers\.dev"),
    ("md.succ.ai", r"md\.succ\.ai"),
    ("pure.md", r"(?<![\w.])pure\.md"),
    ("allorigins.hexlet.app", r"allorigins\.hexlet\.app"),
    ("api.cors.lol", r"api\.cors\.lol"),
    ("corsmirror.com", r"corsmirror\.com"),
    ("webcrawlerapi.com", r"webcrawlerapi\.com"),
    ("lemino.ai", r"lemino\.ai"),
    ("magic-html-api.vercel.app", r"magic-html-api\.vercel\.app"),
    ("jsonhero.io", r"jsonhero\.io"),
    ("web.archive.org", r"web\.archive\.org"),
    ("httpbin.org", r"httpbin\.org"),
    ("docs.google.com", r"docs\.google\.com"),
    ("arquivo.pt", r"arquivo\.pt"),
    ("httpbun", r"httpbun(?:\.com)?"),
]
WORKERS_DEV_RE = re.compile(r"((?:[\w-]{1,64}\.)+workers\.dev)", re.I)
URL_TOKEN_RE = re.compile(r"(?:https?://)?[\w.:@-]+(?:\.[\w-]+)+(?:\:\d+)?/[^\s\"'<>\[\]{}|\\^`]*")
INNER_TS_RE = re.compile(r'"@timestamp":\s*"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)"')
SLUG_RE = re.compile(r'"link\.slug":\s*"([^"]+)"')
TRAILING_STRIP = ".,;:'\""

# matches a relay invocation URL starting AT the relay host, anywhere in text
_RELAY_ALTS = (
    r"markdown\.new|r\.jina\.ai|r\.jina-ai\.workers\.dev|md\.succ\.ai|"
    r"(?<![\w.])pure\.md|allorigins\.hexlet\.app|api\.cors\.lol|corsmirror\.com|"
    r"webcrawlerapi\.com|lemino\.ai|magic-html-api\.vercel\.app|jsonhero\.io|"
    r"web\.archive\.org|httpbin\.org|docs\.google\.com|arquivo\.pt|httpbun(?:\.com)?|"
    r"(?:[\w-]{1,64}\.)+workers\.dev"
)
RELAY_URL_RE = re.compile(
    r"(https?://)?((?:" + _RELAY_ALTS + r"))(?::\d+)?/[^\s\"'<>\[\]{}|\\^`]*", re.I)

# observed hostname -> canonical relay host (matches the proxy_instance hosts)
HOST_CANON = {
    "httpbun.com": "httpbun",
}


def pct_decode(t):
    for _ in range(3):
        u = urllib.parse.unquote(t)
        if u == t:
            break
        t = u
    return t


def find_chain(text):
    """Return (proxy_service, target_url, chain) for the first relay invocation URL.

    Works on a JSON-unescape + percent-decoded copy so relay URLs embedded
    (possibly encoded) in wrapper-service query strings are found at their
    real host. Returns the decoded URL; the caller keeps the original
    verbatim line separately.
    """
    decoded = pct_decode(text.replace("\\/", "/"))
    m = RELAY_URL_RE.search(decoded)
    if not m:
        return None
    url = m.group(0).rstrip(TRAILING_STRIP)
    host = m.group(2).lower()
    host = HOST_CANON.get(host, host)
    chain = []
    for chost, pat in HOST_PATTERNS:
        for hm in re.finditer(pat, url, re.I):
            chain.append((hm.start(), chost))
    wm = WORKERS_DEV_RE.search(url)
    if wm:
        wob = wm.group(1).lower()
        if not any(wob == h.lower() or h.lower().endswith("." + wob) for _, h in chain):
            chain.append((wm.start(1), wob))
    chain.sort()
    ordered = [h for _, h in chain]
    if host not in ordered:
        ordered.insert(0, host)
    # dedup preserving order
    seen = set()
    deduped = [h for h in ordered if not (h in seen or seen.add(h))]
    return host, url, deduped


def load_events():
    recs = []
    with open(os.path.join(EV, "events.jsonl"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def load_sweep():
    with open(os.path.join(EV, "sweep_results.json"), encoding="utf-8") as fh:
        return json.load(fh)


def build_rmn_slug_index(wanted_slugs):
    """One pass over the rmn-re lane events.jsonl -> {slug: (target, timestamp)}."""
    idx = {}
    with open(RMN_EVENTS, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if "link.slug" not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            lab = d.get("labels", {})
            slug = lab.get("link.slug")
            if slug in wanted_slugs:
                idx[slug] = (lab.get("link.target", ""), d.get("@timestamp", ""))
                if len(idx) == len(wanted_slugs):
                    break
    return idx


def main():
    events = load_events()
    sweep = load_sweep()

    records = []
    drop_log = {"fragment_only_mention_samples": {}, "corpus_duplicate_chains": 0,
                "skipped_proxy_instance": {}, "skipped_ioc": {}}

    def tag(extra):
        t = {"lane": LANE}
        for k, v in extra.items():
            if v is not None:
                t[k] = v
        return t

    # ---- 1. source record ----
    records.append({
        "kind": "source", "ref": "src-sweep",
        "body": {
            "locator": ("repo:data/lanes/2026-10-01-intermediary-relays/ "
                        "(sweep_v3.py outputs: sweep_results.json, sweep_samples.jsonl, "
                        "sweep_summary.txt, sweep_stderr.txt; build_events.py, "
                        "sweep_indicators.py, sweep_v2.py; PROVENANCE.md, WRITEUP.md, SHA256SUMS)"),
            "source_type": "submitted",
        },
        "tags": tag({"collection": "2026-10-01",
                     "provenance": "data/lanes/2026-10-01-intermediary-relays/PROVENANCE.md"}),
    })

    # ---- 2. run record ----
    records.append({
        "kind": "run", "ref": "run-sweep",
        "body": {
            "run_kind": "indicator_sweep",
            "tool": "sweep_v3.py",
            "params": {
                "indicators": sorted(INDICATORS.keys()),
                "relays": sorted(sweep["relay_scores"].keys()),
                "corpus_root": "data/",
                "exclusions": ["sibling data/2026-10-01-* lanes", "*/frames/* animation dirs",
                               "files > 200MB"],
                "line_truncation": "lines truncated to 20KB before regex (full lines remain in sources)",
                "stage1": "ripgrep per-indicator matching-line/file census over text files (-z for gz)",
                "stage2": "Python co-occurrence scoring on relay-mentioning lines only",
            },
            "coverage": {
                "description": ("ripgrep indicator census + Python relay co-occurrence scoring over "
                                "on-disk text corpora under data/ (sibling 2026-10-01 lanes excluded)"),
                "scanned": 43688,
                "complete": True,
            },
        },
        "tags": tag({"grade": "OBSERVED"}),
    })

    # ---- 3. proxy_instance records (relay_score) ----
    for ev in events:
        if ev["record_kind"] != "relay_score":
            continue
        lab = ev["labels"]
        relay = lab["relay"]
        if RELAYS.get(relay) is None:
            drop_log["skipped_proxy_instance"][relay] = (
                "infra.proxy_instance already in corpus (lane proxy-fresh-blood)")
            continue
        r = RELAYS[relay]
        data = {"host": r["host"], "invocation_shape": r["shape"],
                "access": r["access"], "live": r["live"]}
        if r["last_checked"]:
            data["last_checked"] = r["last_checked"]
        data["notes"] = (
            "Sweep score: {lm} matching lines, {di} distinct co-occurring indicators, "
            "{tc} total co-occurrence hits. Co-occurring indicators: {inds}. "
            "Agent-use grade ({g}): {gn}".format(
                lm=lab["line.matches"], di=lab["distinct.indicators"],
                tc=lab["total.cooccur.hits"], inds=", ".join(lab["indicators"]),
                g=r["agent_use_grade"], gn=r["grade_note"]))
        records.append({
            "kind": "observation", "ref": "proxyinst-" + relay.replace(".", "-"),
            "body": {"type": "infra.proxy_instance",
                     "data_schema": "urn:factum:infra:proxy-instance:1",
                     "data": data, "files": [],
                     "source": "@src-sweep",
                     "run": "@run-sweep",
                     "observed_at": SWEEP_DATE, "time_basis": "source_metadata"},
            "tags": tag({"grade": "OBSERVED", "legacy_kind": "relay_score",
                         "agent_use_grade": r["agent_use_grade"],
                         "line.matches": lab["line.matches"],
                         "distinct.indicators": lab["distinct.indicators"],
                         "total.cooccur.hits": lab["total.cooccur.hits"],
                         "timestamp_source": lab.get("timestamp_source")}),
        })

    # ---- 4. ioc records (indicator_census) ----
    for ev in events:
        if ev["record_kind"] != "indicator_census":
            continue
        lab = ev["labels"]
        ind = lab["indicator"]
        if ind in SKIP_IOC:
            drop_log["skipped_ioc"][ind] = SKIP_IOC[ind]
            continue
        term = INDICATORS[ind]
        extra = {"grade": "OBSERVED", "legacy_kind": "indicator_census",
                 "indicator": ind, "matching.lines": lab["matching.lines"],
                 "files": lab["files"], "timestamp_source": lab.get("timestamp_source"),
                 "status_rationale": (
                     "{n} matching lines across {m} files in the 2026-10-01 relay sweep "
                     "census; candidate pending noise review.".format(
                         n=lab["matching.lines"], m=lab["files"]))}
        if ind == "double_slash":
            extra["census_note"] = DOUBLE_SLASH_NOTE
        records.append({
            "kind": "observation", "ref": "ioc-" + ind,
            "body": {"type": "infra.ioc",
                     "data_schema": "urn:factum:infra:ioc:1",
                     "data": {"term": term, "category": "marker",
                              "provenance": LANE + " indicator census (sweep_v3.py)",
                              "status": "candidate"},
                     "files": [],
                     "source": "@src-sweep",
                     "run": "@run-sweep",
                     "observed_at": SWEEP_DATE, "time_basis": "source_metadata"},
            "tags": tag(extra),
        })

    # ---- 5. proxy_chain records (samples) ----
    # 5a. ts samples: join slug -> full shortener_link record in the rmn-re lane
    ts_events = [ev for ev in events if ev["record_kind"] == "relay_ts_sample"]
    wanted = {}
    for ev in ts_events:
        m = SLUG_RE.search(ev["description"])
        if m:
            wanted[m.group(1)] = ev
    slug_idx = build_rmn_slug_index(set(wanted))
    missing_slugs = sorted(set(wanted) - set(slug_idx))
    drop_log["ts_samples_slug_unresolved"] = missing_slugs

    chain_candidates = []  # dicts: svc, url, chain, obs_at, time_basis, ts_source, sample_kind, relay_label, verbatim
    for slug, ev in wanted.items():
        target, ts = slug_idx.get(slug, ("", ""))
        if not target:
            continue
        found = find_chain(target)
        relay_label = ev["labels"]["relay"]
        if found:
            svc, url, chain = found
        else:
            # fall back to the sweep's relay label mapped to host when no URL parse
            host = (RELAYS.get(relay_label) or {}).get("host") if RELAYS.get(relay_label) else None
            svc, url, chain = host or relay_label, target, [host or relay_label]
        obs_at = ts if ts and not ts.startswith("1970") else SWEEP_DATE
        chain_candidates.append({
            "svc": svc, "url": url, "chain": chain, "obs_at": obs_at,
            "time_basis": "source_metadata",
            "ts_source": "ts_samples" if ts and not ts.startswith("1970") else "fallback:dir_date_prefix",
            "sample_kind": "relay_ts_sample", "relay_label": relay_label,
            "verbatim": ev["description"]})

    # 5b. mention samples: extract relay URL from the verbatim line
    frag_only = {}
    for ev in events:
        if ev["record_kind"] != "relay_mention_sample":
            continue
        desc = ev["description"]
        relay_label = ev["labels"]["relay"]
        found = find_chain(desc)
        if not found:
            frag_only[relay_label] = frag_only.get(relay_label, 0) + 1
            continue
        svc, url, chain = found
        m = INNER_TS_RE.search(desc)
        inner_ts = m.group(1) if m else ""
        if inner_ts and not inner_ts.startswith("1970"):
            obs_at, ts_source = inner_ts, "inner_record"
        else:
            obs_at, ts_source = SWEEP_DATE, "fallback:dir_date_prefix"
        chain_candidates.append({
            "svc": svc, "url": url, "chain": chain, "obs_at": obs_at,
            "time_basis": "source_metadata", "ts_source": ts_source,
            "sample_kind": "relay_mention_sample", "relay_label": relay_label,
            "verbatim": desc})
    drop_log["fragment_only_mention_samples"] = frag_only

    # 5c. intra-batch dedup on (proxy_service, target_url); ts-sample evidence wins ties
    merged = {}
    for cand in sorted(chain_candidates,
                      key=lambda c: (c["svc"], c["url"],
                                     0 if c["sample_kind"] == "relay_ts_sample" else 1)):
        key = (cand["svc"], cand["url"])
        if key in merged:
            prev = merged[key]
            kinds = sorted(set(prev["sample_kinds"] + [cand["sample_kind"]]))
            # prefer the candidate with a real (non-fallback) timestamp
            if prev["ts_source"] == "fallback:dir_date_prefix" and cand["ts_source"] != "fallback:dir_date_prefix":
                winner = dict(cand)
            else:
                winner = dict(prev)
            winner["sample_kinds"] = kinds
            merged[key] = winner
        else:
            merged[key] = dict(cand, sample_kinds=[cand["sample_kind"]])

    n_corpus_dup = 0
    chain_idx = 0
    for key in sorted(merged):
        if key in EXISTING_CHAINS:
            n_corpus_dup += 1
            continue
        m = merged[key]
        chain_idx += 1
        records.append({
            "kind": "observation",
            "ref": "chain-%06d" % chain_idx,
            "body": {"type": "infra.proxy_chain",
                     "data_schema": "urn:factum:infra:proxy-chain:1",
                     "data": {"proxy_service": m["svc"], "target_url": m["url"],
                              "chain": m["chain"]},
                     "files": [],
                     "source": "@src-sweep",
                     "run": "@run-sweep",
                     "observed_at": m["obs_at"], "time_basis": m["time_basis"]},
            "tags": tag({"grade": "OBSERVED",
                         "legacy_kind": "+".join(m["sample_kinds"]),
                         "sample.relay": m["relay_label"],
                         "timestamp_source": m["ts_source"],
                         "verbatim": m["verbatim"],
                         "upstream_lane": ("2016-12-28-rmn-re"
                                           if "relay_ts_sample" in m["sample_kinds"] else None)}),
        })
    drop_log["corpus_duplicate_chains"] = n_corpus_dup
    drop_log["chains_emitted"] = sum(1 for r in records
                                    if r["kind"] == "observation"
                                    and r["body"]["type"] == "infra.proxy_chain")

    # ---- 6. reachability.check records (live probes, PROVENANCE.md / WRITEUP.md) ----
    probes = [
        ("https://markdown.new/", "GET", "response", 200,
         "Homepage read 2026-10-01 ~20:18-20:30 UTC; states 'No signup required'; rate limit self-declared 500 requests/day/IP."),
        ("https://markdown.new/https://example.com", "GET", "response", 200,
         "Benign test conversion #1 (GET) worked with no key."),
        ("https://markdown.new/https://example.com?format=json", "GET", "response", 200,
         "Benign test conversion #2 (GET ?format=json) worked with no key; returns {success,url,title,content,timestamp,method,duration_ms,tokens}."),
        ("https://markdown.new/crawl", "GET", "response", None,
         "Crawl endpoint read 2026-10-01; crawl results stored 14 days keyed by unguessable jobId, no public listing."),
        ("https://pure.md/", "GET", "response", None,
         "Homepage read 2026-10-01: signup required (API key); Starter $0/mo pay-as-you-go with $1 free credit, rate-limited without subscription."),
        ("https://r.jina.ai/", "GET", "blocked", None,
         "Live probe blocked by sandbox fetch policy; keyless status not re-verified this lane. Do not retry per runtime instruction."),
    ]
    for i, (target, method, outcome, http_status, note) in enumerate(probes):
        data = {"target": target, "method": method, "outcome": outcome}
        if http_status:
            data["http_status"] = http_status
        records.append({
            "kind": "observation", "ref": "reach-%d" % i,
            "body": {"type": "reachability.check",
                     "data_schema": "urn:factum:web:reachability-check:1",
                     "data": data, "files": [],
                     "source": "@src-sweep",
                     "run": "@run-sweep",
                     "observed_at": SWEEP_DATE, "time_basis": "source_metadata"},
            "tags": tag({"grade": "OBSERVED", "legacy_kind": "live_probe",
                         "probe_window": "2026-10-01 ~20:18-20:30 UTC (documented; exact per-probe times not recorded)",
                         "probe_note": note}),
        })

    bundle = {"bundle": 2, "actor": ACTOR, "idempotency_key": IDEMPOTENCY_KEY,
              "records": records}
    with open(OUT_BUNDLE, "w", encoding="utf-8") as fh:
        json.dump(bundle, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(OUT_DROPLOG, "w", encoding="utf-8") as fh:
        json.dump(drop_log, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    kinds = {}
    for r in records:
        k = (r["kind"], r["body"].get("type") if isinstance(r.get("body"), dict) else None)
        kinds[k] = kinds.get(k, 0) + 1
    print("records:", len(records))
    for k in sorted(kinds, key=str):
        print("  ", k, kinds[k])
    print("drop log:", json.dumps(drop_log, indent=1)[:800])
    print("wrote", OUT_BUNDLE)


if __name__ == "__main__":
    main()
