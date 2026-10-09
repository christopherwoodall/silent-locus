from pathlib import Path

import pytest

from factum_lib import store
from factum_lib.schemas import SchemaError
from factum_lib.store import FactumError, State, add_bundle, export_pending, initialize


@pytest.mark.parametrize("value", ["Example.COM", "https://Example.COM/Path?Token=AbC#MiXeD", "  leading and trailing  ", "Résumé 東京 e\u0301", "not a URL :// [", "@source", "SYNTHETIC_FAKE_TOKEN_NOT_A_CREDENTIAL", "\r\nline\r\n"])
def test_exact_strings_round_trip(state, bundle, value):
    bundle["records"][0]["body"]["value"] = value
    bundle["records"][0]["tags"] = {"nested": {"literal": "@source", "values": [None, True, 1, value]}}
    result = add_bundle(state, bundle)
    before = State(state.repo).load()
    export_pending(before)
    state.db_path.unlink()
    after = State(state.repo).load()
    after.project()
    assert after.records[result["ids"]["value"]]["body"]["value"] == value
    assert after.records[result["ids"]["value"]]["tags"] == {
        **bundle["records"][0]["tags"],
        store.AUTHOR_TAG: "agent:synthetic",
    }
    after.project()
    assert after.state_digest == before.state_digest


def test_idempotency_survives_export_and_index_loss(state, bundle):
    first = add_bundle(state, bundle)
    assert add_bundle(State(state.repo).load(), bundle)["ids"] == first["ids"]
    export_pending(State(state.repo).load())
    state.db_path.unlink()
    restored = State(state.repo).load()
    restored.project()
    assert add_bundle(restored, bundle)["ids"] == first["ids"]
    bundle["records"][0]["body"]["value"] += "changed"
    with pytest.raises(FactumError, match="test/value"):
        add_bundle(State(state.repo).load(), bundle)


@pytest.mark.parametrize("storage", ["git", "local"])
def test_byte_preservation_cas_and_changed_path(state, bundle, tmp_path, storage):
    source = tmp_path / "binary evidence"
    raw = b"CRLF\r\n\x00\xff" + "東京 e\u0301".encode()
    source.write_bytes(raw)
    bundle["files"] = [{"ref": "file", "path": str(source), "storage": storage}]
    first = add_bundle(state, bundle)
    restored = State(state.repo).load()
    assert restored.artifact_bytes(first["ids"]["file"]) == raw
    bundle["idempotency_key"] += "/second-acquisition"
    second = add_bundle(restored, bundle)
    assert second["ids"]["file"] != first["ids"]["file"]
    root = state.data if storage == "git" else state.local
    assert len(list((root / "blobs").rglob("*" + restored.records[first["ids"]["file"]]["body"]["sha256"]))) == 1
    source.write_bytes(raw + b"changed")
    with pytest.raises(FactumError):
        add_bundle(State(state.repo).load(), bundle)
    assert len(State(state.repo).load().records) == 4


def test_rejected_bundle_leaves_only_understood_orphan_bytes(state, bundle, tmp_path):
    path = tmp_path / "synthetic"
    path.write_bytes(b"synthetic orphan")
    bundle["files"] = [{"ref": "file", "path": str(path), "storage": "git"}]
    bundle["records"].append({"kind": "observable", "body": {"type": "unknown", "value": "x"}})
    with pytest.raises(SchemaError):
        add_bundle(state, bundle)
    restored = State(state.repo).load()
    assert not restored.records and not restored.pending and not restored.receipts
    assert any((state.data / "blobs/sha256").rglob("*"))


@pytest.mark.parametrize("phase", ["before-pending", "after-pending", "database-replace", "after-batch"])
def test_failure_recovery(state, bundle, monkeypatch, phase):
    if phase in {"before-pending", "after-pending"}:
        original = store.write_json_atomic
        def interrupted(path, value):
            if "pending" in Path(path).parts:
                if phase == "after-pending":
                    original(path, value)
                raise OSError("synthetic failure")
            return original(path, value)
        monkeypatch.setattr(store, "write_json_atomic", interrupted)
    elif phase == "database-replace":
        original = store.os.replace
        def interrupted(source, destination):
            if Path(destination) == state.db_path:
                raise OSError("synthetic replacement failure")
            return original(source, destination)
        monkeypatch.setattr(store.os, "replace", interrupted)
    else:
        add_bundle(state, bundle)
        original = Path.unlink
        def interrupted(path, *args, **kwargs):
            if "pending" in path.parts:
                raise OSError("synthetic pending cleanup failure")
            return original(path, *args, **kwargs)
        monkeypatch.setattr(Path, "unlink", interrupted)
    old_db = state.db_path.read_bytes()
    with pytest.raises(OSError):
        if phase == "after-batch":
            export_pending(State(state.repo).load())
        else:
            add_bundle(state, bundle)
    assert state.db_path.read_bytes() == old_db
    monkeypatch.undo()
    recovered = State(state.repo).load()
    assert len(recovered.records) == (0 if phase == "before-pending" else 1)
    recovered.project()
    retried = add_bundle(State(state.repo).load(), bundle)
    assert retried.get("replayed", False) is (phase != "before-pending")
    export_pending(State(state.repo).load())
    assert export_pending(State(state.repo).load())["exported"] == []
    assert len(State(state.repo).load().records) == 1


def test_rebuild_restores_exported_and_pending(state, bundle):
    add_bundle(state, bundle)
    export_pending(State(state.repo).load())
    bundle["idempotency_key"] += "/pending"
    add_bundle(State(state.repo).load(), bundle)
    expected = State(state.repo).load()
    state.db_path.unlink()
    recovered = State(state.repo).load()
    recovered.project()
    assert recovered.records == expected.records
    assert recovered.state_digest == expected.state_digest
    assert len(recovered.pending) == 1


@pytest.mark.parametrize("filename", [".gitignore", ".gitattributes"])
def test_init_preserves_existing_git_file_bytes(repo, filename):
    path = repo / filename
    original = b"# user content\r\nuser-rule\r\n"
    path.write_bytes(original)
    initialize(repo)
    assert path.read_bytes().startswith(original)
    identity = (repo / "data/corpus.json").read_bytes()
    lock = (repo / "data/schema-lock.json").read_bytes()
    initialize(repo)
    assert (repo / "data/corpus.json").read_bytes() == identity
    assert (repo / "data/schema-lock.json").read_bytes() == lock


@pytest.mark.parametrize("target", ["data", "data/.local", "data/blobs", "data/.local/pending", "data/records"])
def test_managed_ancestor_symlink_is_rejected(repo, bundle, tmp_path, target):
    import shutil
    path = repo / target
    outside = tmp_path / "outside"
    if path.exists():
        shutil.copytree(path, outside)
        shutil.rmtree(path)
    else:
        outside.mkdir()
        path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(outside, target_is_directory=True)
    before = sorted(p.relative_to(outside).as_posix() for p in outside.rglob("*"))
    with pytest.raises((FactumError, SchemaError)):
        state = State(repo).load()
        add_bundle(state, bundle)
        export_pending(State(repo).load())
    assert sorted(p.relative_to(outside).as_posix() for p in outside.rglob("*")) == before


def test_hash_mismatch_and_metadata_reference(state, bundle, tmp_path):
    source = tmp_path / "file"
    source.write_bytes(b"synthetic")
    bundle["files"] = [{"ref": "file", "path": str(source), "storage": "git"}]
    bundle["records"].append({"ref": "reference", "kind": "artifact", "body": {"reference": {"uri": "synthetic:reference"}}})
    result = add_bundle(state, bundle)
    current = State(state.repo).load()
    assert current.verify_blobs()["verified_hashes"] == 1
    with pytest.raises(FactumError, match=result["ids"]["reference"]):
        current.artifact_bytes(result["ids"]["reference"])
    value = current.records[result["ids"]["file"]]["body"]["sha256"]
    path = state.data / "blobs/sha256" / value[:2] / value
    path.write_bytes(b"corrupt")
    with pytest.raises(FactumError):
        current.verify_blobs()


def test_retraction_preserves_target(state, bundle):
    original = add_bundle(state, bundle)["ids"]["value"]
    bundle["idempotency_key"] += "/retract"
    bundle["records"] = [{"kind": "retraction", "body": {"target": original, "reason": "synthetic withdrawal"}}]
    add_bundle(State(state.repo).load(), bundle)
    assert original in State(state.repo).load().records
