"""Acceptance tests for the `update` record command.

Update contract (implemented in ``factum_lib.store.update_record``)::

    update_record(state, record_id, actor, changes) -> dict

* ``changes`` is either a dict of tag key -> value (a ``None`` value
  deletes the tag; bare keys and ``tags.``-prefixed keys both address
  tags) or a list of ``(path, value)`` pairs in ``--set <path>=<value>``
  shape.
* Editable paths: ``tags.*`` except reserved ``factum.*`` keys, plus the
  schema-declared body paths (``body.provenance`` when the core body
  schema declares it; ``body.data.provenance`` / ``body.data.status``
  when the record's assigned ``data_schema`` declares them). Anything
  else fails with ``EVIDENCE_EDIT``.
* Empty actor -> ``IDENTITY``; unknown ID -> ``NOT_FOUND``; retracted
  target -> ``RETRACTED``; ``body.data.status`` outside its schema enum
  -> ``UPDATE_VALUE``.
* The write re-reads the owning file under a guard and applies to the
  latest bytes, so concurrent updates to different fields merge. A
  no-op returns the current record unchanged (no fingerprint churn, no
  audit stamps).
* Effective updates stamp ``tags["factum.updated_at"]`` /
  ``tags["factum.updated_by"]``, set the envelope ``actor`` to the
  updater (original authorship stays in immutable
  ``tags["factum.author"]``), recompute the fingerprint, rewrite the
  owning file (pending JSON or exported batch with recomputed manifest
  hash), and rebuild the projection.
* CLI: ``factum update <id> --actor A --set <path>=<value>`` (repeatable;
  values are JSON). ``update`` is a mutating command, so ``--at`` fails
  with ``READ_ONLY``.

Design line under test: ``tags`` are annotations (mutable); ``body`` is
evidence (immutable except the schema-declared metadata paths above).
"""

import json
import shutil
import threading
import uuid
from pathlib import Path

import pytest

from factum_lib import store
from factum_lib.cli import dispatch, parser
from factum_lib.schemas import install_pack, sha256
from factum_lib.store import FactumError, State, add_bundle, export_pending
from tools.validation_support import git


ROOT = Path(__file__).resolve().parents[1]


def invoke(repo, *args):
    return dispatch(repo, parser().parse_args(args))


def _bundle(actor="agent:synthetic", key=None, tags=None, kind="observable", body=None):
    return {
        "bundle": 2,
        "actor": actor,
        "idempotency_key": key or f"test/{uuid.uuid4().hex}",
        "tags": {},
        "records": [{
            "ref": "value",
            "kind": kind,
            "body": body if body is not None else {"type": "domain", "value": "Example.COM"},
            "tags": tags if tags is not None else {},
        }],
    }


def _add(state, **kwargs):
    result = add_bundle(state, _bundle(**kwargs))
    return result["ids"]["value"]


def _fresh(repo):
    return State(repo).load()


def _record(repo, record_id):
    return _fresh(repo).records[record_id]


def _install_infra_pack(repo, tmp_path):
    src = tmp_path / "infra-pack"
    shutil.copytree(ROOT / "schema-proposals/infra/1.0.0", src)
    result = install_pack(repo, src, True)
    assert result["installed"]


def _add_ioc(state):
    """An infra.ioc observation: data_schema declares provenance and status."""
    bundle = {
        "bundle": 2,
        "actor": "agent:synthetic",
        "idempotency_key": f"test/{uuid.uuid4().hex}",
        "tags": {},
        "records": [
            {
                "ref": "src",
                "kind": "source",
                "body": {"source_type": "submitted", "locator": "test"},
                "tags": {},
            },
            {
                "ref": "ioc",
                "kind": "observation",
                "body": {
                    "type": "infra.ioc",
                    "source": "@src",
                    "data_schema": "urn:factum:infra:ioc:1",
                    "data": {
                        "term": "evil.example",
                        "category": "domain",
                        "provenance": "seed",
                        "status": "candidate",
                    },
                },
                "tags": {},
            },
        ],
    }
    return add_bundle(state, bundle)["ids"]["ioc"]


def _locate(repo, record_id):
    """Return ("pending"|"exported", Path) for the file holding the record."""
    for path in (repo / "data/.local/pending").glob("*.json"):
        document = json.loads(path.read_bytes())
        if any(record["id"] == record_id for record in document["records"]):
            return ("pending", path)
    for path in (repo / "data/records").glob("*/records.jsonl"):
        for line in path.read_bytes().splitlines():
            if json.loads(line)["id"] == record_id:
                return ("exported", path)
    raise AssertionError(f"record {record_id} not found on disk")


def _assert_manifest_consistent(repo):
    for manifest_path in (repo / "data/records").glob("*/manifest.json"):
        manifest = json.loads(manifest_path.read_bytes())
        raw = (manifest_path.parent / "records.jsonl").read_bytes()
        assert manifest["records_sha256"] == sha256(raw), manifest_path
        assert manifest["record_count"] == len(raw.splitlines()), manifest_path


# ---------------------------------------------------------------------------
# Positive
# ---------------------------------------------------------------------------

def test_update_tag_on_pending_record(state):
    record_id = _add(state)
    updated = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", {"status": "confirmed"}
    )
    assert updated["tags"]["status"] == "confirmed"
    assert updated["tags"][store.AUTHOR_TAG] == "agent:synthetic"
    assert updated["tags"]["factum.updated_by"] == "agent:updater"
    assert "factum.updated_at" in updated["tags"]
    assert updated["actor"] == "agent:updater"
    kind, _ = _locate(state.repo, record_id)
    assert kind == "pending"
    assert _record(state.repo, record_id)["tags"]["status"] == "confirmed"


def test_update_tag_on_exported_record(state):
    record_id = _add(state)
    export_pending(_fresh(state.repo))
    kind, _ = _locate(state.repo, record_id)
    assert kind == "exported"
    updated = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", [("tags.status", "confirmed")]
    )
    assert updated["tags"]["status"] == "confirmed"
    assert _record(state.repo, record_id)["tags"]["status"] == "confirmed"
    _assert_manifest_consistent(state.repo)
    _fresh(state.repo)


def test_update_body_provenance_when_declared(state, tmp_path):
    _install_infra_pack(state.repo, tmp_path)
    record_id = _add_ioc(_fresh(state.repo))
    before = _record(state.repo, record_id)
    updated = store.update_record(
        _fresh(state.repo),
        record_id,
        "agent:updater",
        [("body.data.provenance", "rechecked 2026-10-09")],
    )
    assert updated["body"]["data"]["provenance"] == "rechecked 2026-10-09"
    assert updated["body"]["data"]["term"] == before["body"]["data"]["term"]
    assert updated["body"]["data"]["status"] == before["body"]["data"]["status"]


def test_update_body_status_when_declared(state, tmp_path):
    _install_infra_pack(state.repo, tmp_path)
    record_id = _add_ioc(_fresh(state.repo))
    updated = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", [("body.data.status", "active")]
    )
    assert updated["body"]["data"]["status"] == "active"


def test_update_deletes_tag_via_null(state):
    record_id = _add(state, tags={"stale": "yes", "keep": "yes"})
    updated = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", {"stale": None}
    )
    assert "stale" not in updated["tags"]
    assert updated["tags"]["keep"] == "yes"


def test_update_dict_and_pairs_forms_agree(state):
    first_id = _add(state)
    second_id = _add(state)
    first = store.update_record(
        _fresh(state.repo), first_id, "agent:updater", {"status": "confirmed"}
    )
    second = store.update_record(
        _fresh(state.repo), second_id, "agent:updater", [("tags.status", "confirmed")]
    )
    assert first["tags"]["status"] == second["tags"]["status"] == "confirmed"
    assert first["body"] == second["body"]


# ---------------------------------------------------------------------------
# Negative
# ---------------------------------------------------------------------------

def test_update_rejects_undeclared_body_path(state):
    """Seed schemas declare no body metadata paths: the path is rejected."""
    record_id = _add(state)
    with pytest.raises(FactumError) as excinfo:
        store.update_record(
            _fresh(state.repo), record_id, "agent:updater",
            [("body.data.status", "active")],
        )
    assert excinfo.value.code == "EVIDENCE_EDIT"


@pytest.mark.parametrize("changes", [[("body.value", "evil")], {"body.value": "evil"}])
def test_update_rejects_evidence_body_field(state, changes):
    record_id = _add(state)
    before = _record(state.repo, record_id)
    with pytest.raises(FactumError) as excinfo:
        store.update_record(_fresh(state.repo), record_id, "agent:updater", changes)
    assert excinfo.value.code == "EVIDENCE_EDIT"
    assert _record(state.repo, record_id)["body"] == before["body"]


@pytest.mark.parametrize(
    "changes",
    [{"factum.author": "agent:impostor"}, [("tags.factum.author", "agent:impostor")]],
)
def test_update_rejects_reserved_author_tag(state, changes):
    record_id = _add(state)
    with pytest.raises(FactumError) as excinfo:
        store.update_record(_fresh(state.repo), record_id, "agent:updater", changes)
    assert excinfo.value.code == "EVIDENCE_EDIT"
    assert _record(state.repo, record_id)["tags"][store.AUTHOR_TAG] == "agent:synthetic"


def test_update_rejects_other_reserved_factum_tags(state):
    record_id = _add(state)
    with pytest.raises(FactumError) as excinfo:
        store.update_record(
            _fresh(state.repo), record_id, "agent:updater",
            [("tags.factum.updated_by", "agent:impostor")],
        )
    assert excinfo.value.code == "EVIDENCE_EDIT"


def test_update_rejects_status_outside_enum(state, tmp_path):
    _install_infra_pack(state.repo, tmp_path)
    record_id = _add_ioc(_fresh(state.repo))
    with pytest.raises(FactumError) as excinfo:
        store.update_record(
            _fresh(state.repo), record_id, "agent:updater",
            [("body.data.status", "bogus")],
        )
    assert excinfo.value.code == "UPDATE_VALUE"
    assert _record(state.repo, record_id)["body"]["data"]["status"] == "candidate"


def test_update_nonexistent_record(state):
    with pytest.raises(FactumError) as excinfo:
        store.update_record(
            _fresh(state.repo), "observable_deadbeef", "agent:updater",
            {"status": "x"},
        )
    assert excinfo.value.code == "NOT_FOUND"


def test_update_retracted_target(state):
    record_id = _add(state)
    add_bundle(
        _fresh(state.repo),
        _bundle(
            kind="retraction",
            body={"target": record_id, "reason": "superseded by re-review"},
        ),
    )
    with pytest.raises(FactumError) as excinfo:
        store.update_record(
            _fresh(state.repo), record_id, "agent:updater", {"status": "confirmed"}
        )
    assert excinfo.value.code == "RETRACTED"


@pytest.mark.parametrize("actor", [None, ""])
def test_update_rejects_empty_actor(state, actor):
    record_id = _add(state)
    with pytest.raises(FactumError) as excinfo:
        store.update_record(_fresh(state.repo), record_id, actor, {"status": "x"})
    assert excinfo.value.code == "IDENTITY"


def test_update_read_only_under_at(state):
    record_id = _add(state)
    export_pending(_fresh(state.repo))
    git(state.repo, "-c", "user.email=test@example.com", "-c", "user.name=test",
        "add", "-A")
    git(state.repo, "-c", "user.email=test@example.com", "-c", "user.name=test",
        "commit", "-qm", "test")
    with pytest.raises(FactumError) as excinfo:
        invoke(
            state.repo, "--at", "HEAD", "update", record_id,
            "--actor", "agent:updater", "--set", "tags.status=confirmed",
        )
    assert excinfo.value.code == "READ_ONLY"


# ---------------------------------------------------------------------------
# Recovery
# ---------------------------------------------------------------------------

def test_update_noop_returns_current_unchanged(state):
    record_id = _add(state)
    first = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", {"status": "confirmed"}
    )
    second = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", {"status": "confirmed"}
    )
    assert second["fingerprint"] == first["fingerprint"]
    assert second["tags"] == first["tags"]


def test_concurrent_updates_merge(state):
    record_id = _add(state)
    export_pending(_fresh(state.repo))
    count = 8
    barrier = threading.Barrier(count)
    errors = []

    def worker(index):
        try:
            barrier.wait(timeout=30)
            worker_state = State(state.repo).load()
            store.update_record(
                worker_state, record_id, f"agent:worker-{index}",
                [(f"tags.tag-{index}", index)],
            )
        except Exception as error:  # noqa: BLE001 - collected for assertion
            errors.append(error)

    threads = [threading.Thread(target=worker, args=(index,)) for index in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=120)

    assert not errors, errors
    tags = _record(state.repo, record_id)["tags"]
    for index in range(count):
        assert tags[f"tag-{index}"] == index
    _assert_manifest_consistent(state.repo)
    _fresh(state.repo)


def test_fingerprint_recomputed_after_update(state):
    record_id = _add(state)
    before = _record(state.repo, record_id)
    updated = store.update_record(
        _fresh(state.repo), record_id, "agent:updater", {"status": "confirmed"}
    )
    assert updated["fingerprint"] != before["fingerprint"]
    unsigned = {key: value for key, value in updated.items() if key != "fingerprint"}
    assert store.digest(unsigned) == updated["fingerprint"]


def test_reprojection_after_update(state, tmp_path):
    record_id = _add(state)
    store.update_record(
        _fresh(state.repo), record_id, "agent:updater", {"status": "confirmed"}
    )
    state.db_path.unlink()
    rebuilt = _fresh(state.repo)
    rebuilt.project()
    assert invoke(state.repo, "get", record_id)["record"]["tags"]["status"] == "confirmed"
    query_path = tmp_path / "query.json"
    query_path.write_text(json.dumps({"kind": "observable", "tags": {"status": "confirmed"}}))
    result = invoke(state.repo, "query", "--input", str(query_path))
    assert result["count"] >= 1
    assert record_id in {record["id"] for record in result["records"]}


# ---------------------------------------------------------------------------
# CLI --set parsing (Dev 2)
# ---------------------------------------------------------------------------

def test_update_cli_set_flag_end_to_end(state):
    record_id = _add(state, tags={"lane": "old"})
    result = invoke(
        state.repo, "update", record_id, "--actor", "agent:editor",
        "--set", "tags.reviewed=true", "--set", "tags.lane=null",
    )
    assert result["updated"] is True
    tags = _record(state.repo, record_id)["tags"]
    assert tags["reviewed"] is True
    assert "lane" not in tags
    assert tags["factum.updated_by"] == "agent:editor"


def test_update_cli_set_noop(state):
    record_id = _add(state, tags={"reviewed": True})
    result = invoke(
        state.repo, "update", record_id, "--actor", "agent:editor",
        "--set", "tags.reviewed=true",
    )
    assert result["updated"] is False


@pytest.mark.parametrize("flag", ["tags.x", "tags.x={bad json", "=1", ""])
def test_update_cli_set_rejects_bad_syntax(state, flag):
    record_id = _add(state)
    with pytest.raises(FactumError) as excinfo:
        invoke(
            state.repo, "update", record_id, "--actor", "agent:editor",
            "--set", flag,
        )
    assert excinfo.value.code == "SET"


def test_update_cli_tags_flag(state):
    record_id = _add(state)
    result = invoke(
        state.repo, "update", record_id, "--actor", "agent:editor",
        "--tags", '{"reviewed": true, "stale": null}',
    )
    assert result["updated"] is True
    assert _record(state.repo, record_id)["tags"]["reviewed"] is True
