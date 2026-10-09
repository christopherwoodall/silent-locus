import copy
import json
import shutil

import pytest

from factum_lib.cli import dispatch, parser
from factum_lib.schemas import SchemaError, install_pack, read_json, write_json_atomic
from factum_lib.store import FactumError, State, add_bundle, digest, export_pending
from tools.validation_support import ROOT, cli, git, install_skill, run, snapshot


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    return snapshot(tmp_path_factory.mktemp("distributed-source"))


@pytest.fixture
def sites(tmp_path, staged):
    a = tmp_path / "site-a"
    a.mkdir()
    git(a, "init", "-q", "-b", "main")
    skill_a = install_skill(a, *staged)
    cli(skill_a, a, "init")
    dispatch(a, parser().parse_args(["lane", "new", "Shared synthetic lane"]))
    git(a, "add", "--all")
    git(a, "commit", "-qm", "Synthetic shared base")
    b = tmp_path / "site-b"
    run(["git", "clone", "-q", a, b])
    skill_b = install_skill(b, *staged)
    cli(skill_b, b, "init")
    return a, b, skill_a, skill_b


def seal(host, message):
    export_pending(State(host).load())
    git(host, "add", "--all")
    git(host, "commit", "-qm", message)


def merge(a, b):
    git(b, "fetch", "-q", "origin")
    return git(b, "merge", "--no-edit", "origin/main", check=False)


def test_clean_git_merge_still_rejects_conflicting_receipts(sites, bundle):
    a, b, _, skill_b = sites
    add_bundle(State(a).load(), bundle)
    changed = copy.deepcopy(bundle)
    changed["records"][0]["body"]["value"] = "Different.Example"
    add_bundle(State(b).load(), changed)
    seal(a, "Synthetic incompatible A receipt")
    seal(b, "Synthetic incompatible B receipt")
    assert merge(a, b).returncode == 0
    assert cli(skill_b, b, "verify", ok=False)["error"]["code"] == "IDEMPOTENCY_CONFLICT"


def test_clean_git_merge_rejects_same_immutable_id(sites, bundle):
    a, b, _, skill_b = sites
    add_bundle(State(a).load(), bundle)
    seal(a, "Synthetic original immutable record")
    # Deliberately adversarial ledger fixture, not a normal ingestion path.
    directory = next((a / "data/records").iterdir())
    destination = b / "data/records" / ("b" * 32)
    destination.mkdir(parents=True)
    record = json.loads((directory / "records.jsonl").read_bytes())
    record["body"]["value"] = "Conflict.Example"
    record["fingerprint"] = digest({k: v for k, v in record.items() if k != "fingerprint"})
    raw = (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    manifest = read_json(directory / "manifest.json")
    manifest["batch_id"] = destination.name
    manifest["records_sha256"] = __import__("hashlib").sha256(raw).hexdigest()
    manifest["receipt"]["key"] = "adversarial/different-key"
    manifest["receipt"]["result"]["batch_id"] = destination.name
    (destination / "records.jsonl").write_bytes(raw)
    write_json_atomic(destination / "manifest.json", manifest)
    git(b, "add", "--all")
    git(b, "commit", "-qm", "Synthetic conflicting immutable record")
    assert merge(a, b).returncode == 0
    assert cli(skill_b, b, "verify", ok=False)["error"]["code"] == "IMMUTABLE_CONFLICT"


@pytest.mark.parametrize("duplicate", ["schema", "type"])
def test_schema_merge_requires_semantic_validation(sites, tmp_path, duplicate):
    a, b, _, skill_b = sites
    for host, name in [(a, "extension-a"), (b, "extension-b")]:
        proposal = tmp_path / name
        shutil.copytree(ROOT / "examples/pack/1.0.0", proposal)
        manifest = read_json(proposal / "pack.json")
        manifest["name"] = name
        write_json_atomic(proposal / "pack.json", manifest)
        if duplicate == "type":
            definitions = read_json(proposal / "definitions.json")
            for definition in definitions["definitions"]:
                if "schema" in definition:
                    definition["schema"] += "-" + name
            write_json_atomic(proposal / "definitions.json", definitions)
            for path in (proposal / "schemas").glob("*.json"):
                schema = read_json(path)
                schema["$id"] += "-" + name
                write_json_atomic(path, schema)
        install_pack(host, proposal, True)
        git(host, "add", "--all")
        git(host, "commit", "-qm", "Synthetic conflicting extension")
    result = merge(a, b)
    assert result.returncode != 0 and "CONFLICT" in result.stdout
    # Resolve only the textual lock conflict by combining both entries.
    # Semantic verification must reject this apparently complete union.
    lock = read_json(a / "data/schema-lock.json")
    entry_b = next(e for e in json.loads(git(b, "show", "HEAD:data/schema-lock.json").stdout)["packs"] if e["name"] == "extension-b")
    lock["packs"].append(entry_b)
    write_json_atomic(b / "data/schema-lock.json", lock)
    result = cli(skill_b, b, "verify", ok=False)
    assert result["error"]["code"] == "SCHEMA"
    assert ("Duplicate schema ID" if duplicate == "schema" else "Duplicate type assignment") in result["error"]["message"]


def test_mutable_lane_edits_remain_git_conflicts(sites):
    a, b, _, _ = sites
    for host, title in [(a, "Synthetic A title"), (b, "Synthetic B title")]:
        state = State(host).load()
        lane_id = next(iter(state.lanes))
        dispatch(host, parser().parse_args(["lane", "edit", lane_id, "--title", title]))
        git(host, "add", "--all")
        git(host, "commit", "-qm", "Synthetic divergent lane edit")
    result = merge(a, b)
    assert result.returncode != 0 and "CONFLICT" in result.stdout
    with pytest.raises((ValueError, SchemaError)):
        State(b).load()
