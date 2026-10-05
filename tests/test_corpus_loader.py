"""Offline checks for strict registered-corpus ingestion."""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import push_to_local_es as loader


class CorpusLoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.name = "test-index"
        folder = self.root / "data" / self.name
        folder.mkdir(parents=True)
        self.events = folder / "events.jsonl"
        self.mapping = {"mappings": {"properties": {
            "event": {"properties": {"dataset": {"type": "keyword"}}}}}}
        (self.root / "mapping.json").write_text(json.dumps(self.mapping))
        (self.root / "manifest.json").write_text(json.dumps({"mapping": "mapping.json", "via_script": []}))
        (self.root / "registry.json").write_text(json.dumps({"collections": [
            {"name": self.name, "index": self.name}]}))
        for key, value in (("BASE", str(self.root)), ("MANIFEST", str(self.root / "manifest.json")),
                           ("REGISTRY", str(self.root / "registry.json"))):
            p = patch.object(loader, key, value)
            p.start()
            self.addCleanup(p.stop)
        self.write([{"event": {"dataset": self.name}, "value": 1}])

    def write(self, docs):
        self.events.write_text("".join(json.dumps(d) + "\n" for d in docs))

    def run_cli(self, args, request):
        with patch.object(sys, "argv", ["loader", *args]), \
             patch.object(loader, "ping", return_value=(True, "8.0")), \
             patch.object(loader, "es_req", side_effect=request), \
             patch.object(loader, "head_status", return_value=404), \
             contextlib.redirect_stdout(io.StringIO()) as out:
            try:
                loader.main()
                code = 0
            except SystemExit as exc:
                code = exc.code
            return code, out.getvalue()

    def test_expected_distinct_ids_include_explicit_and_canonical(self):
        a = {"event": {"dataset": self.name}, "value": 1}
        b = {"value": 1, "event": {"dataset": self.name}}
        self.write([a, b, {"event": {"dataset": self.name}, "_id": "fixed"},
                    {"event": {"dataset": self.name}, "_id": "fixed"}])
        self.assertEqual(loader.expected_counts(self.name, [f"data/{self.name}/events.jsonl"]), (4, 2))
        self.assertEqual(loader.doc_id(a), loader.doc_id(b))
        self.assertEqual(loader.doc_id({"event": {"dataset": self.name}, "_id": "fixed"}), "fixed")
        self.write([{"event": {"dataset": self.name}, "_id": 7}])
        with self.assertRaisesRegex(ValueError, "invalid staged document"):
            loader.expected_counts(self.name, [f"data/{self.name}/events.jsonl"])

    def test_bulk_response_rejects_missing_items_errors_and_failed_status(self):
        buf = [json.dumps({"index": {"_index": self.name, "_id": "a"}}), '{"value":1}']
        for response in ({}, {"items": []}, {"errors": True, "items": [
                {"index": {"_index": self.name, "_id": "a", "status": 201}}]},
                {"errors": False, "items": [{"index": {
                    "_index": self.name, "_id": "a", "status": 400, "error": {"secret": "do not print"}}}]}):
            with self.subTest(response=response), patch.object(loader, "es_req", return_value=(200, response)):
                with self.assertRaises(RuntimeError):
                    loader.send_batch("", None, self.name, buf)
        with patch.object(loader, "es_req", return_value=(503, {"secret": "do not print"})):
            with self.assertRaisesRegex(RuntimeError, "HTTP 503"):
                loader.send_batch("", None, self.name, buf)

    def test_existing_mapping_preflight_rejects_conflict_without_writes(self):
        with patch.object(loader, "head_status", return_value=200), \
             patch.object(loader, "es_req", return_value=(200, {self.name: {
                 "mappings": {"properties": {"event": {"properties": {
                     "dataset": {"type": "text"}}}}}}})) as req:
            with self.assertRaisesRegex(RuntimeError, "incompatible"):
                loader.ensure_index("", None, self.name, "mapping.json")
            self.assertEqual([call.args[1] for call in req.call_args_list], ["GET"])
        self.assertTrue(loader.mapping_compatible(
            self.mapping["mappings"], {"properties": {
                "event": {"properties": {"dataset": {"type": "keyword"}}},
                "extra": {"type": "keyword"}}}))

    def test_verify_is_read_only_and_detects_mismatch(self):
        self.write([{"event": {"dataset": self.name}, "value": 1}] * 2)
        calls = []

        def request(es, method, path, **kwargs):
            calls.append((method, path))
            return 200, {"count": 1}

        code, output = self.run_cli(["--all", "--verify"], request)
        self.assertEqual(code, 0)
        self.assertIn("expected=1", output)
        self.assertEqual(calls, [("GET", f"/{self.name}/_count")])
        calls.clear()

        def mismatch(es, method, path, **kwargs):
            calls.append((method, path))
            return 200, {"count": 2}

        code, output = self.run_cli(["--index", self.name, "--verify"], mismatch)
        self.assertEqual(code, 1)
        self.assertIn("COUNT MISMATCH", output)
        self.assertEqual(calls, [("GET", f"/{self.name}/_count")])

    def test_load_refreshes_before_count_and_fails_closed(self):
        methods = []

        def request(es, method, path, **kwargs):
            methods.append((method, path))
            if path == "/_bulk?refresh=false":
                raw = kwargs["raw"].splitlines()
                ident = json.loads(raw[0])["index"]["_id"]
                return 200, {"errors": False, "items": [{"index": {
                    "_index": self.name, "_id": ident, "status": 201}}]}
            if path.endswith("/_count"):
                return 200, {"count": 1}
            return 200, {}

        code, _ = self.run_cli(["--index", self.name], request)
        self.assertEqual(code, 0)
        self.assertEqual(methods, [("PUT", f"/{self.name}"), ("POST", "/_bulk?refresh=false"),
                                   ("POST", f"/{self.name}/_refresh"), ("GET", f"/{self.name}/_count")])
        for broken_path in (f"/{self.name}", "/_bulk?refresh=false",
                            f"/{self.name}/_refresh", f"/{self.name}/_count"):
            methods.clear()

            def fail(es, method, path, **kwargs):
                if path == broken_path:
                    return 503, {"secret": "do not print"}
                return request(es, method, path, **kwargs)

            code, output = self.run_cli(["--index", self.name], fail)
            self.assertEqual(code, 1)
            self.assertIn("FAILED", output)
            self.assertNotIn("secret", output)


if __name__ == "__main__":
    unittest.main()
