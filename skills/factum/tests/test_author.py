"""Author-tag (factum.author) behavior and its immutability contract.

These tests pin the system-assigned `tags["factum.author"]` field for the
future `update` command (Dev 2): the update implementation must reject any
change to this key with EVIDENCE_EDIT. See store.AUTHOR_TAG.
"""

import copy

import pytest

from factum_lib import store
from factum_lib.schemas import SchemaError
from factum_lib.store import FactumError, State, add_bundle


def test_author_tag_set_from_bundle_actor(state, bundle):
    result = add_bundle(state, bundle)
    record = State(state.repo).load().records[result["ids"]["value"]]
    assert record["tags"][store.AUTHOR_TAG] == "agent:synthetic"


def test_author_tag_rejects_submitter_value(state, bundle):
    bundle["records"][0]["tags"] = {store.AUTHOR_TAG: "agent:impostor"}
    with pytest.raises(FactumError) as excinfo:
        add_bundle(state, bundle)
    assert excinfo.value.code == "EVIDENCE_EDIT"


def test_reserved_tag_prefix_rejected_at_creation(state, bundle):
    bundle["records"][0]["tags"] = {"factum.custom": "nope"}
    with pytest.raises(FactumError) as excinfo:
        add_bundle(state, bundle)
    assert excinfo.value.code == "EVIDENCE_EDIT"


def test_make_record_rejects_reserved_tags():
    with pytest.raises(FactumError) as excinfo:
        store.make_record(
            "observation", {"type": "t"}, "agent:synthetic",
            {"factum.author": "agent:impostor"},
        )
    assert excinfo.value.code == "EVIDENCE_EDIT"


def test_author_tag_covered_by_fingerprint(state, bundle):
    result = add_bundle(state, bundle)
    record = State(state.repo).load().records[result["ids"]["value"]]
    unsigned = {key: value for key, value in record.items() if key != "fingerprint"}
    assert store.digest(unsigned) == record["fingerprint"]


def test_tampered_author_tag_breaks_fingerprint(state, bundle):
    result = add_bundle(state, bundle)
    tampered = copy.deepcopy(State(state.repo).load().records[result["ids"]["value"]])
    tampered["tags"][store.AUTHOR_TAG] = "agent:impostor"
    with pytest.raises(FactumError) as excinfo:
        State(state.repo).load().insert_record(tampered)
    assert excinfo.value.code == "HASH"


def test_author_tag_set_on_tagless_records():
    record = store.make_record("observation", {"type": "t"}, "agent:synthetic")
    assert record["tags"] == {store.AUTHOR_TAG: "agent:synthetic"}


def test_make_record_does_not_mutate_submitter_tags():
    submitted = {"lane": "webhook-deaddrops"}
    store.make_record("observation", {"type": "t"}, "agent:synthetic", submitted)
    assert submitted == {"lane": "webhook-deaddrops"}


@pytest.mark.parametrize("actor", [None, ""])
def test_make_record_rejects_empty_actor(actor):
    with pytest.raises(FactumError) as excinfo:
        store.make_record("observation", {"type": "t"}, actor)
    assert excinfo.value.code == "IDENTITY"


def test_empty_bundle_actor_rejected(state, bundle):
    bundle["actor"] = ""
    with pytest.raises(SchemaError):
        add_bundle(state, bundle)
