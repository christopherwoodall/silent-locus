#!/usr/bin/env python3
"""Offline test runner for detect.py — fixtures only, no network.

Runs each fixture in tests/fixtures/ through detect.py and asserts the EXACT
{rule: alert_count} mapping. Also exercises:
  - malformed JSON input → exit code 2 with a clear stderr message
  - burst state persistence across two batches via --state-file

Usage: python3 tests/run_tests.py   (run from the detector/ directory)
Exit 0 when every assertion passes, 1 otherwise.
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DETECTOR = os.path.dirname(HERE)
DETECT = os.path.join(DETECTOR, "detect.py")
FIX = os.path.join(HERE, "fixtures")

# fixture → expected {rule_name: alert_count}. Absent = no alerts expected.
EXPECTATIONS = {
    # Rule 1 — incident burst geometry: 5 temp-account page creations in ~10 min.
    "f01_temp_account_burst_pos.jsonl": {
        "temp-account-burst": 1,
        "web2cit-config-edit": 4,          # 4 live configs (User: sandbox title excluded by design)
        "web2cit-nonbibliographic-target": 4,  # arcgis.com x3 + geodata.hawaii.gov; none allowlisted
    },
    # Same actors, spread over hours + one legit named-user edit → no burst.
    "f01_temp_account_burst_neg.jsonl": {
        "web2cit-config-edit": 3,          # 2 live configs + 1 legit abcnews config
        "web2cit-nonbibliographic-target": 2,  # arcgis.com x2; abcnews.go.com allowlisted → silent
    },
    # Rule 2 — incident sandbox sweep (May 10, 3 temp-account sandbox edits/7 min).
    "f02_sandbox_burst_pos.jsonl": {"sandbox-edit-burst": 1},
    # Same shape by named users → must NOT fire.
    "f02_sandbox_burst_neg.jsonl": {},
    # Rule 3 — Web2Cit/data/ tripwire.
    "f03_web2cit_config_pos.jsonl": {"web2cit-config-edit": 1},
    # Web2Cit/Docs (not data/) + ordinary article → silent.
    "f03_web2cit_config_neg.jsonl": {},
    # Rule 4 — ArcGIS geocoding target: the incident anomaly.
    "f04_nonbiblio_pos.jsonl": {
        "web2cit-config-edit": 1,
        "web2cit-nonbibliographic-target": 1,  # arcgis.com (title) + services.arcgis.com (content URL)
    },
    # Allowlisted bibliographic target (abcnews.go.com): rule 3 only.
    "f04_nonbiblio_neg.jsonl": {"web2cit-config-edit": 1},
    # Rule 5 — census probe tokens (tok=expt0; task-oai-117 in comment).
    "f05_probe_token_pos.jsonl": {"probe-token": 2},
    "f05_probe_token_neg.jsonl": {},
    # Rule 6 — empty comment (Pppery deletion shape) + machine comment + mw-replaced.
    "f06_comment_shape_pos.jsonl": {
        "web2cit-config-edit": 2,
        "web2cit-nonbibliographic-target": 1,  # line 1 only (arcgis.com); line 2 abcnews allowlisted
        "comment-tag-shape": 2,                # empty comment + machine-shaped comment/tagged edit
    },
    # Descriptive comment on allowlisted config + empty comment on ARTICLE (scoped out).
    "f06_comment_shape_neg.jsonl": {"web2cit-config-edit": 1},
}


def run_detect(fixture_path, extra_args=()):
    proc = subprocess.run(
        [sys.executable, DETECT, "--rules", os.path.join(DETECTOR, "rules.yaml"),
         *extra_args, fixture_path],
        capture_output=True, text=True)
    return proc


def count_rules(proc):
    counts = {}
    for line in proc.stdout.splitlines():
        try:
            alert = json.loads(line)
        except json.JSONDecodeError:
            return None, f"alert line is not JSON: {line[:120]}"
        rule = alert.get("rule")
        counts[rule] = counts.get(rule, 0) + 1
        # Grade-friendly output contract: every alert carries provenance.
        prov = alert.get("provenance") or {}
        if not (prov.get("finding") and prov.get("source_file") and prov.get("grade")):
            return None, f"alert missing provenance fields: {line[:200]}"
        for f in ("ts", "rule", "severity", "wiki", "user", "title", "evidence"):
            if f not in alert:
                return None, f"alert missing field {f!r}: {line[:200]}"
    return counts, None


def main():
    failures = []
    ran = 0

    for fixture, expected in sorted(EXPECTATIONS.items()):
        ran += 1
        path = os.path.join(FIX, fixture)
        proc = run_detect(path)
        if proc.returncode != 0:
            failures.append(f"{fixture}: exit={proc.returncode}, stderr={proc.stderr.strip()[:200]}")
            continue
        counts, err = count_rules(proc)
        if err:
            failures.append(f"{fixture}: {err}")
        elif counts != expected:
            failures.append(f"{fixture}: expected {expected}, got {counts}")

    # --- malformed input must exit 2 with a clear error ---
    ran += 1
    bad = os.path.join(FIX, "f07_malformed.jsonl")
    proc = run_detect(bad)
    if proc.returncode != 2:
        failures.append(f"f07_malformed: expected exit 2, got {proc.returncode}")
    elif "malformed input" not in proc.stderr.lower() and "invalid json" not in proc.stderr.lower():
        failures.append(f"f07_malformed: stderr unclear: {proc.stderr.strip()[:200]}")

    # --- burst state persists across batches ---
    ran += 1
    with tempfile.TemporaryDirectory() as tmp:
        state = os.path.join(tmp, "state.json")
        batch_a = os.path.join(tmp, "a.jsonl")
        batch_b = os.path.join(tmp, "b.jsonl")
        with open(batch_a, "w") as fh:
            for i, ts in enumerate(["2026-06-25T20:28:27Z", "2026-06-25T20:31:26Z",
                                    "2026-06-25T20:35:20Z"], start=1):
                fh.write(json.dumps({"ts": ts, "wiki": "en.wikipedia.org",
                                     "user": f"~2026-40000-{i:02d}",
                                     "title": f"Probe page {i}", "comment": "x",
                                     "tags": [], "content": "x"}) + "\n")
        with open(batch_b, "w") as fh:
            for i, ts in enumerate(["2026-06-25T20:36:09Z", "2026-06-25T20:38:33Z"], start=4):
                fh.write(json.dumps({"ts": ts, "wiki": "en.wikipedia.org",
                                     "user": f"~2026-40000-{i:02d}",
                                     "title": f"Probe page {i}", "comment": "x",
                                     "tags": [], "content": "x"}) + "\n")
        p1 = run_detect(batch_a, ("--state-file", state))
        c1, err = count_rules(p1)
        if p1.returncode != 0 or err or c1 != {}:
            failures.append(f"state test run1: expected silence, got rc={p1.returncode} counts={c1} err={err}")
        else:
            p2 = run_detect(batch_b, ("--state-file", state))
            c2, err = count_rules(p2)
            if p2.returncode != 0 or err or c2 != {"temp-account-burst": 1}:
                failures.append(f"state test run2: expected temp-account-burst x1, "
                                f"got rc={p2.returncode} counts={c2} err={err} stderr={p2.stderr.strip()[:200]}")
        # State file must be valid JSON in the documented format.
        try:
            with open(state) as fh:
                st = json.load(fh)
            assert isinstance(st, dict) and "temp-account-burst" in st
        except Exception as exc:
            failures.append(f"state test: bad state file: {exc}")

    # --- raw EventStreams revision-create shape normalizes end to end ---
    # (performer.user_text -> user, database -> wiki; README's claimed mapping)
    ran += 1
    with tempfile.TemporaryDirectory() as tmp:
        raw_batch = os.path.join(tmp, "raw_es.jsonl")
        with open(raw_batch, "w") as fh:
            fh.write(json.dumps({
                "meta": {"uri": "https://meta.wikimedia.org/wiki/Web2Cit/data/com/arcgis/templates.json",
                         "dt": "2026-06-25T20:35:20Z",
                         "domain": "meta.wikimedia.org",
                         "stream": "mediawiki.revision-create"},
                "database": "metawiki",
                "page_title": "Web2Cit/data/com/arcgis/templates.json",
                "page_namespace": 0,
                "rev_id": 30732701, "rev_parent_id": 0,
                "rev_content": "{\"templates\": []}",
                "comment": "adding geocoding template",
                "performer": {"user_text": "~2026-36867-71", "user_groups": ["*"]},
            }) + "\n")
        proc = run_detect(raw_batch)
        counts, err = count_rules(proc)
        want = {"web2cit-config-edit": 1, "web2cit-nonbibliographic-target": 1}
        if proc.returncode != 0 or err or counts != want:
            failures.append(f"raw-ES normalization: expected {want}, "
                            f"got rc={proc.returncode} counts={counts} err={err} "
                            f"stderr={proc.stderr.strip()[:200]}")

    # --- nameless rule / unknown type = clean exit 2, never a traceback ---
    ran += 1
    with tempfile.TemporaryDirectory() as tmp:
        bad_rules = os.path.join(tmp, "rules.yaml")
        with open(bad_rules, "w") as fh:
            fh.write("rules:\n  - description: no name here\n    type: title_prefix\n")
        proc = subprocess.run(
            [sys.executable, DETECT, "--rules", bad_rules,
             os.path.join(FIX, "f03_web2cit_config_neg.jsonl")],
            capture_output=True, text=True)
        if proc.returncode != 2:
            failures.append(f"bad-rules: expected exit 2, got {proc.returncode}")
        elif "traceback" in proc.stderr.lower():
            failures.append("bad-rules: leaked a traceback instead of a clean error")

    print(f"run_tests: {ran} checks, {len(failures)} failures")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
