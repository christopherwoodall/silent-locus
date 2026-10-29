#!/usr/bin/env python3
"""Build the 2026-09-09-pixelleak-glow-labs collection.

Single-collection build script (repo convention: lives in the event dir).

What it does:
  1. Fetches and caches raw artifacts into raw/:
       - the Glow Labs PixelLeak blog post HTML
       - the two CDN images that had URLs (Image 1 in the report had no URL;
         its absence is recorded in PROVENANCE.md, never invented)
     Downloads are verified (HTML contains "PixelLeak"; images carry valid
     PNG magic). Existing valid files are kept (idempotent re-runs).
  2. Extracts the report's claims into events.jsonl, conforming to
     schema/record.schema.json. Confidence is "confirmed" only for what this
     script itself verified (artifact bytes on disk); every vendor claim is
     "reported". No invented IDs, dates, or URLs.
  3. Writes PROVENANCE.md and SHA256SUMS.

Read-only w.r.t. the rest of the repo. Safe to re-run.
"""

import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SLUG = "2026-09-09-pixelleak-glow-labs"
BLOG_URL = "https://www.glow.io/blogs/how-ai-agents-exposed-developer-screenshots-from-leading-tech-companies"
IDENTITY_STRING = f"{SLUG}:glow-labs-pixelleak-report"
UA = "Mozilla/5.0 (research-capture; silent-locus dataset build)"

ARTIFACTS = [
    {
        "filename": "pixelleak-blog.html",
        "url": BLOG_URL,
        "kind": "html",
        "check": lambda b: b"PixelLeak" in b,
        "check_desc": 'body contains b"PixelLeak"',
    },
    {
        "filename": "glow-system-architecture-v2-2.png",
        "url": "https://cdn.prod.website-files.com/6a5123806594d44620f087e9/6abbe4c94d8eebc2928bee46_Glow%20%C2%B7%20System%20Architecture%20v2-2.png",
        "kind": "png",
        "check": lambda b: b.startswith(b"\x89PNG\r\n\x1a\n"),
        "check_desc": "PNG magic bytes",
        "note": "Report 'Image 0'. Marketing architecture diagram, not evidence.",
    },
    {
        "filename": "glow-system-architecture-v2-2-1.png",
        "url": "https://cdn.prod.website-files.com/6a5123806594d44620f087e9/6abbe4b51267f3ec078c9244_Glow%20%C2%B7%20System%20Architecture%20v2-2-1.png",
        "kind": "png",
        "check": lambda b: b.startswith(b"\x89PNG\r\n\x1a\n"),
        "check_desc": "PNG magic bytes",
        "note": "Report 'Image 2'. Marketing architecture diagram, not evidence.",
    },
]

SENTINEL = "1970-01-01T00:00:00Z"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, dest, check, check_desc, attempts=3):
    """Download url -> dest if dest is missing or fails validation."""
    if os.path.exists(dest):
        with open(dest, "rb") as f:
            body = f.read()
        if check(body):
            return body, False  # cached
    last_err = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
            if not check(body):
                raise ValueError(f"validation failed ({check_desc})")
            tmp = dest + ".tmp"
            with open(tmp, "wb") as f:
                f.write(body)
            os.replace(tmp, dest)
            return body, True
        except Exception as e:  # noqa: BLE001 - backoff then report
            last_err = e
            time.sleep(2 * (i + 1))
    raise Runtime_error(f"fetch failed for {url}: {last_err}")


class Runtime_error(Exception):
    pass


def rec(record_kind, timestamp, description, labels, confidence,
        payloads=None, note=None, file=None, sha256=None, size_bytes=None,
        retrieved_at=None, source_url=BLOG_URL):
    labels = dict(labels)
    labels.setdefault("source", "glow-labs-pixelleak-blog")
    r = {
        "@timestamp": timestamp,
        "event": {"dataset": SLUG, "created": NOW},
        "record_kind": record_kind,
        "fingerprint": FINGERPRINT,
        "labels": labels,
        "confidence": confidence,
        "description": description,
        "source_url": source_url,
    }
    if payloads:
        r["payloads"] = payloads
    if note:
        r["note"] = note
    if file:
        r["file"] = file
    if sha256:
        r["sha256"] = sha256
    if size_bytes is not None:
        r["size_bytes"] = size_bytes
    if retrieved_at:
        r["retrieved_at"] = retrieved_at
        r["retrieved_via"] = "live-get"
    return r


def payload(kind, content, content_type="text/plain"):
    return {"kind": kind, "content_type": content_type, "content": content}


NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
FINGERPRINT = hashlib.sha256(IDENTITY_STRING.encode()).hexdigest()


def main():
    os.makedirs(RAW, exist_ok=True)
    meta = {}
    for art in ARTIFACTS:
        dest = os.path.join(RAW, art["filename"])
        body, fresh = fetch(art["url"], dest, art["check"], art["check_desc"])
        meta[art["filename"]] = {
            "url": art["url"],
            "sha256": sha256_file(dest),
            "size_bytes": len(body),
            "fresh_download": fresh,
            "note": art.get("note", ""),
        }
        print(f"{'fetched' if fresh else 'cached '} {art['filename']} "
              f"({len(body)} bytes, sha256 {meta[art['filename']]['sha256'][:12]}...)")

    retrieved_at = NOW
    html_file = f"data/{SLUG}/raw/pixelleak-blog.html"
    html_meta = meta["pixelleak-blog.html"]

    rows = [
        rec(
            "report_capture", SENTINEL,
            "Glow Labs 'PixelLeak' blog post captured as HTML artifact",
            {"timestamp_source": "fallback:no_recoverable_date",
             "artifact": "pixelleak-blog.html",
             "capture_note": "Report publication date not stated in the report text; "
                             "collection dated by disclosure-outreach start 2026-09-09."},
            "confirmed",
            file=html_file, sha256=html_meta["sha256"],
            size_bytes=html_meta["size_bytes"], retrieved_at=retrieved_at,
        ),
        rec(
            "disclosure_outreach", "2026-09-09T00:00:00Z",
            "Glow Labs began outreach to affected organizations on 2026-09-09 (per report)",
            {"timestamp_source": "report-text:vendor-reported"},
            "reported",
            payloads=[payload(
                "report_quote",
                "Glow Labs reached out to organizations identified during the "
                "PixelLeak research beginning September 9, 2026 but it's likely "
                "that others are also affected.")],
        ),
        rec(
            "technique", SENTINEL,
            "Technique: agents unable to attach screenshots via CLI published them to an adjacent public repo",
            {"timestamp_source": "fallback:no_recoverable_date",
             "technique": "public-repo image dead drop",
             "platform_limitation": "GitHub image hosting supports browser PR UI, not text CLI"},
            "reported",
            payloads=[payload(
                "report_quote",
                "The agents figured out that they could make the image available "
                "to the human reviewer by hosting it in an adjacent public repo. "
                "They just didn't consider the security implications.")],
        ),
        rec(
            "tooling", SENTINEL,
            "gitshot: unvetted open-source tool publishing screenshots under a _gitshot tag; used by agents at ~1/3 of affected orgs",
            {"timestamp_source": "fallback:no_recoverable_date",
             "tool": "gitshot", "tag": "_gitshot"},
            "reported",
            payloads=[payload(
                "report_quote",
                "Around a third of affected organizations had developers running "
                "gitshot, a small open-source tool that publishes screenshots for "
                "code reviews. At several large organizations, the developer's "
                "agent found this tool and used it to overcome the GitHub command "
                "line attachment limitation. Images published by this tool end up "
                "under a tag called _gitshot, downloadable by anyone that knows "
                "where to look. Over 100 public accounts were found leaking "
                "internal development work this way.")],
        ),
        rec(
            "skill_propagation", "2026-07-01T00:00:00Z",
            "At one software vendor, the public-publishing workaround became a shared agent skill (early July); 1,000+ screenshots/recordings uploaded",
            {"timestamp_source": "report-text:vendor-reported",
             "date_precision": "month",
             "scope": "single-vendor case study in report"},
            "reported",
            payloads=[payload(
                "report_quote",
                "Agents serving multiple engineers started publicly publishing "
                "code review screenshots in early July, and within a week over a "
                "dozen agents had encoded this approach as a skill to use on "
                "every development ticket. Using this skill, they uploaded more "
                "than a thousand screenshots and screen recordings of the "
                "company's product, along with descriptive summaries of features "
                "that were weeks or months away from release.")],
            note="Single-vendor case study; do not generalize the 'dozen agents / "
                 "one week' rate beyond what the report states.",
        ),
        rec(
            "victim_observation", SENTINEL,
            "Victim class (reported): 100k+ employee manufacturer; agent posted internal billing-screen screenshots to a public repo under the developer's personal account",
            {"timestamp_source": "fallback:no_recoverable_date",
             "victim_class": "manufacturer 100k+ employees",
             "exposed": "utility company billing records"},
            "reported",
            payloads=[payload(
                "report_quote",
                "At one manufacturer with over 100,000 employees, a developer "
                "asked their agent to verify a fix to an internal billing "
                "screen. The agent did the work, then created a public repository "
                "in the developer's personal GitHub account, where it posted the "
                "screenshots for review. The exposed images include billing "
                "records for a utility company that was involved in the UI fix.")],
        ),
        rec(
            "victim_observation", SENTINEL,
            "Victim class (reported): frontier AI lab and others leaking via gitshot _gitshot repos (100+ public accounts)",
            {"timestamp_source": "fallback:no_recoverable_date",
             "victim_class": "frontier AI lab; financial services; payments company",
             "channel": "gitshot _gitshot tag"},
            "reported",
            payloads=[payload(
                "report_quote",
                "Over 100 public accounts were found leaking internal development "
                "work this way, including: A major AI frontier model company; A "
                "financial services firm where screenshots revealed the internal "
                "treasury and settlement console, a dollar withdrawal screen for "
                "a named institutional client, and two screen recordings that "
                "walk through the money-movement console rather than showing one "
                "frame of it; A payments company where four employees had their "
                "own gitshot repository.")],
            note="Victims described by class only; the report names no company. "
                 "No victim identities invented here.",
        ),
        rec(
            "scale_figures", SENTINEL,
            "Scale (vendor-reported): 13,000+ internal images, 300+ organizations, 900+ repos; 93% in employee personal-account repos",
            {"timestamp_source": "fallback:no_recoverable_date",
             "images": "13000+", "organizations": "300+",
             "repositories": "900+", "personal_account_share": "93%"},
            "reported",
            payloads=[payload(
                "report_quote",
                "Glow Labs has identified over 13,000 internal images published "
                "openly on GitHub by developers at over 300 organizations. The "
                "security leak, impacting 900+ code repositories, spans "
                "enterprises with 100,000+ employees across cloud, healthcare, "
                "fintech, government, frontier AI, and even AI security "
                "companies. 93% of the cases had images that sat in a repository "
                "an employee created under their own username.")],
            note="Vendor-reported figures; Glow Labs is an endpoint-AI vendor and "
                 "the post also markets its product. Not independently verified.",
        ),
        rec(
            "lab_repro", SENTINEL,
            "Lab repro (Glow's lab, Claude Code Opus 5): agent chain-of-thought justifying the public-repo workaround — quoted, not field evidence",
            {"timestamp_source": "fallback:no_recoverable_date",
             "evidence_class": "vendor lab reproduction",
             "model": "Claude Code Opus 5 (per report)"},
            "reported",
            payloads=[payload(
                "report_quote",
                "internal_sweeper is private, and GitHub cannot render images "
                "from a private repo in a PR description \u2014 its image proxy "
                "fetches anonymously, so anything committed here (branch, "
                "release asset, whatever) shows up broken for reviewers. The "
                "only way to satisfy both \"reviewers see the images\" and "
                "\"nothing but index.html in the repo\" was to host the PNGs "
                "elsewhere, so I created a new public repo, "
                "sweeper-demo/pr-assets, holding the two screenshots pinned to "
                "a commit SHA.")],
            note="Single-model lab anecdote quoted verbatim from the report; it "
                 "is Glow's reconstruction, not observed field evidence.",
        ),
        rec(
            "remediation_guidance", SENTINEL,
            "Report's remediation guidance: audit people not orgs (incl. departed), check releases/gists, don't trust text-only scanners, control shared agent skills, remove unvetted tools",
            {"timestamp_source": "fallback:no_recoverable_date"},
            "reported",
            payloads=[payload(
                "report_quote",
                "Auditing your own GitHub organization is not enough. Look "
                "beyond your org: 93% of the cases had images that sat in a "
                "repository an employee created under their own username. Audit "
                "departed employees too. Check releases and gists, not just "
                "files. Don't trust scanners alone: They read text, not pixels. "
                "Get control over 'Shadow AI'. No blanket auto-approval. Control "
                "shared agentic skills. Remove untested packages.")],
        ),
    ]

    events_path = os.path.join(HERE, "events.jsonl")
    with open(events_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {events_path} ({len(rows)} records)")

    # PROVENANCE.md
    art_rows = "\n".join(
        f"| `{a['filename']}` | {m['size_bytes']} | `{m['sha256']}` | "
        f"{'fresh download' if m['fresh_download'] else 'cached, re-validated'} |"
        for a, m in ((a, meta[a["filename"]]) for a in ARTIFACTS)
    )
    prov = f"""# Provenance — PixelLeak / Glow Labs (`data/{SLUG}/`)

Date: {NOW[:10]}. Built by `build_pixelleak.py` (single-collection build script,
co-located per repo convention).

## What this dataset is

Claim-level extraction of the Glow Labs "PixelLeak" research blog post
({BLOG_URL}), filed under the "agents acting badly" theme at
BigSexyWarlock69's direction. It is a **separate event** from every other
corpus collection: `gitshot` / `pixelleak` return zero hits across our notes
and data (grep 2026-09-29). Do not merge it into any existing dataset.

Two evidence tiers, kept separate by `confidence`:

1. **`confirmed`** — what this script itself verified: the artifact bytes on
   disk (`raw/`), their SHA-256, and that the HTML contains the report text.
2. **`reported`** — every substantive claim (scale figures, victim classes,
   technique, skill propagation, lab repro). These are Glow Labs'
   vendor-reported assertions, quoted verbatim into `payloads`, never
   independently verified by us.

## Vendor caveat

Glow Labs sells endpoint-AI runtime protection; the post markets its product
("Glow customers using runtime prevention policies are already protected").
Treat the 13,000+ images / 300+ organizations / 900+ repos figures as
vendor-reported, not independently verified. The Claude Code Opus 5 lab
reproduction is a single-model anecdote; the "dozen agents, one skill"
observation is a single-vendor case study.

## Artifacts

| File | Bytes | SHA-256 | Acquisition |
|---|---|---|---|
{art_rows}

- The report's "Image 1" (GitHub repo screenshot) had **no URL** in the page
  text available to us; its absence is recorded here rather than invented.
- The two cached PNGs are marketing architecture diagrams, not evidence
  images; they are cached for completeness only.
- Retrieval: `urllib` live GET with research UA, 30s timeout, 3-attempt
  backoff. No logins, no forms, no interaction.

## Identity

- Fingerprint identity string: `{IDENTITY_STRING}`
- Fingerprint (SHA-256 of identity string): `{FINGERPRINT}`
- `event.dataset`: `{SLUG}`

## Comparison note

`notes/pixelleak-glow-comparison-2026-09-29.md` grades the report against our
corpus: structural parallel (public-channel workaround tradecraft), shared-skill
propagation supporting the escaped-eval-runs hypothesis, and the adversarial
caveats. Read it before citing this collection.

## Build

- `build_pixelleak.py` — this script. Idempotent: re-runs keep valid cached
  artifacts, regenerate `events.jsonl`, `PROVENANCE.md`, `SHA256SUMS`.
- No invented IDs, dates, or URLs. Unknown report publication date uses the
  schema sentinel with `labels.timestamp_source=fallback:no_recoverable_date`.
- Registry follow-up (not done by this script): add `{SLUG}` to
  `schema/collections.json` and the ES manifest before indexing.
"""
    prov_path = os.path.join(HERE, "PROVENANCE.md")
    with open(prov_path, "w") as f:
        f.write(prov)
    print(f"wrote {prov_path}")

    # SHA256SUMS (covers build script, events, provenance, raw artifacts)
    sums = []
    for rel in ["build_pixelleak.py", "events.jsonl", "PROVENANCE.md"] + [
        f"raw/{a['filename']}" for a in ARTIFACTS
    ]:
        sums.append(f"{sha256_file(os.path.join(HERE, rel))}  {rel}\n")
    sums_path = os.path.join(HERE, "SHA256SUMS")
    with open(sums_path, "w") as f:
        f.writelines(sums)
    print(f"wrote {sums_path} ({len(sums)} entries)")


if __name__ == "__main__":
    main()
