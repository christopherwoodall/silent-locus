from pathlib import Path

import pytest

from factum_lib import schemas, store
from factum_lib.cli import dispatch, parser
from factum_lib.schemas import SchemaError, read_json, write_json_atomic
from factum_lib.store import FactumError, State, add_bundle, initialize


def invoke(repo, *args):
    return dispatch(repo, parser().parse_args(args))


def test_verification_checks_each_acquisition_size(state, bundle, tmp_path):
    path = tmp_path / "file"
    path.write_bytes(b"same synthetic bytes")
    bundle["files"] = [{"ref": "file", "path": str(path), "storage": "git"}]
    add_bundle(state, bundle)
    bundle["idempotency_key"] += "/again"
    second = add_bundle(State(state.repo).load(), bundle)
    current = State(state.repo).load()
    current.records[second["ids"]["file"]]["body"]["size"] += 1
    with pytest.raises(FactumError):
        current.verify_blobs()


def test_atomic_publication_syncs_new_directory_ancestors(tmp_path, monkeypatch):
    synced = []
    monkeypatch.setattr(schemas, "sync_directory", lambda path: synced.append(Path(path)))
    target = tmp_path / "new" / "pending" / "record.json"
    schemas.write_json_atomic(target, {"synthetic": True})
    assert tmp_path in synced
    assert target.parent.parent in synced
    assert target.parent in synced
    assert read_json(target) == {"synthetic": True}


def test_schema_error_does_not_echo_submitted_payload(state, bundle):
    token = "SYNTHETIC_FAKE_TOKEN_NOT_A_CREDENTIAL"
    bundle["records"][0]["body"]["value"] = {"synthetic_token": token}
    with pytest.raises(SchemaError) as error:
        add_bundle(state, bundle)
    assert token not in str(error.value)


@pytest.mark.parametrize("case", ["no-basis", "no-cites"])
def test_interpretive_edges_require_provenance(state, bundle, case):
    bundle["records"].append({
        "kind": "edge",
        "body": {"subject": "@value", "object": "@value", "predicate": "related_to", "basis": "INFERENCE", "cites": []},
    })
    if case == "no-basis":
        del bundle["records"][-1]["body"]["basis"]
    with pytest.raises(SchemaError):
        add_bundle(state, bundle)
    assert not State(state.repo).load().records


def test_high_degree_graph_reports_limits(state, bundle):
    bundle["records"] = [
        {"ref": f"v{i}", "kind": "observable", "body": {"type": "text", "value": str(i)}}
        for i in range(30)
    ] + [
        {"kind": "edge", "body": {"subject": "@v0", "object": f"@v{i}", "predicate": "part_of"}}
        for i in range(1, 30)
    ]
    result = add_bundle(state, bundle)
    graph = invoke(state.repo, "graph", result["ids"]["v0"], "--limit", "3")
    assert graph["truncated"]
    assert len(graph["edges"]) == 3
    assert len(graph["nodes"]) <= 4


@pytest.mark.parametrize("failure", ["missing-fts", "disk-full", "permission"])
def test_projection_failures_leave_prior_database(state, bundle, monkeypatch, failure):
    original = store.sqlite3.connect
    class BrokenDatabase:
        def __init__(self, path):
            self.db = original(path)
        def executescript(self, sql):
            if failure == "missing-fts":
                raise store.sqlite3.OperationalError("synthetic: no such tokenizer: trigram")
            raise OSError("synthetic disk full" if failure == "disk-full" else "synthetic permission denied")
        def close(self):
            self.db.close()
    monkeypatch.setattr(store.sqlite3, "connect", BrokenDatabase)
    prior = state.db_path.read_bytes()
    with pytest.raises((store.sqlite3.OperationalError, OSError)):
        add_bundle(state, bundle)
    assert state.db_path.read_bytes() == prior
    monkeypatch.undo()
    recovered = State(state.repo).load()
    assert len(recovered.records) == 1 and len(recovered.pending) == 1
    recovered.project()


def test_general_locator_ingestion_is_not_quote_verification(repo, tmp_path):
    path = tmp_path / "file"
    path.write_bytes(b"exact synthetic text")
    capture = invoke(repo, "capture", "--url", "synthetic:locator", "--file", str(path), "--storage", "git", "--actor", "agent:synthetic", "--key", "locator/capture")
    bundle = {
        "bundle": 2, "actor": "agent:synthetic", "idempotency_key": "locator/sighting",
        "records": [
            {"ref": "v", "kind": "observable", "body": {"type": "text", "value": "invented quote"}},
            {"ref": "s", "kind": "sighting", "body": {
                "observable": "@v", "observation": capture["ids"]["observation"],
                "locator": {"artifact": capture["ids"]["file0"], "text_pos": {"start": 0, "end": 5}, "quote": {"exact": "invented quote"}},
            }},
        ],
    }
    result = add_bundle(State(repo).load(), bundle)
    with pytest.raises(FactumError, match="Quote differs"):
        invoke(repo, "get", result["ids"]["s"], "--context", "0")


def test_partial_initialization_requires_inspection(tmp_path):
    from tools.validation_support import git
    repo = tmp_path / "partial"
    repo.mkdir()
    git(repo, "init", "-q")
    existing = repo / "data/schema-packs"
    existing.mkdir(parents=True)
    (existing / "unrelated").write_bytes(b"unrelated")
    with pytest.raises(FactumError, match="Inspect"):
        initialize(repo)
    assert (existing / "unrelated").read_bytes() == b"unrelated"


@pytest.mark.parametrize("kind", ["observation", "event"])
@pytest.mark.parametrize("assignment", ["matching", "conflicting"])
def test_explicit_payload_schema_assignment(repo, tmp_path, kind, assignment):
    from tools.validation_support import ROOT
    schemas.install_pack(repo, ROOT / "examples/pack/1.0.0", True)
    bundle = read_json(ROOT / "examples/bundle.json")
    bundle["files"][0]["path"] = str(ROOT / "examples/capture.txt")
    record = next(r for r in bundle["records"] if r["kind"] == kind)
    record["body"]["data_schema"] = ("urn:factum:example:capture:1" if kind == "observation" else "urn:factum:example:event:1") if assignment == "matching" else "urn:factum:core:empty:1"
    if assignment == "conflicting":
        with pytest.raises(SchemaError):
            add_bundle(State(repo).load(), bundle)
    else:
        add_bundle(State(repo).load(), bundle)


def test_reference_traversal_allof_arrays_and_local_pointer(repo, tmp_path):
    import shutil
    from tools.validation_support import ROOT
    pack = tmp_path / "proposal"
    shutil.copytree(ROOT / "examples/pack/1.0.0", pack)
    path = pack / "schemas/observation.json"
    schema = read_json(path)
    schema["$defs"] = {"artifact": {"$ref": "urn:factum:core:common:1#/$defs/id", "x-factum-target-kinds": ["artifact"]}}
    schema["properties"]["refs"] = {
        "type": "array", "prefixItems": [{"$ref": "#/$defs/artifact"}],
        "items": {"allOf": [{"$ref": "#/$defs/artifact"}]},
    }
    write_json_atomic(path, schema)
    schemas.install_pack(repo, pack, True)
    bundle = read_json(ROOT / "examples/bundle.json")
    bundle["files"][0]["path"] = str(ROOT / "examples/capture.txt")
    bundle["records"][1]["body"]["data"]["refs"] = ["@file", "@file"]
    result = add_bundle(State(repo).load(), bundle)
    current = State(repo).load()
    assert current.records[result["ids"]["observation"]]["body"]["data"]["refs"] == [result["ids"]["file"]] * 2


def test_query_filters_and_rejects_unsupported_constraints(state, bundle, tmp_path):
    bundle["records"][0]["tags"] = {"nested": {"literal": "@source"}}
    add_bundle(state, bundle)
    path = tmp_path / "query.json"
    write_json_atomic(path, {"kind": "observable", "tags": {"nested": {"literal": "@source"}}, "count": True})
    assert invoke(state.repo, "query", "--input", str(path))["count"] == 1
    write_json_atomic(path, {"kind": "observable", "where": "unsupported"})
    with pytest.raises(FactumError):
        invoke(state.repo, "query", "--input", str(path))


def test_path_helpers_use_packaged_assets_and_shared_resolution(repo):
    from factum_lib.paths import assets_root, resolve_repository
    assert (assets_root() / "packs/factum-core/1.0.0/pack.json").is_file()
    assert resolve_repository(repo) == repo


def test_documentation_links_resolve():
    import re
    from tools.validation_support import ROOT
    paths = [ROOT / name for name in ("README.md", "INSTALL.md", "SKILL.md", "AGENTS.md", "ARCHITECTURE.md", "references/data-contract.md", "docs/HANDOFF.md", "docs/VALIDATION.md")]
    for path in paths:
        for target in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)", path.read_text()):
            assert (path.parent / target).is_file(), (path.name, target)
