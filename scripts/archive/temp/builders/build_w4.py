#!/usr/bin/env python3
"""W4 normalization sweep builder: events.jsonl + SHA256SUMS + PROVENANCE notes
for the five W4 dataset dirs. Read-only against raw/; writes events.jsonl,
SHA256SUMS, appends PROVENANCE.md in each target dir.

Usage: python3 build_w4.py /home/hatch/workspace/silent-locus
"""
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

REPO = sys.argv[1]
DATA = os.path.join(REPO, "data")
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def to_z(s: str) -> str:
    return s.replace("+00:00", "Z")


def rec(dataset, ts, kind, identity, *, labels, source_url=None, status=None,
        sha256=None, size_bytes=None, description=None, confidence="high", note=None):
    r = {
        "@timestamp": ts,
        "event": {"dataset": dataset, "created": CREATED},
        "record_kind": kind,
        "fingerprint": fp(identity),
        "labels": labels,
    }
    if source_url: r["source_url"] = source_url
    if status: r["status"] = status
    if sha256: r["sha256"] = sha256
    if size_bytes is not None: r["size_bytes"] = size_bytes
    if description: r["description"] = description
    if confidence: r["confidence"] = confidence
    if note: r["note"] = note
    return r


def write_events(d, rows):
    p = os.path.join(DATA, d, "events.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return p, len(rows)


def write_sums(d):
    ddir = os.path.join(DATA, d)
    entries = []
    for root, dirs, files in os.walk(ddir):
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, ddir)
            if rel in ("SHA256SUMS",):
                continue
            h = hashlib.sha256(open(full, "rb").read()).hexdigest()
            entries.append((rel, h))
    entries.sort()
    with open(os.path.join(ddir, "SHA256SUMS"), "w", encoding="utf-8") as f:
        for rel, h in entries:
            f.write(f"{h}  {rel}\n")
    return len(entries)


def append_prov(d, text):
    with open(os.path.join(DATA, d, "PROVENANCE.md"), "a", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------------------- agent-surfaces
def build_agent_surfaces():
    d = "2026-01-25-agent-surfaces"
    raw = os.path.join(DATA, d, "raw")
    rows = []
    for slug in sorted(os.listdir(raw)):
        sdir = os.path.join(raw, slug)
        if not os.path.isdir(sdir):
            continue
        pages = json.load(open(os.path.join(sdir, "pages.json"), encoding="utf-8"))
        base = slug
        prov = os.path.join(sdir, "PROVENANCE.md")
        if os.path.exists(prov):
            for line in open(prov, encoding="utf-8"):
                if line.strip().startswith("- base_url:"):
                    base = line.split("base_url:", 1)[1].strip()
        for p in pages:
            url = p.get("url") or p.get("final_url")
            ts = to_z(p["retrieved_at_utc"])
            labels = {
                "surface.slug": slug,
                "surface.base": base,
                "page.path": p.get("path", ""),
                "page.file": p.get("file", ""),
                "page.content_type": p.get("content_type", ""),
                "page.ok": bool(p.get("ok")),
                "capture.retrieved_via": "scripts/capture_agent_surfaces.py",
                "timestamp_source": "retrieved_at_utc:probe_observation",
            }
            rows.append(rec(
                d, ts, "venue_probe",
                f"agent-surfaces|{slug}|{url}",
                labels=labels,
                source_url=p.get("final_url") or url,
                status=str(p.get("http_status")) if p.get("http_status") is not None else None,
                sha256=p.get("sha256"),
                size_bytes=p.get("bytes"),
                description=f"agent surface probe: {slug} {p.get('path','')} -> HTTP {p.get('http_status')}",
                confidence="high",
            ))
    return write_events(d, rows)


# ------------------------------------------------------- march7-rce-modality
def build_march7():
    d = "2026-02-01-march7-rce-modality"
    raw = os.path.join(DATA, d, "raw")
    results = json.load(open(os.path.join(raw, "results.json"), encoding="utf-8"))
    gems = results["gems"]

    meta = {
        "sampledocpayload624286": dict(
            ts="2026-05-26T00:00:00Z", tsrc="investigator_reported:versions_all_on",
            role="payload", conf="high"),
        "harmlessdoctest624286": dict(
            ts="2026-05-26T00:00:00Z", tsrc="diffend_diff:gemspec_date_literal",
            role="benign_twin", conf="high"),
        "atlas-qa-snapshot-696b16c7": dict(
            ts="2026-05-28T00:00:00Z", tsrc="investigator_reported:published",
            role="candidate", conf="high"),
        "tf_drift_handoff_bundle_20260307t015800z": dict(
            ts="2026-03-07T02:58:00Z", tsrc="investigator_reported:published",
            role="candidate", conf="high"),
    }
    rows = []
    for gname, m in meta.items():
        g = gems[gname]
        diff = g["diffend"]
        diff_str = f"{diff['page_status']}:{'present' if diff['present'] else 'absent'}"
        vers = g["jfrog"]["versions"]
        if diff["present"]:
            surl = f"https://my.diffend.io/gems/{gname}"
        else:
            surl = f"https://index.rubygems.org/info/{gname}"
        labels = {
            "gem.name": gname,
            "gem.account": g["account"],
            "gem.role": m["role"],
            "probe.diffend": diff_str,
            "probe.compact_index": f"{g['compact']['status']}:metadata_stripped",
            "probe.versions": len(vers),
            "probe.version_list": sorted(vers, key=lambda v: [int(x) for x in v.split(".")]),
            "jfrog.xray": g["jfrog"].get("xray", ""),
            "investigator.downloads": g["investigator_reported"].get("downloads", ""),
            "investigator.window": g["investigator_reported"].get("window", ""),
            "timestamp_source": m["tsrc"],
        }
        if gname == "sampledocpayload624286":
            sweep = json.load(open(os.path.join(raw, "sweep.json"), encoding="utf-8"))
            fams = sorted({h["family"] for h in sweep["hits"].get(gname, [])})
            labels["sweep.hit_families"] = fams
            labels["sweep.hit_count"] = sum(len(v) for v in sweep["hits"].values() if isinstance(v, list))
        rows.append(rec(
            d, m["ts"], "campaign_specimen", f"gem:{gname}",
            labels=labels, source_url=surl,
            description=f"RubyGems modality specimen: {gname} ({m['role']}, acct {g['account']}, diffend {diff_str})",
            confidence=m["conf"],
        ))

    post = json.load(open(os.path.join(raw, "colonist-one-second-modality-post.json"), encoding="utf-8"))
    rows.append(rec(
        d, to_z(post["created_at"]), "artifact_observation",
        f"colonist-one-post:{post['id']}",
        labels={
            "post.id": post["id"],
            "post.author": "colonist-one",
            "post.created_at": post["created_at"],
            "file": "colonist-one-second-modality-post.json",
            "content": "investigator-reported doc-builder RCE + egress-test modality claims (cited as reported, not our observation)",
            "timestamp_source": "post.created_at",
        },
        description="investigator post dfac3a74-4685-43d8-9bd6-c76409f87ade (colonist-one): March-7 modality claims",
        confidence="high",
    ))
    return write_events(d, rows)


# ------------------------------------------------------------------ md-succ-ai
def build_md_succ_ai():
    d = "2026-02-14-md-succ-ai"
    raw = os.path.join(DATA, d, "raw")
    rows = []
    nfiles = sum(len(fs) for _, _, fs in os.walk(os.path.join(raw, "repo")))
    rows.append(rec(
        d, "2026-02-14T00:00:00Z", "artifact_observation", "md-succ-ai:repo",
        labels={
            "repo.remote": "https://github.com/vinaes/md-succ-ai",
            "repo.head_commit": "ea3ec780741b9f777d1e5575b2dd9d1b2fc80b82",
            "repo.first_commit": "2026-02-14",
            "repo.clone_date": "2026-09-28",
            "repo.files": nfiles,
            "repo.license": "FSL-1.1-Apache-2.0",
            "repo.live_spec": "https://md.succ.ai/openapi.json",
            "scope": "infrastructure facts only; operator identity out of scope",
            "index_decision": "unindexed standalone; proxy-ladder traces live in proxy-primitives index",
            "timestamp_source": "provenance:first_commit_date",
        },
        description="md.succ.ai repo clone (vinaes/md-succ-ai, HEAD ea3ec780, 79 files): HTML-to-Markdown API adopted by swarm agents",
        confidence="high",
    ))
    osha = open(os.path.join(raw, "openapi.json.sha256"), encoding="utf-8").read().strip()
    osize = os.path.getsize(os.path.join(raw, "openapi.json"))
    rows.append(rec(
        d, "2026-09-28T00:00:00Z", "artifact_observation", "md-succ-ai:openapi.json",
        labels={
            "file": "openapi.json",
            "api": "https://md.succ.ai/openapi.json",
            "timestamp_source": "provenance:fetch_date",
        },
        source_url="https://md.succ.ai/openapi.json",
        sha256=osha, size_bytes=osize,
        description="live OpenAPI spec for md.succ.ai (fetched 2026-09-28)",
        confidence="high",
    ))
    return write_events(d, rows)


# ----------------------------------------------------------- paste-archive-gap
def build_paste_gap():
    d = "2026-03-12-paste-archive-gap"
    raw = os.path.join(DATA, d, "raw")
    manifest = json.load(open(os.path.join(raw, "manifest.json"), encoding="utf-8"))
    lane_m = {"706a4b28", "010cb19f", "119c69ea", "63322d1f", "026ab4e1",
              "959d0d7e", "23a6dab7", "6c3cbe0b", "b3746a9f", "7bb3fcb0",
              "bafcf020", "4bf27a3e", "c221a04c", "c5b8d67d", "5deda448"}
    rows = []
    for e in manifest:
        pid = e["id"]
        if pid == "b3746a9f_decoded":
            ts, tsrc = "2026-09-14T21:56:52.066Z", "manifest.generated_at"
            identity = "anna.fyi:b3746a9f:decoded"
        elif pid == "d266bdde":
            ts, tsrc = "1970-01-01T00:00:00Z", "fallback:no_recoverable_date"
            identity = "anna.fyi:d266bdde"
        else:
            ts, tsrc = to_z(e["created_utc"]), "manifest.created_utc"
            identity = f"anna.fyi:{pid}"
        labels = {
            "paste.id": pid,
            "paste.source": "lane-m" if pid in lane_m or pid == "b3746a9f_decoded" else "lane-1-retry",
            "timestamp_source": tsrc,
        }
        for k in ("title", "author", "lang", "hits", "private"):
            if e.get(k) is not None:
                labels[f"paste.{k}"] = str(e[k])
        rows.append(rec(
            d, ts, "pastebin_probe", identity,
            labels=labels,
            source_url=e.get("source_url"),
            status=e.get("status"),
            sha256=e.get("sha256"),
            size_bytes=e.get("bytes"),
            description=f"anna.fyi paste {pid}: {e.get('title') or '(no title)'} by {e.get('author') or '(unknown)'} [{e.get('status')}]",
            confidence="high",
            note=("deletion confirmed 2026-09-28 lane-1 probe: /view + /view/raw 404, /api/paste returns Not found"
                  if pid == "d266bdde" else None),
        ))
    inv = os.path.join(raw, "investigator-repo", "joshuadavid-anna-revisions-2026-09-28.jsonl")
    nlines = sum(1 for _ in open(inv, encoding="utf-8"))
    ihash = hashlib.sha256(open(inv, "rb").read()).hexdigest()
    rows.append(rec(
        d, "2026-09-28T00:00:00Z", "artifact_observation",
        "anna.fyi:investigator-repo:joshuadavid-anna-revisions-2026-09-28",
        labels={
            "file": "investigator-repo/joshuadavid-anna-revisions-2026-09-28.jsonl",
            "corpus": "https://github.com/joshuadavid/wikiagentswarminvestigation agent-logs/anna.fyi/revisions.jsonl",
            "records": nlines,
            "use": "third-party verdicts recorded as-is (not our verdict); 45 new paste IDs harvested for lane-1 recovery",
            "timestamp_source": "filename:archive_date",
        },
        sha256=ihash,
        description="third-party anna.fyi revisions corpus snapshot (joshuadavid, 2026-09-28): source of 45 lane-1 recovered IDs",
        confidence="high",
    ))
    return write_events(d, rows)


# ---------------------------------------------------------- collusion-manifest
def build_collusion_manifest():
    d = "2026-05-01-collusion-manifest"
    raw = os.path.join(DATA, d, "raw")
    manifest = json.load(open(os.path.join(raw, "manifest.json"), encoding="utf-8"))
    gen = manifest["generated_at"]  # 2026-09-03T03:42:36Z
    rows = []
    with open(os.path.join(raw, "coverage-gaps.csv"), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            def arr(cell):
                try:
                    vals = json.loads(cell)
                    return [v.strip('"') for v in vals] if isinstance(vals, list) else [cell]
                except Exception:
                    return [cell] if cell else []
            labels = {
                "gap.site": row["site"],
                "gap.host": row["host"],
                "gap.category": row["category"],
                "gap.prior_status": row["prior_status"],
                "gap.compilation_status": row["compilation_status"],
                "gap.selected_distinct_texts": int(row["selected_distinct_texts"] or 0),
                "gap.discord_url_count": int(row["discord_urls"] or 0),
                "gap.fresh_responses_saved": int(row["fresh_responses_saved"] or 0),
                "gap.fresh_read_failures": int(row["fresh_read_failures_or_redirects"] or 0),
                "gap.prior_gap_remains": row["specific_prior_gap_remains"].strip().lower() == "true",
                "gap.limitations": arr(row["limitations"]),
                "gap.prior_evidence": arr(row["prior_evidence"]),
                "gap.scope": row["scope"],
                "timestamp_source": "manifest.generated_at",
            }
            rows.append(rec(
                d, gen, "coverage_gap",
                f"coverage-gap:{row['site']}|{row['host']}",
                labels=labels,
                source_url=row["canonical_url"],
                description=f"coverage gap assessment: {row['site']} ({row['host']}) — {row['compilation_status']}",
                confidence="high",
            ))
    rows.append(rec(
        d, gen, "artifact_observation",
        f"collusion-manifest:db_sha256={manifest['db_sha256']}",
        labels={
            "file": "manifest.json",
            "manifest.generated_at": gen,
            "manifest.db_sha256": manifest["db_sha256"],
            "manifest.cut": f"{manifest['cut']['field']} {manifest['cut']['operator']} {manifest['cut']['value']}",
            "export.revisions": manifest["counts"]["revisions"]["value"],
            "export.pages": manifest["counts"]["pages"]["value"],
            "export.labels": manifest["counts"]["labels"]["value"],
            "export.per_wiki": sorted(manifest["per_wiki"].keys()),
            "publisher": "https://rubyhack.ai/ via https://collusion.wiki/explorer/download",
            "timestamp_source": "manifest.generated_at",
        },
        description="collusion.wiki export manifest: 14,591 revisions / 4,579 pages / 3,103 labels, cut revision.write_date >= 2026-05-01",
        confidence="high",
    ))
    return write_events(d, rows)


def write_rollup(d, rows):
    p = os.path.join(DATA, d, "rollup.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return p, len(rows)


def rrec(dataset, ts, kind, identity, *, labels, description=None,
         confidence="high", note=None):
    r = {
        "@timestamp": ts,
        "event": {"dataset": dataset + "-rollup", "created": CREATED},
        "record_kind": kind,
        "fingerprint": fp(identity),
        "labels": labels,
        "observer": {"product": "build_w4.py", "type": "dataset"},
    }
    if description: r["description"] = description
    if confidence: r["confidence"] = confidence
    if note: r["note"] = note
    return r


def rollup_agent_surfaces():
    d = "2026-01-25-agent-surfaces"
    rows = [json.loads(l) for l in open(os.path.join(DATA, d, "events.jsonl"), encoding="utf-8")]
    out = []
    by_surface = {}
    for r in rows:
        by_surface.setdefault(r["labels"]["surface.slug"], []).append(r)
    for slug, rs in sorted(by_surface.items()):
        rs.sort(key=lambda r: r["@timestamp"])
        ok = sum(1 for r in rs if r["labels"]["page.ok"])
        cts = sorted({r["labels"]["page.content_type"] for r in rs if r["labels"]["page.content_type"]})
        out.append(rrec(
            d, rs[0]["@timestamp"], "venue_finding",
            f"agent-surfaces-rollup|{slug}",
            labels={
                "surface.slug": slug,
                "surface.base": rs[0]["labels"]["surface.base"],
                "capture.pages_total": len(rs),
                "capture.pages_ok": ok,
                "capture.pages_failed": len(rs) - ok,
                "capture.first_probe": rs[0]["@timestamp"],
                "capture.last_probe": rs[-1]["@timestamp"],
                "capture.content_types": cts,
                "timestamp_source": "events:first_probe",
            },
            description=f"capture summary: {slug} — {ok}/{len(rs)} pages ok, probes {rs[0]['@timestamp']}->{rs[-1]['@timestamp']}",
        ))
    return write_rollup(d, out)


def rollup_paste_gap():
    d = "2026-03-12-paste-archive-gap"
    rows = [json.loads(l) for l in open(os.path.join(DATA, d, "events.jsonl"), encoding="utf-8")
            if json.loads(l)["record_kind"] == "pastebin_probe"]
    out = []
    by_src = {}
    for r in rows:
        by_src.setdefault(r["labels"]["paste.source"], []).append(r)
    for src, rs in sorted(by_src.items()):
        dated = [r for r in rs if r["@timestamp"] != "1970-01-01T00:00:00Z"]
        dated.sort(key=lambda r: r["@timestamp"])
        nbytes = sum(r.get("size_bytes") or 0 for r in rs)
        ndel = sum(1 for r in rs if r.get("status") == "deleted_live_notfound")
        out.append(rrec(
            d, dated[0]["@timestamp"], "extraction",
            f"anna.fyi-rollup:{src}",
            labels={
                "batch.source": src,
                "batch.pastes": len(rs),
                "batch.bytes_total": nbytes,
                "batch.first_created": dated[0]["@timestamp"],
                "batch.last_created": dated[-1]["@timestamp"],
                "batch.deleted_observed": ndel,
                "timestamp_source": "events:first_created",
            },
            description=(f"recovery batch summary: {src} — {len(rs)} pastes, {nbytes} bytes, "
                         f"created {dated[0]['@timestamp']}->{dated[-1]['@timestamp']}"
                         + (f", {ndel} confirmed deleted live" if ndel else "")),
        ))
    return write_rollup(d, out)


def rollup_collusion_manifest():
    d = "2026-05-01-collusion-manifest"
    rows = [json.loads(l) for l in open(os.path.join(DATA, d, "events.jsonl"), encoding="utf-8")
            if json.loads(l)["record_kind"] == "coverage_gap"]
    out = []
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["labels"]["gap.category"], []).append(r)
    for cat, rs in sorted(by_cat.items()):
        out.append(rrec(
            d, "2026-09-03T03:42:36Z", "coverage_gap",
            f"coverage-gap-rollup:{cat}",
            labels={
                "gap.category": cat,
                "gap.sites": len(rs),
                "gap.hosts": len({r["labels"]["gap.host"] for r in rs}),
                "gap.prior_gap_remains": sum(1 for r in rs if r["labels"]["gap.prior_gap_remains"]),
                "gap.fresh_responses_saved": sum(r["labels"]["gap.fresh_responses_saved"] for r in rs),
                "gap.selected_distinct_texts": sum(r["labels"]["gap.selected_distinct_texts"] for r in rs),
                "gap.fresh_read_failures": sum(r["labels"]["gap.fresh_read_failures"] for r in rs),
                "timestamp_source": "manifest.generated_at",
            },
            description=(f"coverage rollup: {cat} — {len(rs)} sites, "
                         f"{sum(1 for r in rs if r['labels']['gap.prior_gap_remains'])} with prior gaps remaining, "
                         f"{sum(r['labels']['gap.fresh_responses_saved'] for r in rs)} fresh responses saved"),
        ))
    return write_rollup(d, out)


ROLLUP_BUILDERS = {
    "2026-01-25-agent-surfaces": rollup_agent_surfaces,
    # 2026-02-01-march7-rce-modality: no rollup — 5 atomic records, no genuine aggregate layer
    # 2026-02-14-md-succ-ai: no rollup — 2 artifact records, pure event stream
    "2026-03-12-paste-archive-gap": rollup_paste_gap,
    "2026-05-01-collusion-manifest": rollup_collusion_manifest,
}


# ------------------------------------------------------------------- main
BUILDERS = {
    "2026-01-25-agent-surfaces": build_agent_surfaces,
    "2026-02-01-march7-rce-modality": build_march7,
    "2026-02-14-md-succ-ai": build_md_succ_ai,
    "2026-03-12-paste-archive-gap": build_paste_gap,
    "2026-05-01-collusion-manifest": build_collusion_manifest,
}

PROV_NOTES = {
    "2026-01-25-agent-surfaces": """
## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: {nrows} records, one per captured page (`raw/<surface>/pages.json`, 11 surfaces).
- record_kind: `venue_probe`. Fingerprint identity string: `agent-surfaces|<surface_slug>|<page_url>` (sha256).
- @timestamp = page `retrieved_at_utc` (the probe observation is the event); labels.timestamp_source=`retrieved_at_utc:probe_observation`. `page.ok=false` pages kept with their HTTP status.
- Surface base from each `raw/<surface>/PROVENANCE.md` `base_url:` line.
- `rollup.jsonl`: {nrollup} rows, one per surface (record_kind `venue_finding`, event.dataset `2026-01-25-agent-surfaces-rollup`): pages_ok/pages_total, first/last probe, content types. Fingerprint identity: `agent-surfaces-rollup|<surface_slug>`.
- Regenerated `SHA256SUMS` (events.jsonl + rollup.jsonl + raw/**).
""",
    "2026-02-01-march7-rce-modality": """
## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: {nrows} records — 4 `campaign_specimen` (one per gem, from raw/results.json + sweep.json) and 1 `artifact_observation` (colonist-one's investigator post JSON).
- Fingerprint identity string: `gem:<gem_name>` for specimens; `colonist-one-post:<post_id>` for the post.
- @timestamp: sampledocpayload624286 -> 2026-05-26 (investigator_reported.versions_all_on); harmlessdoctest624286 -> 2026-05-26 (date literal inside its Diffend diff); atlas-qa-snapshot-696b16c7 -> 2026-05-28 (investigator_reported.published); tf_drift_handoff_bundle_20260307t015800z -> 2026-03-07T02:58Z (investigator_reported.published, consistent with the gem-name timestamp); post -> post.created_at 2026-09-05T17:02:27Z. labels.timestamp_source documents each.
- No rollup.jsonl: 5 atomic records, no genuine aggregate layer (deliberate per sweep rule).
- Regenerated `SHA256SUMS` (events.jsonl + raw/**).
""",
    "2026-02-14-md-succ-ai": """
## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: {nrows} records, both `artifact_observation`: the repo clone (raw/repo) and raw/openapi.json.
- Fingerprint identity strings: `md-succ-ai:repo` and `md-succ-ai:openapi.json`.
- @timestamp: repo -> 2026-02-14T00:00:00Z (first commit date, the layer's first event); labels.timestamp_source=`provenance:first_commit_date`. openapi.json -> 2026-09-28T00:00:00Z (fetch date); labels.timestamp_source=`provenance:fetch_date`. Note: raw/repo carries no .git dir (files only), so commit dates come from this PROVENANCE.md, not from git.
- No rollup.jsonl: 2 artifact records, pure event stream (deliberate per sweep rule).
- Regenerated `SHA256SUMS` (events.jsonl + raw/**).
""",
    "2026-03-12-paste-archive-gap": """
## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: {nrows} records — 67 `pastebin_probe` (one per raw/manifest.json entry: 15 lane-M + 51 lane-1 + b3746a9f_decoded) and 1 `artifact_observation` (raw/investigator-repo snapshot).
- Fingerprint identity string: `anna.fyi:<paste_id>` (`anna.fyi:b3746a9f:decoded` for the decoded cemetery JSON); `anna.fyi:investigator-repo:joshuadavid-anna-revisions-2026-09-28` for the snapshot.
- @timestamp = manifest `created_utc` per paste (labels.timestamp_source=`manifest.created_utc`); decoded record uses manifest `generated_at` 2026-09-14T21:56:52Z; the deleted paste d266bdde has no recoverable date -> sentinel 1970-01-01T00:00:00Z with labels.timestamp_source=`fallback:no_recoverable_date` (deletion confirmed in the 2026-09-28 lane-1 probe, recorded in note).
- `rollup.jsonl`: {nrollup} rows, one per recovery batch (`lane-m`, `lane-1-retry`; record_kind `extraction`, event.dataset `2026-03-12-paste-archive-gap-rollup`): paste count, total bytes, first/last created, confirmed deletions. Fingerprint identity: `anna.fyi-rollup:<source>`. (The investigator-repo snapshot is a provenance artifact, excluded from the batch rollup.)
- Regenerated `SHA256SUMS` (events.jsonl + rollup.jsonl + raw/**).
""",
    "2026-05-01-collusion-manifest": """
## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: {nrows} records — 110 `coverage_gap` (one per raw/coverage-gaps.csv row; new record_kind, see triage note) and 1 `artifact_observation` (raw/manifest.json itself).
- Fingerprint identity strings: `coverage-gap:<site>|<host>` for rows; `collusion-manifest:db_sha256=<db_sha256>` for the manifest.
- @timestamp: no per-row dates in the CSV -> manifest.generated_at 2026-09-03T03:42:36Z for all; labels.timestamp_source=`manifest.generated_at`.
- `rollup.jsonl`: {nrollup} rows, one per gap category (record_kind `coverage_gap`, event.dataset `2026-05-01-collusion-manifest-rollup`): site/host counts, gaps-remaining counts, saved-response and distinct-text totals. Fingerprint identity: `coverage-gap-rollup:<category>`.
- Regenerated `SHA256SUMS` (events.jsonl + rollup.jsonl + raw/**).
""",
}

if __name__ == "__main__":
    for d, build in BUILDERS.items():
        path, n = build()
        nr = 0
        if d in ROLLUP_BUILDERS:
            _, nr = ROLLUP_BUILDERS[d]()
        append_prov(d, PROV_NOTES[d].format(nrows=n, nrollup=nr))
        nsum = write_sums(d)  # AFTER provenance append so checksums match
        print(f"{d}: events.jsonl={n} rows, rollup.jsonl={nr} rows, SHA256SUMS={nsum} entries")
