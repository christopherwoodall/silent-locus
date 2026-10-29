#!/usr/bin/env python3
"""Local pre-submit validator for bundle-ss41-swe-smith-mini.json.

Checks schema-required fields per the installed packs, bundle-local @ref
resolution, and the lane-tag invariant. Does NOT need the factum lock.
"""
import json
import os
import sys

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.join(LANE_DIR, "bundle-ss41-swe-smith-mini.json")
LANE = "swe-smith-mini-trajectories"

errors = []


def err(msg):
    errors.append(msg)


def main():
    b = json.load(open(BUNDLE))
    assert b["bundle"] == 2, "bundle version"
    assert b["actor"], "actor required"
    assert b["idempotency_key"], "idempotency_key required"
    recs = b["records"]
    refs = [r["ref"] for r in recs]
    if len(refs) != len(set(refs)):
        err("duplicate refs")
    refset = set(refs)
    kinds = {}

    def resolve(ref):
        # "@name" must name a bundle-local ref
        assert ref.startswith("@"), f"ref not @-form: {ref}"
        name = ref[1:]
        if name not in refset:
            err(f"dangling @ref: {ref}")
        return name

    for r in recs:
        ref = r["ref"]
        if len(ref) > 64:
            err(f"ref too long: {ref}")
        if r.get("tags", {}).get("lane") != LANE:
            err(f"missing/wrong tags.lane: {ref}")
        kind = r["kind"]
        body = r.get("body", {})
        kinds[kind] = kinds.get(kind, 0) + 1
        if kind == "observation":
            for f in ("type", "source", "observed_at", "time_basis", "files", "data"):
                if f not in body:
                    err(f"{ref}: observation missing {f}")
            if not isinstance(body.get("files"), list):
                err(f"{ref}: files not a list")
            t = body["type"]
            data = body.get("data", {})
            if t == "dataset.record":
                for f in ("snapshot", "locator"):
                    if f not in data:
                        err(f"{ref}: dataset.record missing data.{f}")
                loc = data.get("locator", {})
                if "artifact" not in loc:
                    err(f"{ref}: locator missing artifact")
                else:
                    aname = resolve(loc["artifact"])
                    arec = next(x for x in recs if x["ref"] == aname)
                    if arec["kind"] != "artifact":
                        err(f"{ref}: locator artifact not an artifact: {aname}")
                resolve(data["snapshot"])
            elif t == "dataset.snapshot":
                for f in ("dataset_uri", "coverage"):
                    if f not in data:
                        err(f"{ref}: dataset.snapshot missing data.{f}")
            elif t == "intel.behavior":
                for f in ("category", "description"):
                    if f not in data:
                        err(f"{ref}: intel.behavior missing data.{f}")
                sev = data.get("severity")
                if sev not in ("minimal", "low", "moderate", "high", "critical"):
                    err(f"{ref}: bad severity {sev}")
            else:
                err(f"{ref}: unknown observation type {t}")
            # source ref must resolve (source records are bundle-local here)
            s = body.get("source")
            if isinstance(s, str) and s.startswith("@"):
                resolve(s)
            rr = body.get("run")
            if isinstance(rr, str) and rr.startswith("@"):
                resolve(rr)
        elif kind == "source":
            for f in ("source_type", "locator"):
                if f not in body:
                    err(f"{ref}: source missing {f}")
        elif kind == "run":
            if "run_kind" not in body:
                err(f"{ref}: run missing run_kind")
        elif kind == "artifact":
            pass  # sha256/size optional
        elif kind == "edge":
            for f in ("subject", "predicate", "object"):
                if f not in body:
                    err(f"{ref}: edge missing {f}")
            if body.get("predicate") not in ("related_to", "supports"):
                err(f"{ref}: unexpected predicate {body.get('predicate')}")
            for f in ("subject", "object"):
                v = body[f]
                if isinstance(v, str) and v.startswith("@"):
                    resolve(v)
            for c in body.get("cites", []):
                if isinstance(c, str) and c.startswith("@"):
                    resolve(c)
            if body.get("basis") not in ("OBSERVED", "INFERENCE", "UPSTREAM"):
                err(f"{ref}: bad basis {body.get('basis')}")
        else:
            err(f"{ref}: unknown kind {kind}")

    print("kinds:", kinds)
    print("records:", len(recs))
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors[:30]:
            print(" -", e)
        sys.exit(1)
    print("VALIDATE_OK")


if __name__ == "__main__":
    main()
