#!/usr/bin/env python3
"""Client-side filter for the crt.sh May-Jul 2026 issuance sweep.

Filters:
  window      : not_before OR entry_timestamp in [2026-05-01, 2026-07-31]
  known cert  : exclude serial 040b3c091fd4e4d8ccff7b8fe33b7979
  pattern SAN filters (per super-search-plan.md Step 1):
    webhook-any : keep rows whose SANs carry fleet markers —
                  UUID-shaped subdomain segment (dead-drop inbox style),
                  or hysandbox / fleet strings in the SAN
    vercel-sub  : keep rows whose SANs contain jqp, md.succ, or allorigins
    hy3-any/hy4-any : keep rows whose issuer_name contains "tencent" or whose
                  SANs contain tencent/hunyuan
                  (tie re-justified: chinese-amap-fleet osint 2026-10-05 +
                   eastmoney Dec-2025 "Hunyuan"->"HY" rebrand)
Novelty: per in-window cert SAN hostnames, grep lists/urls/urls.jsonl and
  data/lanes/metre-thread/mined-items.md -> OVERLAP / NEW-candidate.

Writes: SUMMARY.json in the crtsh dir. Probe failures listed to stdout.
"""
import json, os, re, sys, glob

CRTDIR = os.path.expanduser("~/workspace/silent-locus/data/lanes/metre-thread/raw/supersearch/crtsh")
REPO = os.path.expanduser("~/workspace/silent-locus")
KNOWN_SERIAL = "040b3c091fd4e4d8ccff7b8fe33b7979"
WIN_LO, WIN_HI = "2026-05-01", "2026-07-31"

UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)

# slug -> extra SAN/issuer filter function name
EXTRA_FILTERS = {
    "webhook-any": "fleet_markers",
    "vercel-sub": "vercel_relay",
    "hy3-any": "tencent_tie",
    "hy4-any": "tencent_tie",
}

def sans_of(row):
    nv = row.get("name_value") or ""
    return [s.strip().lower() for s in nv.replace("\r", "\n").split("\n") if s.strip()]

def norm_serial(s):
    return re.sub(r"[^0-9a-f]", "", (s or "").lower())

def extra_ok(slug, row, sans):
    f = EXTRA_FILTERS.get(slug)
    if not f:
        return True
    if f == "fleet_markers":
        return any(UUID_RE.search(s) for s in sans) or any(
            ("hysandbox" in s or "fleet" in s) for s in sans)
    if f == "vercel_relay":
        return any(("jqp" in s or "md.succ" in s or "allorigins" in s) for s in sans)
    if f == "tencent_tie":
        issuer = (row.get("issuer_name") or "").lower()
        return ("tencent" in issuer) or any(("tencent" in s or "hunyuan" in s) for s in sans)
    return True

def in_window(row):
    for key in ("not_before", "entry_timestamp"):
        v = (row.get(key) or "")[:10]
        if WIN_LO <= v <= WIN_HI:
            return True
    return False

def load_haystacks():
    urls = open(os.path.join(REPO, "lists/urls/urls.jsonl")).read().lower()
    mined = open(os.path.join(REPO, "data/lanes/metre-thread/mined-items.md")).read().lower()
    return urls, mined

def grade(san, urls, mined):
    return "OVERLAP" if (san in urls or san in mined) else "NEW-candidate"

def main():
    urls, mined = load_haystacks()
    summary = {"window": [WIN_LO, WIN_HI], "excluded_serial": KNOWN_SERIAL,
               "patterns": {}, "probe_failures": []}
    total_in = 0
    for path in sorted(glob.glob(os.path.join(CRTDIR, "q-*.json"))):
        slug = os.path.basename(path)[2:-5]
        try:
            rows = json.load(open(path))
            assert isinstance(rows, list)
        except Exception as e:
            summary["probe_failures"].append({"slug": slug, "error": str(e)})
            continue
        kept = []
        for r in rows:
            if norm_serial(r.get("serial_number")) == KNOWN_SERIAL:
                continue
            if not in_window(r):
                continue
            sans = sans_of(r)
            if not extra_ok(slug, r, sans):
                continue
            per_san = [{"san": s, "novelty": grade(s, urls, mined)} for s in sans]
            kept.append({
                "id": r.get("id"),
                "serial": r.get("serial_number"),
                "issuer": r.get("issuer_name"),
                "not_before": r.get("not_before"),
                "not_after": r.get("not_after"),
                "entry_timestamp": r.get("entry_timestamp"),
                "common_name": r.get("common_name"),
                "sans": per_san,
                "cert_url": f"https://crt.sh/?id={r.get('id')}",
            })
        total_in += len(kept)
        summary["patterns"][slug] = {"total_rows": len(rows), "in_window_rows": len(kept), "certs": kept}
    summary["total_in_window"] = total_in
    out = os.path.join(CRTDIR, "SUMMARY.json")
    json.dump(summary, open(out, "w"), indent=2)
    print(f"patterns: {len(summary['patterns'])}, probe failures: {len(summary['probe_failures'])}, "
          f"total in-window certs: {total_in}")
    for f in summary["probe_failures"]:
        print("FAIL:", f)
    for slug, p in summary["patterns"].items():
        if p["in_window_rows"]:
            print(f"{slug}: {p['total_rows']} total, {p['in_window_rows']} in-window")

if __name__ == "__main__":
    main()
