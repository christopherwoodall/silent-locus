import json

import pytest

from factum_lib.cli import dispatch, parser
from factum_lib.schemas import SchemaError, write_json_atomic
from factum_lib.store import FactumError, State, add_bundle
from tools.validation_support import cli, git, install_skill, snapshot


def invoke(repo, *args):
    return dispatch(repo, parser().parse_args(args))


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    return snapshot(tmp_path_factory.mktemp("installation"))


@pytest.fixture
def installed(tmp_path, staged):
    host = tmp_path / "external host with spaces"
    host.mkdir()
    git(host, "init", "-q")
    skill = install_skill(host, *staged)
    return host, skill


def test_real_nested_clone_path_resolution(installed, tmp_path):
    host, skill = installed
    (host / "data").mkdir()
    (host / "data/unrelated.txt").write_bytes(b"unrelated\r\n")
    result = cli(skill, host, "init", explicit=False)
    identity = result["corpus_id"]
    assert cli(skill, host, "init", cwd=skill, explicit=False)["corpus_id"] == identity
    assert cli(skill, host, "status", cwd=tmp_path)["repo"] == str(host)
    assert cli(skill, host, "status", cwd=tmp_path, env={"FACTUM_REPO": str(host)}, explicit=False)["repo"] == str(host)
    assert cli(skill, skill, "init", ok=False)["error"]["code"] == "REPO"
    assert not (skill / "data").exists()
    assert (host / "data/unrelated.txt").read_bytes() == b"unrelated\r\n"
    assert ".agents/skills/factum" not in git(host, "status", "--porcelain", "--untracked-files=all").stdout


def test_incompatible_format_does_not_change_host_files(installed):
    host, skill = installed
    cli(skill, host, "init")
    corpus = host / "data/corpus.json"
    value = json.loads(corpus.read_bytes())
    value["format_version"] = 1
    write_json_atomic(corpus, value)
    before = {p: (host / p).read_bytes() for p in (".gitignore", ".gitattributes", "data/.local/site.json", "data/schema-lock.json")}
    assert cli(skill, host, "init", ok=False)["error"]["code"] == "FORMAT"
    assert all((host / p).read_bytes() == raw for p, raw in before.items())


@pytest.mark.parametrize("mode", ["exact", "key", "fuzzy"])
def test_matching_modes(state, bundle, mode):
    add_bundle(state, bundle)
    query = "Example.COM" if mode == "exact" else "EXAMPLE.com" if mode == "key" else "Example.CO"
    result = invoke(state.repo, "match", "--value", query, "--type", "domain", "--mode", mode)
    assert result["status"] == "found"
    assert result["matches"][0]["value"] == "Example.COM"
    assert result["searched"]["state_digest"]
    assert result["searched"]["pending_batches"] == 1


@pytest.mark.parametrize("query", [
    {"value": "none", "type": "unknown"},
    {"value": "none", "mode": "fuzzy", "constraint": "unsupported"},
    {"value": "", "mode": "exact"}, {"value": "ab", "mode": "fuzzy"},
    {"value": "valid", "limit": 0}, {"value": "valid", "limit": True},
    {"value": "valid", "type": []},
])
def test_invalid_queries_fail_not_not_found(repo, tmp_path, query):
    path = tmp_path / "query.json"
    write_json_atomic(path, query)
    with pytest.raises((FactumError, SchemaError)):
        invoke(repo, "match", "--input", str(path))


def test_no_match_and_truncation(state, bundle):
    bundle["records"] *= 3
    for index, record in enumerate(bundle["records"]):
        # Avoid aliasing the repeated dictionary.
        bundle["records"][index] = {**record, "ref": f"value{index}"}
    add_bundle(state, bundle)
    found = invoke(state.repo, "match", "--value", "Example.COM", "--limit", "1")
    assert found["truncated"] and len(found["matches"]) == 1
    absent = invoke(state.repo, "match", "--value", "nonexistent")
    assert absent["status"] == "not_found" and absent["searched"]["coverage"]


def test_fuzzy_substring_match(state):
    """Short queries must match longer values that contain them.

    Regression test: ratio("exploitgym", "sunblaze-ucb/exploitgym") is 62.5,
    below the 65 gate, so the old code missed genuine substring hits.
    """
    bundle = {
        "bundle": 2, "actor": "agent:synthetic", "idempotency_key": "test/fuzzy-sub",
        "tags": {},
        "records": [{
            "ref": "obs", "kind": "observable",
            "body": {"type": "domain", "value": "sunblaze-ucb/exploitgym"},
            "tags": {},
        }],
    }
    add_bundle(state, bundle)
    result = invoke(
        state.repo, "match", "--value", "exploitgym",
        "--type", "domain", "--mode", "fuzzy",
    )
    assert result["status"] == "found"
    assert result["matches"][0]["value"] == "sunblaze-ucb/exploitgym"
    assert result["matches"][0]["score"] >= 65


def test_fuzzy_similar_length_still_matches(state, bundle):
    """Existing similar-length fuzzy behavior is preserved."""
    add_bundle(state, bundle)
    result = invoke(
        state.repo, "match", "--value", "Example.CO",
        "--type", "domain", "--mode", "fuzzy",
    )
    assert result["status"] == "found"
    assert result["matches"][0]["value"] == "Example.COM"


def test_fuzzy_unrelated_still_rejected(state, bundle):
    """Unrelated values must not match, even with substring scoring."""
    add_bundle(state, bundle)
    result = invoke(
        state.repo, "match", "--value", "zzzqqq",
        "--type", "domain", "--mode", "fuzzy",
    )
    assert result["status"] == "not_found"


def test_fuzzy_score_prefers_best_alignment(state):
    """The reported score reflects the best alignment found."""
    from factum_lib.cli import fuzzy_score
    assert fuzzy_score("exploitgym", "sunblaze-ucb/exploitgym") == 100.0
    assert fuzzy_score("abc", "abc") == 100.0
    assert fuzzy_score("zzz", "qqq") < 65


def test_stale_missing_index_errors(state, bundle):
    add_bundle(state, bundle)
    current = State(state.repo).load()
    current.db_path.unlink()
    with pytest.raises(FactumError, match="Run rebuild"):
        invoke(state.repo, "match", "--value", "absent")
    current.project()
    # An external portable change must invalidate the projection.
    corpus = state.repo / "data/corpus.json"
    document = json.loads(corpus.read_bytes())
    document["tags"]["external_change"] = True
    write_json_atomic(corpus, document)
    assert invoke(state.repo, "status")["stale"]
    with pytest.raises(FactumError, match="Run rebuild"):
        invoke(state.repo, "match", "--value", "absent")


def capture_fixture(repo, tmp_path, raw):
    path = tmp_path / "capture"
    path.write_bytes(raw)
    return invoke(repo, "capture", "--url", "https://Example.COM/Case?A=B#C", "--file", str(path), "--storage", "git", "--actor", "agent:synthetic", "--key", "test/capture")


def test_extract_offsets_context_and_retry(repo, tmp_path):
    text = "東京 e\u0301\r\nhttps://Example.COM/Case?Token=AbC#MiXeD\r\n"
    capture = capture_fixture(repo, tmp_path, text.encode())
    result = invoke(repo, "extract", capture["ids"]["observation"], "--types", "url", "--actor", "agent:synthetic", "--key", "test/extract")
    assert result["extracted"] == 1
    records = State(repo).load().records
    sighting = next(records[rid] for rid in result["record_ids"] if records[rid]["record_kind"] == "sighting")
    start = text.index("https:")
    locator = sighting["body"]["locator"]
    assert locator["text_pos"] == {"start": start, "end": text.index("\r\n", start)}
    assert sighting["body"]["method"] == "regex-substrings/1:url"
    context = invoke(repo, "get", sighting["id"], "--context", "20")
    assert context["exact"] == locator["quote"]["exact"]
    assert invoke(repo, "extract", capture["ids"]["observation"], "--types", "url", "--actor", "agent:synthetic", "--key", "test/extract")["ids"] == result["ids"]


@pytest.mark.parametrize("case", ["invalid-utf8", "byte-budget", "match-budget", "missing-bytes", "unknown-extractor"])
def test_extraction_failures_are_atomic(repo, tmp_path, case):
    capture = capture_fixture(repo, tmp_path, b"\xff" if case == "invalid-utf8" else b"https://one.example https://two.example")
    before = State(repo).load()
    if case == "missing-bytes":
        artifact = before.records[capture["ids"]["file0"]]["body"]["sha256"]
        (repo / "data/blobs/sha256" / artifact[:2] / artifact).unlink()
    extra = ["--max-bytes", "1"] if case == "byte-budget" else ["--max-matches", "1"] if case == "match-budget" else ["--types", "unknown"] if case == "unknown-extractor" else []
    with pytest.raises((FactumError, UnicodeDecodeError)):
        invoke(repo, "extract", capture["ids"]["observation"], "--actor", "agent:synthetic", "--key", "test/extract", *extra)
    assert State(repo).load().records == before.records


def test_cyclic_graph_and_limits(state, bundle):
    bundle["records"] = [
        {"ref": f"v{i}", "kind": "observable", "body": {"type": "text", "value": str(i)}} for i in range(6)
    ] + [
        {"kind": "edge", "body": {"subject": f"@v{i}", "object": f"@v{(i + 1) % 6}", "predicate": "part_of"}} for i in range(6)
    ]
    result = add_bundle(state, bundle)
    full = invoke(state.repo, "graph", result["ids"]["v0"], "--depth", "10")
    assert len(full["nodes"]) == 6 and len(full["edges"]) == 6
    limited = invoke(state.repo, "graph", result["ids"]["v0"], "--limit", "1")
    assert limited["truncated"] and len(limited["edges"]) == 1
    shallow = invoke(state.repo, "graph", result["ids"]["v0"], "--depth", "0")
    assert shallow["truncated"]


def test_historical_state_does_not_require_current_corpus(installed, tmp_path):
    host, skill = installed
    cli(skill, host, "init")
    path = tmp_path / "bundle.json"
    write_json_atomic(path, {"bundle": 2, "actor": "agent:synthetic", "idempotency_key": "historical", "records": [{"ref": "v", "kind": "observable", "body": {"type": "domain", "value": "Example.COM"}}]})
    result = cli(skill, host, "add", "--input", path)
    cli(skill, host, "export")
    git(host, "add", "--all")
    git(host, "commit", "-qm", "Synthetic historical corpus")
    commit = git(host, "rev-parse", "HEAD").stdout.strip()
    (host / "data/corpus.json").unlink()
    historical = cli(skill, host, "--at", commit, "rebuild")
    assert commit in historical["database"]
    assert cli(skill, host, "--at", commit, "get", result["ids"]["v"])["record"]["body"]["value"] == "Example.COM"
    assert git(host, "rev-parse", "HEAD").stdout.strip() == commit
