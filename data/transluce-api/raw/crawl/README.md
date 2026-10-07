# raw/crawl/ — saved web pages from Transluce findings

We saved web pages from Transluce evidence links on 2026-10-07.
We used curl. Each file is one saved page.

Results: 126 pages saved, 9 failed, 4 skipped (we already had them).
File names use this form: f<finding-id>_<seq>.<ext>.
Example: f153_012.html is the 12th page from finding 153.

Read MANIFEST.jsonl first. A manifest is a list of files.
It maps each file name to its source URL, save time, and sha256.
A sha256 is a file fingerprint.
Some names have odd endings (example: f168_126.119 for an rdap lookup).
The endings copy the MANIFEST filename field exactly.
Trust MANIFEST, not the file ending.
We collected the pages with ../crawl_urls.py. See ../PROVENANCE.md.
