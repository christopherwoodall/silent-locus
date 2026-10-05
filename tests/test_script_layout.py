"""Offline checks for the preserved script layout."""

import ast
import hashlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILDERS = {
    "2026-02-01-agent-convo-venues": "build_dataset.py",
    "2026-05-12-university-shorteners-events": "build_events.py",
    "2026-08-25-commonlog-scan": "build_dataset.py",
    "2026-09-28-nsi-venue-sweep": "build_dataset.py",
    "2026-09-28-open-data-api-venues": "build_dataset.py",
    "2026-09-28-university-shorteners": "build_dataset.py",
    "2026-09-28-university-shorteners-batch2": "build_dataset.py",
    "2026-09-28-university-shorteners-batch3": "build_dataset.py",
    "2026-09-28-worldpoverty-task-family": "build_dataset.py",
    "2026-09-28-yourls-resweep": "build_resweep.py",
}


class ScriptLayoutTests(unittest.TestCase):
    def test_active_tools_remain_at_documented_paths(self):
        for name in (
            "push_to_local_es.py",
            "es_ingest_swarmtraces.py",
            "validate_schema.py",
            "validate_collections.py",
            "verify_checksums.py",
            "gen_dataset_card_table.py",
        ):
            with self.subTest(name=name):
                self.assertTrue((ROOT / "scripts" / name).is_file())

    def test_collection_builders_are_parseable_and_checksummed(self):
        for name, script in BUILDERS.items():
            collection = ROOT / "data" / name
            with self.subTest(collection=name):
                path = collection / script
                self.assertTrue(path.is_file())
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                checksum_lines = (collection / "SHA256SUMS").read_text().splitlines()
                matches = [line[:64] for line in checksum_lines
                           if line.endswith("  " + script)]
                self.assertEqual(
                    matches, [hashlib.sha256(path.read_bytes()).hexdigest()]
                )

    def test_legacy_loaders_not_in_default_ingest_path(self):
        manifest = (ROOT / "scripts" / "local_es_manifest.json").read_text()
        self.assertIn('"via_script": []', manifest)
        self.assertTrue(
            (ROOT / "data/2026-05-17-collusion-wiki/raw/scripts/legacy/es_ingest_wiki.py").is_file()
        )
        self.assertTrue(
            (ROOT / "scripts/archive/es/es_ingest_university_shorteners_consolidated.py").is_file()
        )


if __name__ == "__main__":
    unittest.main()
