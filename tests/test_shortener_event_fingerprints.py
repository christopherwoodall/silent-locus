"""Offline invariants for the canonical shortener event slice."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data/2026-05-12-university-shorteners-events/events.jsonl"
BUILDER = ROOT / "scripts/build_shortener_events.py"
sys.path.insert(0, str(ROOT / "scripts"))
from validate_schema import check  # noqa: E402


class ShortenerEventFingerprints(unittest.TestCase):
    def test_unique_ids_fingerprints_and_schema(self):
        seen = set()
        normalized_empty_labels = []
        with EVENTS.open(encoding="utf-8") as stream:
            rows = list(stream)
        self.assertEqual(len(rows), 1591)
        for number, row in enumerate(rows, 1):
            with self.subTest(row=number):
                doc = json.loads(row)
                event_id = doc["labels"]["event_id"]
                self.assertNotIn(event_id, seen)
                seen.add(event_id)
                self.assertEqual(
                    doc["fingerprint"], hashlib.sha256(event_id.encode("utf-8")).hexdigest()
                )
                errors = check(doc, f"{EVENTS}:{number}")
                self.assertEqual(errors, [])
                if number > 1522 and doc["labels"].get("best_day") == "{}":
                    normalized_empty_labels.append(number)
        self.assertEqual(
            normalized_empty_labels, list(range(1567, 1580)) + list(range(1588, 1592))
        )

    def test_builder_refuses_canonical_overwrite(self):
        before = hashlib.sha256(EVENTS.read_bytes()).hexdigest()
        for args in ([], ["--output", str(EVENTS)]):
            with self.subTest(args=args):
                result = subprocess.run(
                    [sys.executable, str(BUILDER), *args],
                    cwd=ROOT, capture_output=True, text=True, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
        self.assertEqual(hashlib.sha256(EVENTS.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
