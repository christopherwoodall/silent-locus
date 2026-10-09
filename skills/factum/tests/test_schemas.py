import json
import shutil

import pytest

from factum_lib.schemas import Catalog, SchemaError, install_pack, pack_inventory, read_json
from factum_lib.store import FactumError, State, add_bundle
from tools.validation_support import ROOT


@pytest.fixture
def pack(tmp_path):
    destination = tmp_path / "proposal"
    shutil.copytree(ROOT / "examples/pack/1.0.0", destination)
    return destination


def edit(path, change):
    value = read_json(path)
    change(value)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def install(repo, pack):
    install_pack(repo, pack, True)
    return State(repo).load()


def test_preview_activation_and_idempotent_install(repo, pack):
    original = (repo / "data/schema-lock.json").read_bytes()
    assert install_pack(repo, pack)["valid"]
    assert (repo / "data/schema-lock.json").read_bytes() == original
    assert not (repo / "data/schema-packs/factum-example").exists()
    assert install_pack(repo, pack, True)["installed"]
    assert install_pack(repo, pack, True)["already_present"]
    assert Catalog.from_repo(repo).definition("observation", "example.capture")["schema"] == "urn:factum:example:capture:1"


@pytest.mark.parametrize("name", ["items", "allOf", "additionalProperties", "$id", "$ref", "oneOf"])
def test_keyword_like_property_names_are_not_schemas(repo, pack, name):
    edit(pack / "schemas/observation.json", lambda s: s["properties"].update({
        name: {"$ref": "urn:factum:core:common:1#/$defs/id", "x-factum-target-kinds": ["artifact"]}
    }))
    install(repo, pack)


def test_example_data_is_not_inspected_as_schema(repo, pack):
    edit(pack / "schemas/observation.json", lambda s: s.update({
        "examples": [{"$id": "literal", "$ref": "https://not-installed.invalid/schema", "x-factum-target-kinds": "literal"}],
        "default": {"$dynamicRef": "literal"}, "const": {"$id": "literal"},
    }))
    install(repo, pack)


@pytest.mark.parametrize("keyword", ["oneOf", "anyOf", "if", "then", "else", "not", "patternProperties", "additionalProperties", "unevaluatedProperties", "contains", "dependentSchemas", "propertyNames"])
def test_unsupported_reference_locations_fail(repo, pack, keyword):
    reference = {"type": "string", "x-factum-target-kinds": ["artifact"]}
    value = [reference] if keyword in {"oneOf", "anyOf"} else {"x": reference} if keyword in {"patternProperties", "dependentSchemas"} else reference
    edit(pack / "schemas/observation.json", lambda s: s.update({keyword: value}))
    with pytest.raises(SchemaError):
        install_pack(repo, pack)


@pytest.mark.parametrize("case", ["dependency", "manifest", "missing", "traversal", "remote", "pointer", "duplicate-id", "duplicate-type", "dynamic", "nested-id", "kind", "dialect"])
def test_invalid_packs_rejected(repo, pack, case):
    schema = pack / "schemas/observation.json"
    if case == "dependency":
        edit(pack / "pack.json", lambda v: v["requires"].update({"factum-core": "9.9.9"}))
    elif case == "manifest":
        edit(pack / "pack.json", lambda v: v.update({"unexpected": True}))
    elif case == "missing":
        schema.unlink()
    elif case == "traversal":
        edit(pack / "pack.json", lambda v: v["schemas"].append("../escape.json"))
    elif case == "remote":
        edit(schema, lambda v: v.update({"$ref": "https://not-installed.invalid/schema"}))
    elif case == "pointer":
        edit(schema, lambda v: v.update({"$ref": "#/$defs/absent"}))
    elif case == "duplicate-id":
        edit(schema, lambda v: v.update({"$id": "urn:factum:core:source:1"}))
    elif case == "duplicate-type":
        edit(pack / "definitions.json", lambda v: v["definitions"].append({"category": "observable", "name": "domain", "schema": "urn:factum:example:value:1", "tags": {}}))
    elif case == "dynamic":
        edit(schema, lambda v: v.update({"$dynamicRef": "#foo"}))
    elif case == "nested-id":
        edit(schema, lambda v: v["properties"].update({"x": {"$id": "urn:bad:nested", "type": "string"}}))
    elif case == "kind":
        edit(schema, lambda v: v["properties"]["artifact"].update({"x-factum-target-kinds": ["unknown"]}))
    elif case == "dialect":
        edit(schema, lambda v: v.update({"$schema": "http://json-schema.org/draft-07/schema#"}))
    with pytest.raises((SchemaError, FileNotFoundError)):
        install_pack(repo, pack)


@pytest.mark.parametrize("ancestor", [False, True])
def test_pack_symlink_escape(repo, pack, tmp_path, ancestor):
    outside = tmp_path / "outside"
    outside.mkdir()
    shutil.copyfile(pack / "schemas/observation.json", outside / "observation.json")
    if ancestor:
        shutil.rmtree(pack / "schemas")
        (pack / "schemas").symlink_to(outside, target_is_directory=True)
    else:
        (pack / "schemas/observation.json").unlink()
        (pack / "schemas/observation.json").symlink_to(outside / "observation.json")
    with pytest.raises(SchemaError):
        pack_inventory(pack)


def test_installed_drift_and_changed_candidate(repo, pack):
    install(repo, pack)
    edit(pack / "schemas/value.json", lambda v: v.update({"description": "changed"}))
    with pytest.raises(SchemaError, match="cannot be changed"):
        install_pack(repo, pack, True)
    installed = repo / "data/schema-packs/factum-example/1.0.0/schemas/value.json"
    installed.write_bytes(installed.read_bytes() + b" ")
    with pytest.raises(SchemaError, match="drift"):
        State(repo).load()


def test_additive_version_and_breaking_identity(repo, pack):
    install(repo, pack)
    edit(pack / "pack.json", lambda v: v.update({"version": "2.0.0"}))
    with pytest.raises(SchemaError, match="Duplicate"):
        install_pack(repo, pack)
    edit(pack / "pack.json", lambda v: v.update({"requires": {"factum-core": "1.0.0", "factum-example": "1.0.0"}}))
    for path in (pack / "schemas").glob("*.json"):
        edit(path, lambda v: v.update({"$id": v["$id"].replace(":1", ":2")}))
    edit(pack / "definitions.json", lambda v: [
        d.update({"name": d["name"] + ".v2", **({"schema": d["schema"].replace(":1", ":2")} if "schema" in d else {})})
        for d in v["definitions"]
    ])
    updated = install(repo, pack)
    assert updated.catalog.definition("observable", "example.exact")["schema"].endswith(":1")
    assert updated.catalog.definition("observable", "example.exact.v2")["schema"].endswith(":2")


def example_bundle():
    bundle = read_json(ROOT / "examples/bundle.json")
    bundle["files"][0]["path"] = str(ROOT / "examples/capture.txt")
    return bundle


def test_custom_references_and_literal_values(repo, pack):
    state = install(repo, pack)
    result = add_bundle(state, example_bundle())
    records = State(repo).load().records
    observation = records[result["ids"]["observation"]]["body"]
    assert observation["data"]["artifact"] == result["ids"]["file"]
    assert observation["data"]["items"] == "@source"
    assert records[result["ids"]["claim"]]["body"]["value"] == {"literal": "@source"}
    assert records[result["ids"]["observation"]]["tags"]["literal"] == "@source"


@pytest.mark.parametrize("case", ["wrong-kind", "dangling", "unknown-local", "extra", "missing-basis", "missing-cites", "endpoint"])
def test_custom_bundle_negative_semantics(repo, pack, case):
    state = install(repo, pack)
    bundle = example_bundle()
    body = bundle["records"][1]["body"]
    if case == "wrong-kind":
        body["data"]["artifact"] = "@source"
    elif case == "dangling":
        body["data"]["artifact"] = "artifact_" + "0" * 32
    elif case == "unknown-local":
        body["data"]["artifact"] = "@missing"
    elif case == "extra":
        body["data"]["extra"] = True
    elif case == "missing-basis":
        del bundle["records"][-1]["body"]["basis"]
    elif case == "missing-cites":
        del bundle["records"][-1]["body"]["cites"]
    elif case == "endpoint":
        bundle["records"][-2]["body"]["subject"] = "@source"
    with pytest.raises((SchemaError, FactumError)):
        add_bundle(state, bundle)
    assert not State(repo).load().records


@pytest.mark.parametrize("assignment", ["omitted", "matching", "conflicting"])
def test_value_schema_assignment(state, bundle, assignment):
    if assignment != "omitted":
        bundle["records"][0]["body"]["value_schema"] = "urn:factum:core:raw-string:1" if assignment == "matching" else "urn:factum:core:empty:1"
    if assignment == "conflicting":
        with pytest.raises(SchemaError):
            add_bundle(state, bundle)
    else:
        result = add_bundle(state, bundle)
        assert State(state.repo).load().records[result["ids"]["value"]]["body"]["value_schema"] == "urn:factum:core:raw-string:1"
