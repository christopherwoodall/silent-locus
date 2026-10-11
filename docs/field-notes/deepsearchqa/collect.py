#!/usr/bin/env python3
"""LANE deepsearchqa: enumerate the DeepSearchQA benchmark and extract question fingerprints.

Idempotent: re-running re-downloads DSQA-full.csv only if the local copy is missing
or its sha256 differs from state.json. Never duplicates questions.jsonl rows.

Source: google/deepsearchqa on HuggingFace (public, Apache-2.0, not gated).
Revision pinned via --rev (default b2623f8653065c2672de6d941fc5434cd652376c).
Politeness: curl only, <=1 req/2s (single file fetch), no crawling.

qid scheme: dsqa_<NNN> = 0-based row index in DSQA-full.csv order.
  Verified: Transluce's "dsqa_250" (June-17 DoE incident question) == row 250,
  whose text is the civilrightsdata.ed.gov 2017-2018 counselor/harassment-ratio
  question. Do NOT renumber.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
DATASET_URL = "https://huggingface.co/datasets/google/deepsearchqa"
EXPECTED_SHA256 = "25d48dcf7efa872e5467032e8b8eedf38d301f59a252d0da95cda584baa78396"

GOV_RE = re.compile(r"\b[\w.-]+\.gov\b", re.IGNORECASE)

# domain/agency family -> tag applied when the pattern matches the question text
FAMILY_TAGS = [
    (re.compile(r"\bcivilrightsdata\.ed\.gov\b|\bnces\.ed\.gov\b|\bnationsreportcard\.gov\b", re.I), "gov-education"),
    (re.compile(r"\bdata\.nysed\.gov\b", re.I), "gov-education-ny"),
    (re.compile(r"\btea\.texas\.gov\b", re.I), "gov-education-tx"),
    (re.compile(r"\bcensus\.gov\b|\bdata\.census\.gov\b", re.I), "gov-census"),
    (re.compile(r"\bwonder\.cdc\.gov\b|\bcdc\.gov\b", re.I), "gov-cdc"),
    (re.compile(r"\bbea\.gov\b", re.I), "gov-bea"),
    (re.compile(r"\bbls\.gov\b", re.I), "gov-bls"),
    (re.compile(r"\btrade\.gov\b", re.I), "gov-trade"),
    (re.compile(r"\busda\.gov\b|\bers\.usda\.gov\b", re.I), "gov-usda"),
    (re.compile(r"\bnoaa\.gov\b|\bweather\.gov\b", re.I), "gov-noaa"),
    (re.compile(r"\b(fbi|vault\.fbi\.gov)\b", re.I), "gov-fbi"),
    (re.compile(r"\bcia\.gov\b", re.I), "gov-cia"),
    (re.compile(r"\bcongress\.gov\b", re.I), "gov-congress"),
    (re.compile(r"\bnps\.gov\b", re.I), "gov-nps"),
    (re.compile(r"\bmedicaid\.gov\b", re.I), "gov-medicaid"),
    (re.compile(r"\belections\.il\.gov\b|\bhistorical\.elections\.virginia\.gov\b|\baec\.gov\b", re.I), "gov-elections"),
    (re.compile(r"\bfoia\.state\.gov\b", re.I), "gov-state-dept"),
    (re.compile(r"\bproductsafety\.gov\b", re.I), "gov-cpsc"),
    (re.compile(r"\btransit\.dot\.gov\b", re.I), "gov-dot"),
    (re.compile(r"\bclinicaltrials\.gov\b", re.I), "gov-clinicaltrials"),
    (re.compile(r"\babs\.gov\b", re.I), "gov-abs-aus"),
    (re.compile(r"\bwebarchive\.nationalarchives\.gov\b", re.I), "gov-archives"),
    (re.compile(r"\bdepartment of justice\b|\bdoj\b|\bojjdp\b|\bjuvenile justice\b", re.I), "gov-justice-flavored"),
    (re.compile(r"\bcensus\b", re.I), "census-flavored"),
    (re.compile(r"\bbureau of economic analysis\b", re.I), "gov-bea"),
]

# qids with special, evidence-backed flags (never invented)
FLAGGED = {
    # Empirically confirmed: Transluce "dsqa_250" == row index 250 of DSQA-full.csv.
    "dsqa_250": ["incident-match-doe-20260617"],
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def state_path():
    return os.path.join(BASE, "state.json")


def load_state():
    p = state_path()
    if os.path.exists(p):
        return json.load(open(p))
    return {}


def save_state(state):
    with open(state_path(), "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def download_csv(rev, out_path):
    url = f"https://huggingface.co/datasets/google/deepsearchqa/resolve/{rev}/DSQA-full.csv"
    # one request, curl follows the HF temporary redirect; politeness sleep handled by caller
    subprocess.run(
        ["curl", "-sSL", "--max-time", "300", url, "-o", out_path],
        check=True,
    )


def tag_question(qid, category, answer_type, text):
    tags = []
    tags.append("category:" + re.sub(r"\s+", "-", category.strip().lower()))
    tags.append("answer-type:" + re.sub(r"\s+", "-", answer_type.strip().lower()))
    if GOV_RE.search(text):
        tags.append("gov-data")
    seen = set()
    for pat, tag in FAMILY_TAGS:
        if pat.search(text) and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    for flag in FLAGGED.get(qid, []):
        if flag not in seen:
            tags.append(flag)
            seen.add(flag)
    return sorted(tags)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="b2623f8653065c2672de6d941fc5434cd652376c",
                    help="HF dataset revision (commit sha) to pin")
    args = ap.parse_args()

    os.makedirs(DATA, exist_ok=True)
    state = load_state()
    csv_path = os.path.join(DATA, "DSQA-full.csv")
    jsonl_path = os.path.join(DATA, "questions.jsonl")

    started = state.get("started_utc") or datetime.now(timezone.utc).isoformat()
    rev = args.rev

    need_dl = True
    if os.path.exists(csv_path):
        cur = sha256_file(csv_path)
        if cur == state.get("csv_sha256") == EXPECTED_SHA256:
            need_dl = False
            print(f"cache hit: {csv_path} sha256 matches state.json; skipping download")
        else:
            print(f"sha mismatch (local={cur[:12]} expected={EXPECTED_SHA256[:12]}); re-downloading")

    if need_dl:
        download_csv(rev, csv_path)
        import time
        time.sleep(2)  # politeness: <=1 req/2s
        cur = sha256_file(csv_path)
        if cur != EXPECTED_SHA256:
            print(f"FATAL: downloaded sha {cur} != expected {EXPECTED_SHA256}", file=sys.stderr)
            sys.exit(1)
        print(f"downloaded {csv_path} ({os.path.getsize(csv_path)} bytes), sha256 ok")

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out = []
    for i, r in enumerate(rows):
        qid = f"dsqa_{i:03d}"
        out.append({
            "qid": qid,
            "question_text": r["problem"],
            "source_url": DATASET_URL,
            "tags": tag_question(qid, r["problem_category"], r["answer_type"], r["problem"]),
        })

    # atomic write, no duplicates possible: full rewrite each run
    tmp = jsonl_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    os.replace(tmp, jsonl_path)

    state = {
        "lane": "deepsearchqa",
        "started_utc": started,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "watermark": rev,
        "csv_sha256": EXPECTED_SHA256,
        "dataset_url": DATASET_URL,
        "license": "apache-2.0",
        "gated": False,
        "items_collected": len(out),
        "status": "complete",
    }
    save_state(state)
    print(f"wrote {jsonl_path}: {len(out)} questions; state.json updated")


if __name__ == "__main__":
    main()
