#!/usr/bin/env python3
"""Real external-host acceptance test. Uses synthetic evidence and local Git only."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

# This is tooling, not an alternative runtime entry point.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.validation_support import cli, git, hashes, install_skill, run, snapshot


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def commit(host, message):
    git(host, "add", "--all")
    assert not git(host, "ls-files", ".agents/skills/factum").stdout
    git(host, "commit", "-qm", message)
    return git(host, "rev-parse", "HEAD").stdout.strip()


def capture(skill, host, fixture, key, storage="git"):
    return cli(
        skill, host, "capture", "--url", "https://Example.COM/CasePath?Token=AbC#MiXeD",
        "--file", fixture, "--storage", storage, "--actor", "agent:synthetic",
        "--key", key, "--tags", '{"synthetic":true,"literal":"@source"}',
    )


def add_value(skill, host, fixtures, key, value):
    path = fixtures / (key.replace("/", "-") + ".json")
    write_json(path, {
        "bundle": 2, "actor": "agent:synthetic", "idempotency_key": key,
        "records": [{"ref": "value", "kind": "observable", "body": {"type": "domain", "value": value}, "tags": {}}],
    })
    return cli(skill, host, "add", "--input", path)


def writer_lock(skill, host, fixture):
    env = os.environ.copy()
    env.pop("FACTUM_REPO", None)
    env.pop("PYTHONPATH", None)
    processes = [
        subprocess.Popen(
            ["uv", "run", "--no-project", "--python", os.environ.get("FACTUM_TEST_PYTHON", "3.12"),
             str(skill / "scripts/factum.py"), "--repo", str(host), "add", "--input", str(fixture)],
            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ) for _ in range(2)
    ]
    results = []
    for process in processes:
        stdout, stderr = process.communicate(timeout=90)
        assert process.returncode == 0, stderr
        results.append(json.loads(stdout))
    assert results[0]["ids"] == results[1]["ids"]
    assert sum(bool(r.get("replayed")) for r in results) == 1


def submodule_scenario(workspace, source):
    host = workspace / "submodule host"
    host.mkdir()
    git(host, "init", "-q", "-b", "main")
    # File transport is enabled only for these disposable local operations.
    run(["git", "-C", host, "-c", "protocol.file.allow=always", "submodule", "add", "-q", source, ".agents/skills/factum"])
    skill = host / ".agents/skills/factum"
    cli(skill, host, "init", cwd=skill, explicit=False)
    git(host, "add", "--all")
    git(host, "commit", "-qm", "Synthetic pinned submodule")
    clone = workspace / "submodule replica"
    run(["git", "clone", "-q", host, clone])
    run(["git", "-C", clone, "-c", "protocol.file.allow=always", "submodule", "update", "--init", "-q"])
    assert cli(clone / ".agents/skills/factum", clone, "init")["initialized"]


def packaging_scenario(workspace, source):
    distributions = workspace / "distributions"
    builder = workspace / "builder"
    run(["uv", "venv", "--python", os.environ.get("FACTUM_TEST_PYTHON", "3.12"), builder])
    python = builder / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run(["uv", "pip", "install", "--python", python, "build"])
    run([python, "-m", "build", "--outdir", distributions, source])
    wheel = next(distributions.glob("*.whl"))
    sdist = next(distributions.glob("*.tar.gz"))
    import tarfile
    import zipfile
    with zipfile.ZipFile(wheel) as archive:
        paths = set(archive.namelist())
        for manifest_path in (source / "scripts/factum_lib/assets/packs").glob("*/*/pack.json"):
            manifest = json.loads(manifest_path.read_bytes())
            relative = manifest_path.parent.relative_to(source / "scripts").as_posix()
            for name in ["pack.json", *manifest["schemas"], *manifest["definitions"]]:
                assert f"{relative}/{name}" in paths
    unpacked = workspace / "sdist"
    with tarfile.open(sdist) as archive:
        archive.extractall(unpacked, filter="data")
    rebuilt = workspace / "rebuilt"
    run([python, "-m", "build", "--wheel", "--outdir", rebuilt, next(unpacked.iterdir())])
    clean = workspace / "console environment"
    run(["uv", "venv", "--python", os.environ.get("FACTUM_TEST_PYTHON", "3.12"), clean])
    executable = clean / ("Scripts/factum.exe" if os.name == "nt" else "bin/factum")
    interpreter = clean / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run(["uv", "pip", "install", "--python", interpreter, next(rebuilt.glob("*.whl"))])
    host = workspace / "console host"
    host.mkdir()
    git(host, "init", "-q")
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.pop("FACTUM_REPO", None)
    def console(*args):
        result = run([executable, "--repo", host, *args], cwd=host, env=environment)
        value = json.loads(result.stdout)
        assert value["ok"], value
        return value
    console("init")
    catalog = console("schema", "list")
    capture_result = console("capture", "--url", "synthetic:console", "--file", source / "examples/capture.txt", "--storage", "git", "--actor", "agent:synthetic", "--key", "console/capture")
    console("export")
    console("verify", "--blobs")
    (host / "data/.local/factum.db").unlink()
    console("rebuild")
    assert console("get", capture_result["ids"]["observation"])["record"]["body"]["data_schema"] == "urn:factum:web:web-capture:1"
    # Also exercise the documented uv tool source-install command in isolation.
    tool_env = environment | {
        "UV_TOOL_DIR": str(workspace / "uv-tools"),
        "UV_TOOL_BIN_DIR": str(workspace / "uv-tool-bin"),
    }
    run(["uv", "tool", "install", "--python", os.environ.get("FACTUM_TEST_PYTHON", "3.12"), source], env=tool_env)
    assert json.loads(run([workspace / "uv-tool-bin/factum", "--repo", host, "doctor"], env=tool_env).stdout)["ok"]
    return catalog, {
        str(path.relative_to(workspace)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [wheel, sdist, next(rebuilt.glob("*.whl"))]
    }


def smoke(workspace, packaging=True):
    source, identity = snapshot(workspace)
    fixtures = workspace / "fixtures"
    fixtures.mkdir()
    host_a = workspace / "host-a"
    host_a.mkdir()
    git(host_a, "init", "-q", "-b", "main")
    skill_a = install_skill(host_a, source, identity)
    # Check every public command's real help, including nested actions.
    help_commands = [
        [name] for name in ("init", "status", "doctor", "rebuild", "export", "verify", "add", "template", "capture", "extract", "note", "get", "match", "query", "graph")
    ] + [["schema", name] for name in ("list", "describe", "assigned", "validate", "install")] + [["lane", name] for name in ("list", "new", "show", "edit", "link")]
    for command in help_commands:
        run(["uv", "run", "--no-project", "--python", os.environ.get("FACTUM_TEST_PYTHON", "3.12"), skill_a / "scripts/factum.py", *command, "--help"], cwd=host_a)
    (host_a / "data").mkdir()
    (host_a / "data/unrelated.txt").write_bytes(b"Unrelated host data\r\n")
    (host_a / ".gitignore").write_bytes(b"# Existing ignore\r\nunrelated-cache/\r\n")
    (host_a / ".gitattributes").write_bytes(b"# Existing attributes\r\n*.custom -text\r\n")
    original_attributes = (host_a / ".gitattributes").read_bytes()
    initialized = cli(skill_a, host_a, "init", explicit=False)
    assert (host_a / ".gitattributes").read_bytes().startswith(original_attributes)
    assert cli(skill_a, host_a, "init", cwd=skill_a, explicit=False)["corpus_id"] == initialized["corpus_id"]
    assert cli(skill_a, host_a, "status", cwd=fixtures, env={"FACTUM_REPO": str(host_a)}, explicit=False)["repo"] == str(host_a)
    assert cli(skill_a, skill_a, "init", ok=False)["error"]["code"] == "REPO"
    # Demonstrate the documented integration block without changing a real host.
    instructions = "# Synthetic host instructions\n\nNo external publication.\n"
    install_text = (source / "INSTALL.md").read_text()
    start = install_text.index("<!-- BEGIN FACTUM INTEGRATION -->")
    end = install_text.index("<!-- END FACTUM INTEGRATION -->", start) + len("<!-- END FACTUM INTEGRATION -->")
    block = install_text[start:end]
    (host_a / "AGENTS.md").write_text(instructions + "\n" + block + "\n")
    assert (host_a / "AGENTS.md").read_text().count("<!-- BEGIN FACTUM INTEGRATION -->") == 1

    proposal = source / "examples/pack/1.0.0"
    assert cli(skill_a, host_a, "schema", "install", proposal)["valid"]
    assert "example.exact" not in cli(skill_a, host_a, "schema", "list")["definitions"]["observable"]
    cli(skill_a, host_a, "schema", "install", proposal, "--approve")
    catalog_a = cli(skill_a, host_a, "schema", "list")
    assert cli(skill_a, host_a, "schema", "assigned", "observation", "example.capture")["definition"]["schema"] == "urn:factum:example:capture:1"
    cli(skill_a, host_a, "schema", "describe", "urn:factum:example:capture:1")
    text = "東京 e\u0301\r\nhttps://Example.COM/CasePath?Token=AbC#MiXeD\r\nExample.COM\r\nSYNTHETIC_FAKE_TOKEN_NOT_A_CREDENTIAL\r\n"
    text_file = fixtures / "evidence with spaces.txt"
    text_file.write_bytes(text.encode("utf-8"))
    binary = fixtures / "binary"
    binary.write_bytes(b"\x00\xff\r\nSYNTHETIC")
    captured = capture(skill_a, host_a, text_file, "smoke/capture")
    assert capture(skill_a, host_a, text_file, "smoke/capture")["ids"] == captured["ids"]
    acquisition = capture(skill_a, host_a, text_file, "smoke/capture-distinct")
    assert acquisition["ids"]["observation"] != captured["ids"]["observation"]
    binary_capture = capture(skill_a, host_a, binary, "smoke/binary")
    local_capture = capture(skill_a, host_a, binary, "smoke/local", "local")
    # Use different local-only bytes, so no Git-retained CAS copy masks absence.
    local_file = fixtures / "local-only"
    local_file.write_bytes(b"synthetic local-only evidence")
    local_only = capture(skill_a, host_a, local_file, "smoke/local-only", "local")
    reference = cli(skill_a, host_a, "capture", "--dataset", "synthetic:metadata-only", "--coverage", "metadata_only", "--actor", "agent:synthetic", "--key", "smoke/reference")
    assert cli(skill_a, host_a, "get", reference["ids"]["reference"])["record"]["body"] == {"reference": {"uri": "synthetic:metadata-only"}}

    bundle = json.loads((source / "examples/bundle.json").read_bytes())
    bundle["files"][0]["path"] = str(text_file)
    bundle_file = fixtures / "example-bundle.json"
    write_json(bundle_file, bundle)
    custom = cli(skill_a, host_a, "add", "--input", bundle_file)
    original_records = {rid: cli(skill_a, host_a, "get", rid)["record"] for rid in custom["record_ids"]}
    observation = original_records[custom["ids"]["observation"]]
    assert observation["body"]["data"]["artifact"] == custom["ids"]["file"]
    assert observation["body"]["data"]["items"] == "@source"
    assert original_records[custom["ids"]["claim"]]["body"]["value"] == {"literal": "@source"}
    lane = cli(skill_a, host_a, "lane", "new", "Synthetic smoke lane")["lane"]["id"]
    cli(skill_a, host_a, "lane", "show", lane)
    cli(skill_a, host_a, "lane", "edit", lane, "--tags", '{"synthetic":true}')
    assert cli(skill_a, host_a, "lane", "list")["lanes"]
    cli(skill_a, host_a, "lane", "link", lane, custom["ids"]["value"], "--actor", "agent:synthetic", "--key", "smoke/lane-link")
    cli(skill_a, host_a, "note", "--subject", custom["ids"]["value"], "--property", "synthetic", "--value", '"@source"', "--basis", "OBSERVED", "--cite", custom["ids"]["observation"], "--actor", "agent:synthetic", "--key", "smoke/note")
    assert cli(skill_a, host_a, "template", "--type", "example.capture")["data_schema"]["$id"] == "urn:factum:example:capture:1"
    query_file = fixtures / "query.json"
    write_json(query_file, {"kind": "claim", "count": True})
    assert cli(skill_a, host_a, "query", "--input", query_file)["count"] == 2
    payload_file = fixtures / "payload.json"
    write_json(payload_file, observation["body"]["data"])
    assert cli(skill_a, host_a, "schema", "validate", "--schema", observation["body"]["data_schema"], "--input", payload_file)["valid"]
    assert cli(skill_a, host_a, "match", "--value", bundle["records"][2]["body"]["value"], "--type", "example.exact")["status"] == "found"
    add_value(skill_a, host_a, fixtures, "smoke/domain", "Example.COM")
    assert cli(skill_a, host_a, "match", "--value", "EXAMPLE.com", "--type", "domain", "--mode", "key")["status"] == "found"
    assert cli(skill_a, host_a, "match", "--text", "Example.CO", "--mode", "fuzzy")["status"] == "found"
    assert cli(skill_a, host_a, "match", "--value", "no-such-evidence")["status"] == "not_found"
    assert cli(skill_a, host_a, "match", "--value", "no-such-evidence", "--type", "unknown", ok=False)["error"]["code"] == "QUERY"
    extracted = cli(skill_a, host_a, "extract", captured["ids"]["observation"], "--types", "url", "--actor", "agent:synthetic", "--key", "smoke/extract")
    assert extracted["extracted"] == 1
    for rid in extracted["record_ids"]:
        record = cli(skill_a, host_a, "get", rid)["record"]
        if record["record_kind"] == "sighting":
            assert cli(skill_a, host_a, "get", rid, "--context", "10")["exact"] == record["body"]["locator"]["quote"]["exact"]

    # Two real toolkit processes retry one request concurrently.
    concurrent_file = fixtures / "concurrent.json"
    write_json(concurrent_file, {"bundle": 2, "actor": "agent:synthetic", "idempotency_key": "smoke/concurrent", "records": [{"ref": "v", "kind": "observable", "body": {"type": "text", "value": "concurrent synthetic"}}]})
    writer_lock(skill_a, host_a, concurrent_file)
    pending_count = cli(skill_a, host_a, "status")["records"]
    (host_a / "data/.local/factum.db").unlink()
    assert cli(skill_a, host_a, "match", "--value", "absent", ok=False)["error"]["code"] == "INDEX_MISSING"
    cli(skill_a, host_a, "rebuild")
    assert cli(skill_a, host_a, "status")["records"] == pending_count
    cli(skill_a, host_a, "export")
    assert cli(skill_a, host_a, "export")["exported"] == []
    assert cli(skill_a, host_a, "verify", "--blobs")["artifacts"]["missing"] == []
    first_commit = commit(host_a, "Synthetic initial evidence and custom pack")
    remote = workspace / "corpus-remote.git"
    run(["git", "init", "--bare", "-q", "--initial-branch=main", remote])
    git(host_a, "remote", "add", "origin", str(remote))
    git(host_a, "push", "-q", "-u", "origin", "main")
    host_b = workspace / "host-b"
    run(["git", "clone", "-q", remote, host_b])
    skill_b = install_skill(host_b, source, identity)
    assert cli(skill_b, host_b, "init")["corpus_id"] == initialized["corpus_id"]
    missing = cli(skill_b, host_b, "verify", "--blobs")["artifacts"]["missing"]
    assert local_only["ids"]["file0"] in missing
    assert local_capture["ids"]["file0"] not in missing
    cli(skill_b, host_b, "rebuild")
    for rid, record in original_records.items():
        assert cli(skill_b, host_b, "get", rid)["record"] == record
    for result, expected in [(captured, text_file.read_bytes()), (binary_capture, binary.read_bytes())]:
        artifact = cli(skill_b, host_b, "get", result["ids"]["file0"])["record"]["body"]
        path = host_b / "data/blobs/sha256" / artifact["sha256"][:2] / artifact["sha256"]
        assert path.read_bytes() == expected
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact["sha256"]
    assert cli(skill_b, host_b, "add", "--input", bundle_file)["ids"] == custom["ids"]

    add_value(skill_a, host_a, fixtures, "site-a/value", "Site-A.Example")
    add_value(skill_b, host_b, fixtures, "site-b/value", "Site-B.Example")
    cli(skill_a, host_a, "export")
    cli(skill_b, host_b, "export")
    commit(host_a, "Synthetic independent site A batch")
    commit(host_b, "Synthetic independent site B batch")
    git(host_a, "push", "-q")
    git(host_b, "fetch", "-q", "origin")
    git(host_b, "merge", "--no-edit", "origin/main")
    cli(skill_b, host_b, "verify")
    cli(skill_b, host_b, "rebuild")
    git(host_b, "push", "-q")
    git(host_a, "pull", "-q", "--ff-only")
    assert cli(skill_a, host_a, "status")["stale"]
    cli(skill_a, host_a, "verify")
    cli(skill_a, host_a, "rebuild")
    state_a = cli(skill_a, host_a, "status")
    state_b = cli(skill_b, host_b, "status")
    assert state_a["searched"]["state_digest"] == state_b["searched"]["state_digest"]
    assert git(host_a, "rev-parse", "HEAD").stdout == git(host_b, "rev-parse", "HEAD").stdout
    current_commit = git(host_a, "rev-parse", "HEAD").stdout.strip()
    # Current catalog additions must not leak into the earlier commit's view.
    delta = fixtures / "delta-pack"
    delta.mkdir()
    write_json(delta / "pack.json", {
        "pack_format": 1, "name": "factum-example-extra", "version": "1.0.0",
        "requires": {"factum-example": "1.0.0"}, "schemas": [],
        "definitions": ["definitions.json"], "tags": {},
    })
    write_json(delta / "definitions.json", {"definitions": [{"category": "observable", "name": "example.extra", "schema": "urn:factum:example:value:1", "tags": {}}], "tags": {}})
    cli(skill_a, host_a, "schema", "install", delta, "--approve")
    add_value(skill_a, host_a, fixtures, "current/pending", "Only.Pending.Example")
    historical = cli(skill_a, host_a, "--at", first_commit, "rebuild")
    assert historical["searched"]["pending_batches"] == 0
    assert first_commit in historical["database"]
    assert cli(skill_a, host_a, "--at", first_commit, "match", "--value", "Only.Pending.Example")["status"] == "not_found"
    assert cli(skill_a, host_a, "--at", first_commit, "get", custom["ids"]["observation"])["record"] == observation
    assert "example.extra" not in cli(skill_a, host_a, "--at", first_commit, "schema", "list")["definitions"]["observable"]
    assert git(host_a, "rev-parse", "HEAD").stdout.strip() == current_commit
    submodule_scenario(workspace, source)
    distribution_hashes = {}
    if packaging:
        console_catalog, distribution_hashes = packaging_scenario(workspace, source)
        seed_catalog = cli(workspace / "submodule host/.agents/skills/factum", workspace / "submodule host", "schema", "list")
        assert console_catalog == seed_catalog
        assert all(schema in catalog_a["schemas"] for schema in console_catalog["schemas"])
    assert hashes(source, identity) == identity
    report = {
        "ok": True, "workspace": str(workspace), "source_files": identity,
        "source_digest": hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest(),
        "runtime_digest": hashlib.sha256(json.dumps({
            name: value for name, value in identity.items()
            if name.startswith("scripts/") or name == "pyproject.toml"
        }, sort_keys=True).encode()).hexdigest(),
        "snapshot_commit": git(source, "rev-parse", "HEAD").stdout.strip(),
        "help_commands_checked": len(help_commands),
        "records_at_merged_commit": state_a["records"],
        "logical_state_digest": state_a["searched"]["state_digest"],
        "distribution_hashes": distribution_hashes,
        "scenarios": ["nested clone", "path resolution", "exact evidence and bytes", "custom pack", "extraction context", "concurrent retries", "pending recovery", "two-site merge", "local-byte disclosure", "historical rebuild", "submodule"] + (["wheel", "sdist-to-wheel", "clean console"] if packaging else []),
    }
    write_json(workspace / "smoke-report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, help="New, nonexistent disposable directory")
    parser.add_argument("--skip-packaging", action="store_true", help="Only for focused reruns, not release acceptance")
    args = parser.parse_args()
    if args.workspace:
        args.workspace.mkdir(parents=True, exist_ok=False)
        workspace = args.workspace.resolve()
    else:
        parent = Path.home() / "factum-validation"
        parent.mkdir(exist_ok=True)
        workspace = Path(tempfile.mkdtemp(prefix="smoke-", dir=parent))
    print(json.dumps(smoke(workspace, not args.skip_packaging), sort_keys=True))


if __name__ == "__main__":
    main()
