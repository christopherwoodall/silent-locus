from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urldefrag, urlparse

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource


DRAFT = "https://json-schema.org/draft/2020-12/schema"

KINDS = (
    "source", "artifact", "observation", "observable", "sighting",
    "event", "claim", "edge", "assessment", "run", "retraction",
)

CORE = {
    name: f"urn:factum:core:{name}:1"
    for name in (*KINDS, "record", "bundle", "lane")
}


class SchemaError(Exception):
    pass


def canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise SchemaError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid(value):
        raise SchemaError(f"Invalid JSON number: {value}")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def read_json(path):
    return parse_json(Path(path).read_bytes())


def no_symlink_path(path):
    """Reject a symlink at any component before managed filesystem access."""
    path = Path(path).absolute()
    for component in (*reversed(path.parents), path):
        if component.is_symlink():
            raise SchemaError(f"Symlinked managed path: {component}")
    return path


def checked_path(root, relative):
    relative = safe_relative(relative)
    root = no_symlink_path(root)
    path = no_symlink_path(root / relative)
    if root.resolve() not in path.resolve().parents:
        raise SchemaError(f"Path escapes its root: {relative}")
    return path


def write_json_atomic(path, value):
    path = no_symlink_path(path)
    durable_mkdir(path.parent)
    fd, temporary = tempfile.mkstemp(prefix=".factum-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write((canonical(value) + "\n").encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sync_directory(path):
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def durable_mkdir(path):
    """Persist newly created directory entries as well as their eventual files."""
    path = no_symlink_path(path)
    missing = []
    current = path
    while not current.exists():
        missing.append(current)
        current = current.parent
    path.mkdir(parents=True, exist_ok=True)
    for directory in reversed(missing):
        sync_directory(directory.parent)


def safe_relative(value):
    if not isinstance(value, str):
        raise SchemaError("Pack paths must be strings.")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or ".." in path.parts
        or "\\" in value
        or not path.parts
        or str(path) != value
    ):
        raise SchemaError(f"Unsafe pack path: {value}")
    return value


def manifest_validate(value):
    expected = {
        "pack_format", "name", "version", "requires",
        "schemas", "definitions", "tags",
    }
    if not isinstance(value, dict) or set(value) != expected:
        raise SchemaError("Invalid pack manifest fields.")
    if value["pack_format"] != 1:
        raise SchemaError("Unsupported pack format.")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", value["name"]):
        raise SchemaError("Invalid pack name.")
    if not re.fullmatch(r"\d+\.\d+\.\d+", value["version"]):
        raise SchemaError("Version must be major.minor.patch.")
    if not isinstance(value["requires"], dict):
        raise SchemaError("requires must be an object.")
    for name, version in value["requires"].items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise SchemaError("Invalid dependency name.")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise SchemaError("Dependencies must use exact versions.")
    if not isinstance(value["tags"], dict):
        raise SchemaError("Pack tags must be an object.")

    paths = []
    for field in ("schemas", "definitions"):
        if not isinstance(value[field], list):
            raise SchemaError(f"{field} must be an array.")
        paths.extend(safe_relative(path) for path in value[field])
    if len(paths) != len(set(paths)) or "pack.json" in paths:
        raise SchemaError("Duplicate or reserved pack path.")


def pack_inventory(directory):
    directory = no_symlink_path(directory).resolve()
    manifest_path = directory / "pack.json"
    if manifest_path.is_symlink():
        raise SchemaError("Symlinked pack files are not permitted.")
    manifest = read_json(manifest_path)
    manifest_validate(manifest)

    names = ["pack.json", *manifest["schemas"], *manifest["definitions"]]
    files = {}
    for name in names:
        path = checked_path(directory, name)
        if not path.is_file() or path.is_symlink():
            raise SchemaError(f"Missing or symlinked pack file: {name}")
        if directory not in path.resolve().parents:
            raise SchemaError(f"Pack file escapes its directory: {name}")
        files[name] = sha256(path.read_bytes())

    return {
        "name": manifest["name"],
        "version": manifest["version"],
        "path": f"schema-packs/{manifest['name']}/{manifest['version']}",
        "files": files,
    }


def reject_retrieval(uri):
    raise NoSuchResource(ref=uri)


class Catalog:
    def __init__(self, read, lock):
        self.read = read
        self.lock = lock
        self.documents = {}
        self.definitions = {
            "observable": {},
            "observation": {},
            "event": {},
            "predicate": {},
        }
        self.manifests = {}

        if (
            not isinstance(lock, dict)
            or set(lock) != {"lock_format", "packs", "tags"}
            or lock["lock_format"] != 1
            or not isinstance(lock["packs"], list)
            or not isinstance(lock["tags"], dict)
        ):
            raise SchemaError("Invalid schema lock.")

        loaded_definitions = []

        for entry in lock["packs"]:
            if set(entry) != {"name", "version", "path", "files"}:
                raise SchemaError("Invalid locked pack entry.")
            expected_path = f"schema-packs/{entry['name']}/{entry['version']}"
            if entry["path"] != expected_path:
                raise SchemaError("Locked pack path is invalid.")

            key = (entry["name"], entry["version"])
            if key in self.manifests:
                raise SchemaError(f"Duplicate locked pack: {key}")

            contents = {}
            for relative, expected_hash in entry["files"].items():
                safe_relative(relative)
                raw = read(f"data/{entry['path']}/{relative}")
                if sha256(raw) != expected_hash:
                    raise SchemaError(f"Schema drift: {entry['path']}/{relative}")
                contents[relative] = parse_json(raw)

            manifest = contents.get("pack.json")
            manifest_validate(manifest)
            if (manifest["name"], manifest["version"]) != key:
                raise SchemaError("Manifest identity differs from lock.")

            listed = {"pack.json", *manifest["schemas"], *manifest["definitions"]}
            if listed != set(contents):
                raise SchemaError("Lock file inventory differs from manifest.")
            self.manifests[key] = manifest

            for path in manifest["schemas"]:
                schema = contents[path]
                Draft202012Validator.check_schema(schema)
                schema_id = schema.get("$id")
                if (
                    schema.get("$schema") != DRAFT
                    or not isinstance(schema_id, str)
                    or not urlparse(schema_id).scheme
                    or "#" in schema_id
                ):
                    raise SchemaError("Schemas need Draft 2020-12 and an absolute $id.")
                if schema_id in self.documents:
                    raise SchemaError(f"Duplicate schema ID: {schema_id}")
                self.documents[schema_id] = schema

            for path in manifest["definitions"]:
                document = contents[path]
                if (
                    not isinstance(document, dict)
                    or set(document) != {"definitions", "tags"}
                    or not isinstance(document["definitions"], list)
                    or not isinstance(document["tags"], dict)
                ):
                    raise SchemaError(f"Invalid definitions file: {path}")
                loaded_definitions.extend(document["definitions"])

        for manifest in self.manifests.values():
            for name, version in manifest["requires"].items():
                if (name, version) not in self.manifests:
                    raise SchemaError(f"Missing pack dependency: {name}@{version}")

        resources = [
            (schema_id, Resource.from_contents(schema))
            for schema_id, schema in self.documents.items()
        ]
        self.registry = Registry(retrieve=reject_retrieval).with_resources(resources)

        for schema_id, schema in self.documents.items():
            self.inspect_schema(schema, schema_id)

        for definition in loaded_definitions:
            self.add_definition(definition)

        for schema_id in CORE.values():
            if schema_id not in self.documents:
                raise SchemaError(f"Missing core schema: {schema_id}")

    @classmethod
    def from_repo(cls, repo):
        repo = Path(repo)
        return cls(
            lambda path: checked_path(repo, path).read_bytes(),
            read_json(checked_path(repo, "data/schema-lock.json")),
        )

    def resolve(self, reference, base):
        if reference.startswith("#"):
            target = base
            fragment = reference[1:]
        else:
            if not urlparse(reference).scheme:
                raise SchemaError("Use absolute schema references or local # pointers.")
            target, fragment = urldefrag(reference)

        if target not in self.documents:
            raise SchemaError(f"Uninstalled schema reference: {target}")

        value = self.documents[target]
        if fragment:
            if not fragment.startswith("/"):
                raise SchemaError("Only JSON Pointer fragments are supported.")
            for token in fragment[1:].split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                try:
                    value = value[int(token)] if isinstance(value, list) else value[token]
                except (KeyError, IndexError, ValueError, TypeError) as error:
                    raise SchemaError(f"Invalid schema pointer: {reference}") from error
        return value, target

    def contains_reference_annotation(self, value, base, seen=None):
        seen = set() if seen is None else seen
        if isinstance(value, dict):
            if "x-factum-target-kinds" in value:
                return True
            if "$ref" in value:
                key = (base, value["$ref"])
                if key not in seen:
                    seen.add(key)
                    target, target_base = self.resolve(value["$ref"], base)
                    if self.contains_reference_annotation(target, target_base, seen):
                        return True
            return any(
                self.contains_reference_annotation(child, base, seen)
                for _, child in self.schema_children(value)
            )
        return False

    @staticmethod
    def schema_children(schema):
        """Yield schema locations, never instance data or property-name maps."""
        maps = ("properties", "patternProperties", "$defs", "dependentSchemas")
        arrays = ("allOf", "anyOf", "oneOf", "prefixItems")
        singles = (
            "items", "additionalProperties", "unevaluatedProperties",
            "additionalItems", "unevaluatedItems", "contains",
            "propertyNames", "if", "then", "else", "not", "contentSchema",
        )
        for keyword in maps:
            for child in schema.get(keyword, {}).values():
                yield keyword, child
        for keyword in arrays:
            for child in schema.get(keyword, []):
                yield keyword, child
        for keyword in singles:
            if keyword in schema:
                yield keyword, schema[keyword]

    def inspect_schema(self, value, base, root=True):
        if isinstance(value, dict):
            if not root and "$id" in value:
                raise SchemaError("Nested $id declarations are unsupported.")
            if "$dynamicRef" in value or "$dynamicAnchor" in value:
                raise SchemaError("Dynamic schema references are unsupported.")

            if "$ref" in value:
                self.resolve(value["$ref"], base)

            if "x-factum-target-kinds" in value:
                kinds = value["x-factum-target-kinds"]
                if (
                    not isinstance(kinds, list)
                    or not kinds
                    or not all(isinstance(item, str) for item in kinds)
                    or not set(kinds) <= {*KINDS, "lane", "*"}
                ):
                    raise SchemaError("Invalid x-factum-target-kinds annotation.")

            unsupported = {
                "oneOf", "anyOf", "if", "then", "else", "not",
                "patternProperties", "additionalProperties",
                "unevaluatedProperties", "contains", "dependentSchemas",
                "propertyNames", "unevaluatedItems", "additionalItems", "contentSchema",
            }
            for keyword, child in self.schema_children(value):
                if keyword in unsupported and self.contains_reference_annotation(child, base):
                    raise SchemaError(
                        f"Reference annotations under {keyword} are unsupported; "
                        "put reference fields in properties/items/allOf."
                    )

                self.inspect_schema(child, base, root=False)

    def add_definition(self, definition):
        if not isinstance(definition, dict):
            raise SchemaError("Type definitions must be objects.")
        category = definition.get("category")
        name = definition.get("name")
        if category not in self.definitions:
            raise SchemaError(f"Unknown definition category: {category}")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_.-]*", name):
            raise SchemaError("Invalid type name.")
        if name in self.definitions[category]:
            raise SchemaError(f"Duplicate type assignment: {category}/{name}")

        common = {"category", "name", "description", "tags"}
        if category == "predicate":
            allowed = common | {"structural", "subject", "object"}
            if type(definition.get("structural", False)) is not bool:
                raise SchemaError("Predicate structural must be boolean.")
            for endpoint in ("subject", "object"):
                if endpoint in definition:
                    kinds = definition[endpoint]
                    if (
                        not isinstance(kinds, list)
                        or not kinds
                        or not set(kinds) <= {*KINDS, "lane"}
                    ):
                        raise SchemaError("Invalid predicate endpoint kinds.")
        else:
            allowed = common | {"schema"}
            schema_id = definition.get("schema")
            if schema_id not in self.documents:
                raise SchemaError(f"Unknown assigned schema: {schema_id}")
            if category == "observable":
                allowed |= {"normalizer"}
                if definition.get("normalizer", "none") not in {"none", "casefold"}:
                    raise SchemaError("Unsupported normalizer.")
                if self.documents[schema_id].get("type") != "string":
                    raise SchemaError("Observable value schemas must describe strings.")
            elif self.documents[schema_id].get("type") != "object":
                raise SchemaError("Observation/event schemas must describe objects.")

        if set(definition) - allowed:
            raise SchemaError(f"Unknown definition fields: {set(definition) - allowed}")
        if not isinstance(definition.get("tags", {}), dict):
            raise SchemaError("Definition tags must be an object.")

        self.definitions[category][name] = definition

    def definition(self, category, name):
        try:
            return self.definitions[category][name]
        except KeyError as error:
            raise SchemaError(f"Unknown {category} type: {name}") from error

    def validate(self, schema_id, value):
        if schema_id not in self.documents:
            raise SchemaError(f"Unknown schema: {schema_id}")
        validator = Draft202012Validator(
            self.documents[schema_id],
            registry=self.registry,
            format_checker=FormatChecker(),
        )
        errors = sorted(
            validator.iter_errors(value),
            key=lambda item: "/".join(map(str, item.absolute_path)),
        )
        if errors:
            error = errors[0]
            path = "/".join(map(str, error.absolute_path))
            # Validator messages can contain raw evidence, including tokens.
            raise SchemaError(f"{schema_id}/{path}: validation failed ({error.validator}).")

    def assign(self, kind, body):
        if kind == "observable":
            category, type_key, schema_key = "observable", "type", "value_schema"
        elif kind == "observation":
            category, type_key, schema_key = "observation", "type", "data_schema"
        elif kind == "event":
            category, type_key, schema_key = "event", "event_type", "data_schema"
        else:
            return

        definition = self.definition(category, body.get(type_key))
        expected = definition["schema"]
        if schema_key in body and body[schema_key] != expected:
            raise SchemaError(
                f"{body[type_key]} is assigned to {expected}, not {body[schema_key]}"
            )
        body[schema_key] = expected

    def validate_body(self, kind, body):
        self.validate(CORE[kind], body)
        if kind in {"observable", "observation", "event"}:
            assigned = copy.deepcopy(body)
            self.assign(kind, assigned)
            if assigned != body:
                raise SchemaError("Stored record is missing its assigned schema.")
            if kind == "observable":
                self.validate(body["value_schema"], body["value"])
            else:
                self.validate(body["data_schema"], body["data"])

        if kind == "edge":
            definition = self.definition("predicate", body["predicate"])
            if not definition.get("structural", False):
                if "basis" not in body or not body.get("cites"):
                    raise SchemaError("Interpretive edges require basis and citations.")

    def walk_references(self, schema_id, value, callback):
        def walk(schema, item, base, depth=0):
            if depth > 100:
                raise SchemaError("Schema/reference traversal depth exceeded.")
            if not isinstance(schema, dict):
                return item

            if "$ref" in schema:
                target, target_base = self.resolve(schema["$ref"], base)
                item = walk(target, item, target_base, depth + 1)

            if "x-factum-target-kinds" in schema:
                item = callback(item, schema["x-factum-target-kinds"])

            for child in schema.get("allOf", []):
                item = walk(child, item, base, depth + 1)

            if isinstance(item, dict):
                for key, child in schema.get("properties", {}).items():
                    if key in item:
                        item[key] = walk(child, item[key], base, depth + 1)

            if isinstance(item, list):
                prefix = schema.get("prefixItems", [])
                for index, child in enumerate(prefix):
                    if index < len(item):
                        item[index] = walk(child, item[index], base, depth + 1)
                child = schema.get("items")
                if isinstance(child, dict):
                    for index in range(len(prefix), len(item)):
                        item[index] = walk(child, item[index], base, depth + 1)
            return item

        return walk(self.documents[schema_id], value, schema_id)

    def body_references(self, kind, body, callback):
        self.walk_references(CORE[kind], body, callback)
        if kind in {"observation", "event"}:
            self.walk_references(body["data_schema"], body["data"], callback)
        return body

    def match_key(self, value_type, value):
        definition = self.definitions["observable"].get(value_type, {})
        if definition.get("normalizer") == "casefold":
            return value.casefold()
        return value


def install_pack(repo, source, approve=False):
    repo = Path(repo)
    source = no_symlink_path(source).resolve()
    lock_path = checked_path(repo, "data/schema-lock.json")
    lock = read_json(lock_path)
    entry = pack_inventory(source)

    existing = [
        item for item in lock["packs"]
        if (item["name"], item["version"]) == (entry["name"], entry["version"])
    ]
    if existing:
        if existing[0] != entry:
            raise SchemaError("An installed pack version cannot be changed.")
        return {"installed": False, "already_present": True, "pack": entry}

    proposed = copy.deepcopy(lock)
    proposed["packs"].append(entry)
    proposed["packs"].sort(key=lambda item: (item["name"], item["version"]))

    destination = checked_path(repo, "data/" + entry["path"])
    prefix = f"data/{entry['path']}/"

    def proposed_read(path):
        if path.startswith(prefix):
            return checked_path(source, path.removeprefix(prefix)).read_bytes()
        return checked_path(repo, path).read_bytes()

    Catalog(proposed_read, proposed)

    if not approve:
        return {"installed": False, "valid": True, "requires": "--approve", "pack": entry}

    durable_mkdir(destination.parent)

    if destination.exists():
        if pack_inventory(destination) != entry:
            raise SchemaError("Unactivated destination differs from proposed pack.")
    else:
        stage = Path(tempfile.mkdtemp(prefix=".pack-", dir=destination.parent))
        try:
            for relative in entry["files"]:
                target = stage / relative
                durable_mkdir(target.parent)
                shutil.copyfile(checked_path(source, relative), target)
                with target.open("rb") as stream:
                    os.fsync(stream.fileno())
                sync_directory(target.parent)
            if pack_inventory(stage) != entry:
                raise SchemaError("Pack changed during installation.")
            os.replace(stage, destination)
            sync_directory(destination.parent)
        finally:
            if stage.exists():
                shutil.rmtree(stage)

    # The lock is the activation point. Unlocked directories are ignored.
    write_json_atomic(lock_path, proposed)
    return {"installed": True, "pack": entry}