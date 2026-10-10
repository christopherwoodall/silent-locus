#!/usr/bin/env python3
"""Build a Factum bundle from the 2022-08-09-github-forensics legacy lane.

Reads evidence/2022-08-09-github-forensics/events.jsonl (239 rows) and
rollup.jsonl (67 rows) and emits one Factum bundle (309 records):
  2 sources + 1 run + 239 observations + 67 claims.

Mapping (legacy record_kind -> Factum type):
  repo_snapshot        -> observation dataset.snapshot
  repo_commit          -> observation web.capture
  repo_issue           -> observation web.capture
  repo_fork            -> observation infra.ioc (term = fork full_name)
  repo_search_hit      -> observation infra.ioc (term = repo full_name)
  gist_scan_page       -> observation reachability.check (0 hits)
  sweep_negative       -> observation reachability.check (blocked)
  related_readme       -> observation web.capture
  fork_day_rollup      -> claim (property fork_day_burst, subject @run-ingest)
  issue_summary_rollup -> claim (property issue_summary, subject @run-ingest)

No edges at ingest (separate pass). Every record carries tags.lane.
No factum.* tags are set manually; the toolkit stamps them.
"""

import json
import sys

LANE = "2022-08-09-github-forensics"
ACTOR = "agent:lane-ingest-2022-08-09-github-forensics"
IDEMPOTENCY_KEY = "lane-ingest-2022-08-09-github-forensics-v1"

EVENTS = "evidence/2022-08-09-github-forensics/events.jsonl"
ROLLUP = "evidence/2022-08-09-github-forensics/rollup.jsonl"
# Source locators point at the POST-MOVE lane paths (files are moved into
# data/lanes/<lane>/ after submit, before the move commit).
EVENTS_LOC = "data/lanes/2022-08-09-github-forensics/events.jsonl"
ROLLUP_LOC = "data/lanes/2022-08-09-github-forensics/rollup.jsonl"


def base_tags(r, **extra):
    t = {
        "lane": LANE,
        "grade": "OBSERVED",
        "legacy_kind": r["record_kind"],
        "legacy_fingerprint": r["fingerprint"],
    }
    t.update(extra)
    return t


def obs(ref, ftype, data, observed_at, source, r, **tags):
    return {
        "ref": ref,
        "kind": "observation",
        "body": {
            "type": ftype,
            "data_schema": SCHEMAS[ftype],
            "data": data,
            "observed_at": observed_at,
            "time_basis": "source_metadata",
            "source": source,
            "files": [],
        },
        "tags": base_tags(r, **tags),
    }


SCHEMAS = {
    "dataset.snapshot": "urn:factum:datasets:snapshot:1",
    "web.capture": "urn:factum:web:web-capture:1",
    "infra.ioc": "urn:factum:infra:ioc:1",
    "reachability.check": "urn:factum:web:reachability-check:1",
}


def main():
    events = [json.loads(l) for l in open(EVENTS)]
    rollup = [json.loads(l) for l in open(ROLLUP)]
    records = []

    # --- sources ---------------------------------------------------------
    records.append({
        "ref": "src-events", "kind": "source",
        "body": {
            "source_type": "submitted",
            "locator": EVENTS_LOC,
            "title": "2022-08-09-github-forensics legacy events.jsonl (239 rows)",
        },
        "tags": {"lane": LANE, "grade": "OBSERVED",
                 "legacy_dataset": LANE, "retrieved_via": "GitHub REST API (2026-09-28/29)"},
    })
    records.append({
        "ref": "src-rollup", "kind": "source",
        "body": {
            "source_type": "submitted",
            "locator": ROLLUP_LOC,
            "title": "2022-08-09-github-forensics legacy rollup.jsonl (67 rows)",
        },
        "tags": {"lane": LANE, "grade": "OBSERVED",
                 "legacy_dataset": LANE + "-rollup",
                 "build_script": "build_rollup_w8.py (2026-09-29 W8)"},
    })

    # --- run -------------------------------------------------------------
    records.append({
        "ref": "run-ingest", "kind": "run",
        "body": {
            "run_kind": "extraction",
            "tool": "build_factum_bundle.py",
            "params": {
                "lane": LANE,
                "legacy_inputs": [EVENTS, ROLLUP],
                "legacy_rows": 306,
                "mapping_note": "see INGEST_NOTES.md in data/lanes/" + LANE + "/",
            },
            "coverage": {
                "complete": True,
                "total": 306,
                "scanned": 306,
                "description": (
                    "239 legacy event rows -> 239 observations; "
                    "67 rollup rows -> 67 claims. Per-day fork counts "
                    "independently recomputed: sum(forks.new) = 146 = "
                    "number of repo_fork rows."
                ),
            },
        },
        "tags": {"lane": LANE, "grade": "OBSERVED", "legacy_dataset": LANE},
    })

    n_obs = n_claim = 0
    seen_terms = {}

    for r in events:
        k = r["record_kind"]
        L = r["labels"]
        if k == "repo_snapshot":
            n_obs += 1
            records.append(obs(
                "obs-snapshot", "dataset.snapshot",
                {"dataset_uri": "https://github.com/sunblaze-ucb/exploitgym",
                 "coverage": "metadata_only"},
                L["repo.pushed_at"], "@src-events", r,
                description=r["description"],
                stars=L["repo.stargazers_count"],
                forks=L["repo.forks_count"],
                open_issues=L["repo.open_issues_count"],
                repo_created_at=L["repo.created_at"]))
        elif k == "repo_commit":
            n_obs += 1
            sha = L["commit.sha"]
            records.append(obs(
                "obs-commit", "web.capture",
                {"requested_url": "https://github.com/sunblaze-ucb/exploitgym/commit/" + sha,
                 "capture_kind": "http", "tool": "GitHub REST API"},
                L["commit.date"], "@src-events", r,
                description=r["description"],
                commit_sha=sha, commit_message=L["commit.message"],
                commit_author=L["commit.author"], commit_pr=L["commit.pr"],
                fix_scope=L["commit.fix_scope"],
                files_changed=L["commit.files_changed"],
                filenames=L["commit.filenames"],
                additions=L["commit.additions"], deletions=L["commit.deletions"],
                redaction_note=L["commit.redaction_note"]))
        elif k == "repo_issue":
            n_obs += 1
            n = L["issue.number"]
            records.append(obs(
                "obs-issue-%d" % n, "web.capture",
                {"requested_url": "https://github.com/sunblaze-ucb/exploitgym/issues/%d" % n,
                 "capture_kind": "http", "tool": "GitHub REST API"},
                L["issue.created_at"], "@src-events", r,
                description=r["description"],
                issue_number=n, issue_title=L["issue.title"],
                issue_state=L["issue.state"], issue_user=L["issue.user"],
                issue_is_pr=L["issue.is_pr"],
                issue_updated_at=L["issue.updated_at"]))
        elif k == "repo_fork":
            n_obs += 1
            term = L["fork.full_name"]
            assert term not in seen_terms, "duplicate fork term: " + term
            seen_terms[term] = True
            records.append(obs(
                "obs-fork-" + r["fingerprint"][:12], "infra.ioc",
                {"term": term, "category": "other", "status": "active",
                 "provenance": LANE},
                L["fork.created_at"], "@src-events", r,
                description=r["description"],
                fork_owner=L["fork.owner"], source_url=r["source_url"],
                fork_stargazers=L["fork.stargazers_count"],
                fork_forks=L["fork.forks_count"]))
        elif k == "repo_search_hit":
            n_obs += 1
            term = L["repo.full_name"]
            assert term not in seen_terms, "duplicate search-hit term: " + term
            seen_terms[term] = True
            records.append(obs(
                "obs-search-" + r["fingerprint"][:12], "infra.ioc",
                {"term": term, "category": "other", "status": "active",
                 "provenance": ("GitHub repo search: "
                                "exploitgym in:description OR exploitgym in:readme")},
                L["repo.created_at"], "@src-events", r,
                description=r["description"],
                repo_description=L["repo.description"],
                repo_stargazers=L["repo.stargazers_count"],
                search_total=L["repo.search_total"],
                search_query=L["repo.search_query"]))
        elif k == "gist_scan_page":
            n_obs += 1
            p = L["gist.page"]
            records.append(obs(
                "obs-gistpage-%d" % p, "reachability.check",
                {"target": "https://api.github.com/gists/public?per_page=100&page=%d" % p,
                 "method": "GET", "outcome": "response", "http_status": 200},
                r["retrieved_at"], "@src-events", r,
                description=r["description"],
                gist_page=p, gists_scanned=L["gist.scanned"],
                exploitgym_hits=L["gist.exploitgym_hits"],
                gist_window=L["gist.window"]))
        elif k == "sweep_negative":
            n_obs += 1
            block = L["api.block"]
            if block == "rate_limit":
                p = L["gist.page"]
                ip = "104.28.196.77" if p == 2 else "104.28.228.77"
                records.append(obs(
                    "obs-gistpage-%d-blocked" % p, "reachability.check",
                    {"target": "https://api.github.com/gists/public?per_page=100&page=%d" % p,
                     "method": "GET", "outcome": "blocked", "http_status": 403,
                     "error": ("API rate limit exceeded for %s. (But here's the good news: "
                               "Authenticated requests get a higher rate limit. Check out the "
                               "documentation for more details.)" % ip)},
                    r["retrieved_at"], "@src-events", r,
                    description=r["description"],
                    gist_page=p, api_block=block))
            elif block == "unauthenticated_401":
                if "api.files" in L:  # stargazers
                    records.append(obs(
                        "obs-stargazers-blocked", "reachability.check",
                        {"target": ("https://api.github.com/repos/sunblaze-ucb/exploitgym/"
                                    "stargazers?per_page=100"),
                         "method": "GET", "outcome": "blocked", "http_status": 401,
                         "error": "Requires authentication"},
                        r["retrieved_at"], "@src-events", r,
                        description=r["description"],
                        api_block=block, pages_unavailable=L["api.n_files"],
                        gap=L["sweep.gap"]))
                else:  # search/code
                    records.append(obs(
                        "obs-searchcode-blocked", "reachability.check",
                        {"target": "https://api.github.com/search/code",
                         "method": "GET", "outcome": "blocked", "http_status": 401,
                         "error": "Requires authentication"},
                        r["retrieved_at"], "@src-events", r,
                        description=r["description"],
                        api_block=block, searched_terms=L["api.terms"],
                        gap=L["sweep.gap"]))
            else:
                raise AssertionError("unknown api.block: " + block)
        elif k == "related_readme":
            n_obs += 1
            full = L["repo.full_name"]
            records.append(obs(
                "obs-readme-" + r["fingerprint"][:12], "web.capture",
                {"requested_url": "https://api.github.com/repos/%s/contents/README.md" % full,
                 "capture_kind": "http",
                 "tool": "GitHub REST API (Accept: raw)"},
                L["repo.created_at"] + "T00:00:00Z", "@src-events", r,
                description=r["description"],
                repo_full_name=full, confidence=r.get("confidence"),
                readme_sha256=L["readme.sha256"],
                readme_size_bytes=L["readme.size_bytes"],
                cached_path=("data/lanes/%s/raw/related-readmes/%s"
                             % (LANE, r["file"].split("/")[-1])),
                timestamp_source="provenance:created_date (date-only; midnight assumed)"))
        else:
            raise AssertionError("unmapped event kind: " + k)

    # --- claims (rollups) -------------------------------------------------
    for r in rollup:
        k = r["record_kind"]
        L = r["labels"]
        labels = {kk: vv for kk, vv in L.items() if kk != "timestamp_source"}
        if k == "fork_day_rollup":
            n_claim += 1
            records.append({
                "ref": "claim-forkday-" + L["day"], "kind": "claim",
                "body": {
                    "subject": "@run-ingest",
                    "property": "fork_day_burst",
                    "value": {"labels": labels},
                    "basis": "OBSERVED",
                    "cites": ["@run-ingest"],
                    "note": r["description"],
                },
                "tags": base_tags(r, legacy_dataset=LANE + "-rollup",
                                  timestamp_source="labels:rollup.day"),
            })
        elif k == "issue_summary_rollup":
            n_claim += 1
            records.append({
                "ref": "claim-issue-summary", "kind": "claim",
                "body": {
                    "subject": "@run-ingest",
                    "property": "issue_summary",
                    "value": {"labels": labels},
                    "basis": "OBSERVED",
                    "cites": ["@run-ingest"],
                    "note": r["description"],
                },
                "tags": base_tags(r, legacy_dataset=LANE + "-rollup",
                                  timestamp_source="labels:issue.created_at(max)"),
            })
        else:
            raise AssertionError("unmapped rollup kind: " + k)

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "records": records,
        "tags": {},
    }
    print("observations: %d  claims: %d  records: %d" % (n_obs, n_claim, len(records)),
          file=sys.stderr)
    assert n_obs == 239, n_obs
    assert n_claim == 67, n_claim
    json.dump(bundle, sys.stdout, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
