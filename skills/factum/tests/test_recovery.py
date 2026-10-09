from pathlib import Path
import shutil

import pytest

from factum_lib import schemas
from factum_lib.cli import dispatch, parser
from factum_lib.schemas import SchemaError, install_pack, read_json, write_json_atomic
from factum_lib.store import FactumError, State, add_bundle, digest, export_pending
from tools.validation_support import ROOT


@pytest.fixture
def pack(tmp_path):
    destination = tmp_path / "proposal"
    shutil.copytree(ROOT / "examples/pack/1.0.0", destination)
    return destination


@pytest.mark.parametrize("phase", ["before-lock", "after-lock", "before-rebuild"])
def test_pack_activation_recovery(repo, pack, monkeypatch, phase):
    original = schemas.write_json_atomic
    def interrupted(path, value):
        if phase == "after-lock":
            original(path, value)
        raise OSError("synthetic activation interruption")
    if phase == "before-rebuild":
        monkeypatch.setattr(State, "project", lambda self: (_ for _ in ()).throw(OSError("synthetic rebuild failure")))
    else:
        monkeypatch.setattr(schemas, "write_json_atomic", interrupted)
    with pytest.raises(OSError):
        dispatch(repo, parser().parse_args(["schema", "install", str(pack), "--approve"]))
    assert (repo / "data/schema-packs/factum-example/1.0.0").exists()
    assert ("example.exact" in State(repo).load().catalog.definitions["observable"]) is (phase != "before-lock")
    monkeypatch.undo()
    install_pack(repo, pack, True)
    State(repo).load().project()
    assert "example.exact" in State(repo).load().catalog.definitions["observable"]


def test_pack_changed_during_copy(repo, pack, monkeypatch):
    original = schemas.shutil.copyfile
    def changed(source, target):
        result = original(source, target)
        Path(target).write_bytes(Path(target).read_bytes() + b" ")
        return result
    monkeypatch.setattr(schemas.shutil, "copyfile", changed)
    before = (repo / "data/schema-lock.json").read_bytes()
    with pytest.raises(SchemaError, match="changed during"):
        install_pack(repo, pack, True)
    assert (repo / "data/schema-lock.json").read_bytes() == before
    assert not (repo / "data/schema-packs/factum-example/1.0.0").exists()


@pytest.mark.parametrize("case", ["immutable-id", "receipt", "fingerprint", "count", "orphan-jsonl", "receipt-record-ids"])
def test_portable_corruption_and_semantic_conflicts(state, bundle, case):
    add_bundle(state, bundle)
    export_pending(State(state.repo).load())
    directory = next((state.data / "records").iterdir())
    manifest_path = directory / "manifest.json"
    manifest = read_json(manifest_path)
    raw = (directory / "records.jsonl").read_bytes()
    record = schemas.parse_json(raw)
    if case in {"immutable-id", "receipt"}:
        other = state.data / "records" / ("a" * 32)
        other.mkdir()
        manifest["batch_id"] = other.name
        if case == "immutable-id":
            record["body"]["value"] = "changed"
            record["fingerprint"] = digest({k: v for k, v in record.items() if k != "fingerprint"})
            raw = (schemas.canonical(record) + "\n").encode()
            manifest["records_sha256"] = schemas.sha256(raw)
        else:
            manifest["receipt"]["request_hash"] = "b" * 64
        (other / "records.jsonl").write_bytes(raw)
        write_json_atomic(other / "manifest.json", manifest)
    elif case == "fingerprint":
        record["body"]["value"] = "changed"
        raw = (schemas.canonical(record) + "\n").encode()
        (directory / "records.jsonl").write_bytes(raw)
        manifest["records_sha256"] = schemas.sha256(raw)
        write_json_atomic(manifest_path, manifest)
    elif case == "count":
        manifest["record_count"] += 1
        write_json_atomic(manifest_path, manifest)
    elif case == "receipt-record-ids":
        manifest["receipt"]["result"]["record_ids"] = ["observable_" + "0" * 32]
        write_json_atomic(manifest_path, manifest)
    else:
        (state.data / "records/orphan.jsonl").write_bytes(raw)
    with pytest.raises((FactumError, SchemaError)):
        State(state.repo).load()


def test_normal_validation_never_fetches_network(repo, pack, monkeypatch):
    import socket
    monkeypatch.setattr(socket, "create_connection", lambda *a, **k: pytest.fail("Schema validation attempted network access"))
    schema = pack / "schemas/observation.json"
    document = read_json(schema)
    document["$ref"] = "https://never-fetch.invalid/schema"
    write_json_atomic(schema, document)
    with pytest.raises(SchemaError, match="Uninstalled"):
        install_pack(repo, pack)
