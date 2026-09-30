"""Offline regression checks for registry-driven staged ingest."""
import contextlib
import io
import json
import os
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import push_to_local_es as loader


class CanonicalIngestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.patch_base = patch.object(loader, "BASE", str(self.root))
        self.patch_base.start()
        self.addCleanup(self.patch_base.stop)
        self.name = "2026-09-28-example"
        self.folder = self.root / "data" / self.name
        self.folder.mkdir(parents=True)
        self.registry = {"collections": [
            {"name": self.name, "index": self.name},
            {"name": "2026-09-28-virtual", "index": self.name, "virtual": True},
        ]}

    def write(self, filename, datasets):
        path = self.folder / filename
        path.write_text("".join(json.dumps({"event": {"dataset": ds}})
                                + "\n" for ds in datasets))
        return path

    def test_registered_event_and_rollup_are_discovered(self):
        self.write("events.jsonl", [self.name] * 2)
        self.write("rollup.jsonl", [self.name + "-rollup"])
        self.assertEqual(loader.discover_staged(self.registry), {
            self.name: [f"data/{self.name}/events.jsonl"],
            self.name + "-rollup": [f"data/{self.name}/rollup.jsonl"],
        })

    def test_virtual_override_and_unregistered_are_not_auto_loaded(self):
        self.registry["collections"][0]["index"] = "2026-09-28-shared"
        self.write("events.jsonl", ["2026-09-28-shared"])
        other = self.root / "data" / "2026-09-28-unregistered"
        other.mkdir()
        (other / "events.jsonl").write_text('{"event":{"dataset":"unregistered"}}\n')
        self.assertEqual(loader.discover_staged(self.registry),
                         {"2026-09-28-shared": [f"data/{self.name}/events.jsonl"]})

    def test_mixed_or_wrong_dataset_is_rejected_before_bulk(self):
        path = self.write("events.jsonl", [self.name, "2026-09-28-other"])
        with self.assertRaisesRegex(ValueError, "mixed event.dataset"):
            loader.discover_staged(self.registry)
        with patch.object(loader, "send_batch", side_effect=AssertionError("network")):
            with self.assertRaisesRegex(ValueError, "mixed event.dataset"):
                loader.bulk_load("", None, self.name,
                                 [os.path.relpath(path, self.root)])
        self.write("events.jsonl", ["2026-09-28-other"])
        with self.assertRaisesRegex(ValueError, "registered"):
            loader.discover_staged(self.registry)

    def test_invalid_and_empty_files_are_rejected(self):
        path = self.folder / "events.jsonl"
        for payload in ('{"event":{}}\n', '{broken}\n', '\n'):
            path.write_text(payload)
            with self.assertRaises(ValueError):
                loader.discover_staged(self.registry)

    def test_cli_requires_selection_and_dry_run_never_pings(self):
        registry_path = self.root / "registry.json"
        manifest_path = self.root / "manifest.json"
        registry_path.write_text(json.dumps(self.registry))
        manifest_path.write_text(json.dumps({"mapping": "mapping.json",
                                             "via_script": []}))
        self.write("events.jsonl", [self.name])
        with patch.object(loader, "REGISTRY", str(registry_path)), \
             patch.object(loader, "MANIFEST", str(manifest_path)), \
             patch.object(loader, "ping", side_effect=AssertionError("ping")), \
             patch.object(loader, "es_req", side_effect=AssertionError("request")), \
             patch.object(loader, "head_status", side_effect=AssertionError("head")):
            with patch.object(sys, "argv", ["loader"]):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as cm:
                        loader.main()
                self.assertEqual(cm.exception.code, 2)
            with patch.object(sys, "argv", ["loader", "--dry-run"]):
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    loader.main()
                self.assertIn(self.name, out.getvalue())
            manifest_path.write_text(json.dumps({
                "mapping": "mapping.json",
                "via_script": [{"index": self.name, "scripts": ["builder.py"]}]}))
            with patch.object(sys, "argv", ["loader", "--dry-run"]):
                with contextlib.redirect_stderr(io.StringIO()) as err:
                    with self.assertRaises(SystemExit) as cm:
                        loader.main()
                self.assertEqual(cm.exception.code, 2)
                self.assertIn("overlap", err.getvalue())


if __name__ == "__main__":
    unittest.main()
