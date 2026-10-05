"""Offline checks for SwarmTraces source validation and ES responses."""
import contextlib
import gzip
import hashlib
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import es_ingest_swarmtraces as loader


class SwarmtracesIngestTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        self.src = root / "redacted.jsonl.gz"
        self.manifest = root / "MANIFEST.json"
        self.mapping = root / "mapping.json"
        self.mapping.write_text(json.dumps({"mappings": {"properties": {}}}))
        for attr, value in (("SRC", str(self.src)), ("MANIFEST", str(self.manifest)),
                            ("MAPPING", str(self.mapping)), ("EXPECTED", 2),
                            ("BATCH", 2)):
            p = patch.object(loader, attr, value)
            p.start()
            self.addCleanup(p.stop)
        self.write_source()

    def write_source(self, ids=("R0000001", "R0000002")):
        with gzip.open(self.src, "wt", encoding="utf-8") as fh:
            for ident in ids:
                fh.write(json.dumps({"id": ident, "kind": "payload",
                                     "text": "sensitive payload"}) + "\n")
        digest = hashlib.sha256(self.src.read_bytes()).hexdigest()
        self.manifest.write_text(json.dumps({"files": [{
            "name": self.src.name, "sha256": digest, "total_records": 2
        }]}))
        p = patch.object(loader, "EXPECTED_SHA256", digest)
        p.start()
        self.addCleanup(p.stop)

    def test_source_validation_precedes_all_bulk_writes(self):
        with patch.object(loader, "req", side_effect=AssertionError("network")):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(loader.check_source(), 2)
            self.src.write_bytes(self.src.read_bytes() + b"x")
            with self.assertRaisesRegex(ValueError, "checksum"):
                loader.cmd_load()

    def test_source_count_and_ids_are_strict(self):
        with patch.object(loader, "req", side_effect=AssertionError("network")):
            self.write_source(ids=("R0000001", "R0000003"))
            with self.assertRaisesRegex(ValueError, "ID"):
                loader.cmd_load()
            self.write_source(ids=("R0000001",))
            with self.assertRaisesRegex(ValueError, "count"):
                loader.cmd_load()

    def test_bulk_ids_are_deterministic_and_failures_raise(self):
        bodies = []

        def successful(method, path, body=None, raw=None):
            bodies.append(raw)
            return 200, {"errors": False, "items": [
                {"index": {"status": 201}}, {"index": {"status": 200}}]}

        with patch.object(loader, "req", side_effect=successful):
            with contextlib.redirect_stdout(io.StringIO()):
                loader.cmd_load()
                loader.cmd_load()
        self.assertEqual(bodies[0], bodies[1])
        self.assertEqual([json.loads(line)["index"]["_id"]
                          for line in bodies[0].splitlines()[::2]],
                         ["R0000001", "R0000002"])
        for response in (
            (503, {}),
            (200, {"items": [{"index": {"status": 201}}]}),
            (200, {"items": [{"index": {"status": 201}},
                             {"index": {"status": 201}}]}),
            (200, {"items": [{"index": {"status": 201}},
                             {"index": {"status": 400, "error": "sensitive payload"}}]}),
            (200, {"errors": True, "items": [{"index": {"status": 201}},
                                              {"index": {"status": 201}}]}),
        ):
            with self.subTest(response=response[0]), \
                 patch.object(loader, "req", return_value=response), \
                 contextlib.redirect_stdout(io.StringIO()), \
                 contextlib.redirect_stderr(io.StringIO()) as err:
                with self.assertRaisesRegex(RuntimeError, "incomplete"):
                    loader.cmd_load()
                self.assertNotIn("sensitive payload", err.getvalue())

    def test_verify_refreshes_before_count_and_rejects_mismatch(self):
        calls = []

        def request(method, path):
            calls.append((method, path))
            return (200, {}) if path.endswith("_refresh") else (200, {"count": 2})

        with patch.object(loader, "req", side_effect=request), \
             contextlib.redirect_stdout(io.StringIO()):
            loader.cmd_verify()
        self.assertEqual(calls, [("POST", "/swarmtraces/_refresh"),
                                 ("GET", "/swarmtraces/_count")])
        with patch.object(loader, "req", side_effect=[
            (200, {}), (200, {"count": 1})]), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "mismatch"):
                loader.cmd_verify()
        with patch.object(loader, "req", return_value=(500, {})):
            with self.assertRaisesRegex(RuntimeError, "refresh"):
                loader.cmd_verify()

    def test_create_and_cli_return_nonzero_on_errors(self):
        with patch.object(loader, "req", return_value=(500, {})):
            self.assertEqual(loader.main(["--create"]), 1)
        with patch.object(loader, "req", side_effect=[
            (404, {}), (200, {"acknowledged": False})]):
            self.assertEqual(loader.main(["--create"]), 1)
        with patch.object(loader, "req", return_value=(200, {})):
            self.assertEqual(loader.main(["--create"]), 1)
        with patch.object(loader, "req", side_effect=[
            (200, {}), (200, {loader.INDEX: {"mappings": {
                "properties": dict(loader.NATIVE_FIELDS, extra={"type": "keyword"})}}})]), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(loader.main(["--create"]), 0)
        with patch.object(loader, "req", side_effect=[
            (200, {}), (200, {loader.INDEX: {"mappings": {
                "properties": {"id": {"type": "text"}}}}})]):
            self.assertEqual(loader.main(["--create"]), 1)
        with patch.object(loader, "req", side_effect=OSError("secret")):
            with contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(loader.main(["--verify"]), 1)
            self.assertNotIn("secret", err.getvalue())
        with patch.object(loader, "req", side_effect=AssertionError("network")):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(loader.main(["--check-source"]), 0)


if __name__ == "__main__":
    unittest.main()
