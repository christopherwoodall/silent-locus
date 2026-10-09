from __future__ import annotations

import argparse
import copy
import re
import sqlite3
from datetime import date
from pathlib import Path

from filelock import FileLock, Timeout
from rapidfuzz.fuzz import ratio

from . import FORMAT_VERSION, TOOLKIT_VERSION
from .schemas import (
    CORE, KINDS, SchemaError, canonical, install_pack,
    parse_json, read_json, write_json_atomic,
    checked_path,
    durable_mkdir,
)
from .store import (
    FactumError, State, add_bundle, atomic_bytes, export_pending,
    fail, head, initialize, new_id, now, resolve_repo,
)


EXTRACTORS = {
    "url": r"""https?://[^\s<>"']+""",
    "domain": r"\b(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,63}\b",
    "ipv4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "sha256": r"\b[0-9A-Fa-f]{64}\b",
    "email": r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}\b",
}
EXTRACTOR_VERSION = "regex-substrings/1"


def emit(value, ok=True):
    print(canonical({"ok": ok, **value}))


def parse_tags(value):
    result = {} if value is None else parse_json(value)
    if not isinstance(result, dict):
        fail("TAGS", "tags must be a JSON object.")
    return result


def scope(state):
    return {
        "commit": state.revision or head(state.repo),
        "state_digest": state.state_digest,
        "pending_batches": len(state.pending),
        "coverage": "Structured Factum records; excludes unimported files and live sources.",
        "policy": "match/2",
    }


def base_bundle(args):
    return {
        "bundle": FORMAT_VERSION,
        "idempotency_key": args.key,
        "actor": args.actor,
        "tags": parse_tags(getattr(args, "tags", None)),
        "records": [],
    }


def capture(state, args):
    if bool(args.url) == bool(args.dataset):
        fail("CAPTURE", "Supply exactly one of --url or --dataset.")
    if args.file and args.storage is None:
        fail("CAPTURE", "Submitted files require --storage git or local.")
    if args.url and not args.file:
        fail("CAPTURE", "A web capture requires submitted bytes.")

    bundle = base_bundle(args)
    if args.lane:
        bundle["lane"] = args.lane
    bundle["files"] = []
    bundle["records"].append({
        "ref": "source",
        "kind": "source",
        "body": {
            "source_type": "web" if args.url else "dataset",
            "locator": args.url or args.dataset,
        },
    })

    bindings = []
    for index, filename in enumerate(args.file or []):
        ref = f"file{index}"
        bundle["files"].append({
            "ref": ref,
            "path": filename,
            "storage": args.storage,
        })
        bindings.append({
            "artifact": "@" + ref,
            "filename": Path(filename).name,
            "role": "body" if args.url else "dataset",
        })

    if args.dataset and not bindings:
        reference = {"uri": args.dataset}
        if args.revision:
            reference["revision"] = args.revision
        bundle["records"].append({
            "ref": "reference",
            "kind": "artifact",
            "body": {"reference": reference},
        })
        bindings.append({"artifact": "@reference", "role": "dataset"})

    if args.url:
        payload = {"requested_url": args.url, "capture_kind": "submitted"}
        if args.final_url is not None:
            payload["final_url"] = args.final_url
        if args.status is not None:
            payload["http_status"] = args.status
        type_name = "web.capture"
    else:
        payload = {"dataset_uri": args.dataset, "coverage": args.coverage}
        if args.revision:
            payload["revision"] = args.revision
        type_name = "dataset.snapshot"

    body = {
        "type": type_name,
        "source": "@source",
        "files": bindings,
        "data": payload,
    }
    if args.observed_at:
        body["observed_at"] = args.observed_at
        body["time_basis"] = "collector_clock"

    bundle["records"].append({
        "ref": "observation",
        "kind": "observation",
        "body": body,
        "tags": parse_tags(args.tags),
    })
    return add_bundle(state, bundle)


def match(state, args):
    query = read_json(args.input) if args.input else {
        "value": args.value or args.url or args.sha256 or args.text,
        "type": args.type or ("url" if args.url else "sha256" if args.sha256 else None),
        "mode": args.mode,
        "limit": args.limit,
    }
    if not isinstance(query, dict) or set(query) - {"value", "type", "mode", "limit"}:
        fail("QUERY", "Allowed fields: value, type, mode, limit.")
    value, value_type = query.get("value"), query.get("type")
    mode, limit = query.get("mode", "exact"), query.get("limit", 25)
    if not isinstance(value, str) or not value:
        fail("QUERY", "A nonempty value is required.")
    if value_type is not None and not isinstance(value_type, str):
        fail("QUERY", "type must be a string.")
    if value_type is not None and value_type not in state.catalog.definitions["observable"] and value_type != "source":
        fail("QUERY", "Unknown search value type.")
    if mode not in {"exact", "key", "fuzzy"}:
        fail("QUERY", "Invalid mode.")
    if type(limit) is not int or not 1 <= limit <= 200:
        fail("QUERY", "limit must be 1..200.")

    db = state.connect()
    try:
        where, params = "raw_value=?", [value]
        if mode == "key":
            if not value_type:
                fail("QUERY", "Key matching requires type.")
            state.catalog.definition("observable", value_type)
            where, params = "value_type=? AND match_key=?", [
                value_type, state.catalog.match_key(value_type, value),
            ]
        elif value_type:
            where += " AND value_type=?"
            params.append(value_type)

        rows = db.execute(
            f"SELECT * FROM search_values WHERE {where} ORDER BY node_id LIMIT 5001",
            params,
        ).fetchall()
        truncated = len(rows) > 5000
        candidates = [dict(row) for row in rows[:5000]]

        if mode == "fuzzy":
            if len(value) < 3:
                fail("QUERY", "Fuzzy matching requires at least three characters.")
            grams = sorted({
                value[index:index + 3]
                for index in range(len(value) - 2)
                if value[index:index + 3].strip()
            })[:32]
            expression = " OR ".join(
                '"' + gram.replace('"', '""') + '"' for gram in grams
            )
            if expression:
                rows = db.execute(
                    "SELECT node_id,raw_value FROM search_fts "
                    "WHERE search_fts MATCH ? ORDER BY rank LIMIT 2001",
                    (expression,),
                ).fetchall()
                truncated = truncated or len(rows) > 2000
                for row in rows[:2000]:
                    for entry in db.execute(
                        "SELECT * FROM search_values WHERE node_id=? AND raw_value=?",
                        (row["node_id"], row["raw_value"]),
                    ):
                        if value_type and entry["value_type"] != value_type:
                            continue
                        if ratio(value, entry["raw_value"]) >= 65:
                            candidates.append(dict(entry))

        matches = {}
        for item in candidates:
            rid = item["node_id"]
            exact = item["raw_value"] == value
            if rid in matches and matches[rid]["match_type"] == "exact":
                continue
            lanes = [
                row[0] for row in db.execute(
                    "SELECT DISTINCT object_id FROM edges "
                    "WHERE subject_id=? AND predicate='in_lane'",
                    (rid,),
                )
            ]
            sightings = [
                record for record in state.records.values()
                if record["record_kind"] == "sighting"
                and record["body"]["observable"] == rid
            ][:10]
            matches[rid] = {
                "id": rid,
                "record_kind": state.records[rid]["record_kind"],
                "value": item["raw_value"],
                "value_type": item["value_type"],
                "match_type": "exact" if exact else mode,
                "score": ratio(value, item["raw_value"]) if mode == "fuzzy" else None,
                "tags": state.records[rid]["tags"],
                "lanes": lanes,
                "sightings": sightings,
                "record": state.records[rid],
            }

        ordered = sorted(
            matches.values(),
            key=lambda item: (
                item["match_type"] != "exact",
                -(item["score"] or 0),
                item["id"],
            ),
        )
        return {
            "status": "found" if ordered else "not_found",
            "matches": ordered[:limit],
            "truncated": truncated or len(ordered) > limit,
            "searched": scope(state),
            "warnings": (
                ["Fuzzy retrieval is heuristic, not an exhaustive absence test."]
                if mode == "fuzzy" else []
            ),
        }
    finally:
        db.close()


def extract(state, args):
    record = state.records.get(args.observation)
    if record is None or record["record_kind"] != "observation":
        fail("OBSERVATION", args.observation)
    types = args.types.split(",")
    if set(types) - set(EXTRACTORS):
        fail("EXTRACTOR", "Unknown extractor.")
    if args.max_bytes < 1 or not 1 <= args.max_matches <= 100000:
        fail("LIMIT", "Invalid extraction limits.")

    attached = {item["artifact"] for item in record["body"]["files"]}
    artifacts = [args.artifact] if args.artifact else sorted(attached)
    if not set(artifacts) <= attached:
        fail("ARTIFACT", "Artifact is not attached to this observation.")

    bundle = base_bundle(args)
    bundle["records"].append({
        "ref": "run",
        "kind": "run",
        "body": {
            "run_kind": "extraction",
            "tool": "factum",
            "tool_version": EXTRACTOR_VERSION,
            "params": {"types": types, "encoding": "utf-8-strict"},
        },
    })

    count = 0
    for artifact_id in artifacts:
        body = state.records[artifact_id]["body"]
        if body.get("size", 0) > args.max_bytes:
            fail("LIMIT", "Artifact exceeds --max-bytes.")
        raw = state.artifact_bytes(artifact_id)
        text = raw.decode("utf-8", errors="strict")
        for type_name in types:
            for found in re.finditer(EXTRACTORS[type_name], text):
                count += 1
                if count > args.max_matches:
                    fail("LIMIT", "Exceeded --max-matches; no records accepted.")
                ref = f"value{count}"
                bundle["records"].extend([
                    {
                        "ref": ref,
                        "kind": "observable",
                        "body": {"type": type_name, "value": found.group(0)},
                    },
                    {
                        "kind": "sighting",
                        "body": {
                            "observable": "@" + ref,
                            "observation": args.observation,
                            "method": f"{EXTRACTOR_VERSION}:{type_name}",
                            "locator": {
                                "artifact": artifact_id,
                                "text_pos": {"start": found.start(), "end": found.end()},
                                "quote": {"exact": found.group(0)},
                            },
                        },
                    },
                    {
                        "kind": "edge",
                        "body": {
                            "subject": "@" + ref,
                            "predicate": "derived_from",
                            "object": args.observation,
                            "basis": "OBSERVED",
                            "cites": ["@run", args.observation],
                        },
                    },
                ])
    return {**add_bundle(state, bundle), "extracted": count}


def graph(state, args):
    if state.kind(args.node) is None:
        fail("NOT_FOUND", args.node)
    if not 0 <= args.depth <= 10 or not 1 <= args.limit <= 2000:
        fail("LIMIT", "Depth must be 0..10 and limit 1..2000.")
    db = state.connect()
    try:
        visited, frontier, edges = {args.node}, {args.node}, {}
        truncated = False
        for _ in range(args.depth):
            following = set()
            for node in sorted(frontier):
                rows = db.execute(
                    "SELECT * FROM edges WHERE subject_id=? OR object_id=? "
                    "ORDER BY id LIMIT ?",
                    (node, node, args.limit + 1),
                )
                for row in rows:
                    if row["id"] in edges:
                        continue
                    if len(edges) >= args.limit:
                        truncated = True
                        break
                    edges[row["id"]] = dict(row)
                    for target in (row["subject_id"], row["object_id"]):
                        if target not in visited:
                            following.add(target)
                if truncated:
                    break
            visited.update(following)
            frontier = following
            if not frontier or truncated:
                break
        if frontier and not truncated:
            # A depth budget can omit edges just as an edge budget can.
            truncated = any(
                row["id"] not in edges
                for node in sorted(frontier)
                for row in db.execute(
                    "SELECT id FROM edges WHERE subject_id=? OR object_id=? "
                    "ORDER BY id LIMIT ?",
                    (node, node, args.limit + 1),
                )
            )
        return {
            "nodes": sorted(visited),
            "edges": list(edges.values()),
            "truncated": truncated,
            "searched": scope(state),
        }
    finally:
        db.close()


def query_records(state, args):
    query = read_json(args.input)
    if not isinstance(query, dict) or set(query) - {"kind", "tags", "limit", "offset", "count"}:
        fail("QUERY", "Allowed fields: kind, tags, limit, offset, count.")
    kind, tags = query.get("kind"), query.get("tags", {})
    limit, offset = query.get("limit", 100), query.get("offset", 0)
    if kind is not None and kind not in KINDS:
        fail("QUERY", "Unknown record kind.")
    if not isinstance(tags, dict):
        fail("QUERY", "tags must be an object.")
    if (
        type(limit) is not int or not 1 <= limit <= 500
        or type(offset) is not int or offset < 0
        or type(query.get("count", False)) is not bool
    ):
        fail("QUERY", "Invalid pagination or count.")

    db = state.connect()
    try:
        sql = "SELECT document FROM records"
        params = []
        if kind:
            sql += " WHERE kind=?"
            params.append(kind)
        sql += " ORDER BY id"
        count, records = 0, []
        for row in db.execute(sql, params):
            record = parse_json(row[0])
            if any(
                key not in record["tags"] or record["tags"][key] != value
                for key, value in tags.items()
            ):
                continue
            if offset <= count < offset + limit:
                records.append(record)
            count += 1
        return {
            "records": [] if query.get("count") else records,
            "count": count,
            "searched": scope(state),
        }
    finally:
        db.close()


def lane_command(state, args):
    if args.action == "list":
        return {"lanes": list(state.lanes.values())}

    if args.action == "new":
        day = args.date or now()[:10]
        date.fromisoformat(day)
        lane = {
            "schema": CORE["lane"],
            "id": new_id("lane"),
            "title": args.title,
            "kind": args.kind,
            "parents": [state.lane_id(value) for value in args.parent],
            "created_at": now(),
            "tags": parse_tags(args.tags),
        }
        state.catalog.validate(CORE["lane"], lane)
        slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-") or "lane"
        directory = state.data / "lanes" / f"{day}-{slug[:60]}-{lane['id'][-8:]}"
        if directory.exists():
            fail("LANE_CONFLICT", "Lane directory already exists.")
        durable_mkdir(directory)
        write_json_atomic(directory / "lane.json", lane)
        for filename, text in {
            "README.md": f"# {args.title}\n\n",
            "PROVENANCE.md": "# Provenance\n\nCite Factum records here.\n",
            "FINDINGS.md": "# Findings\n\nGrade claims OBSERVED, UPSTREAM, or INFERENCE.\n",
        }.items():
            atomic_bytes(directory / filename, text.encode("utf-8"))
        State(state.repo).load().project()
        return {"lane": lane, "path": directory.relative_to(state.repo).as_posix()}

    lane_id = state.lane_id(args.lane)
    lane = state.lanes[lane_id]
    if args.action == "show":
        return {"lane": lane}

    if args.action == "edit":
        document = copy.deepcopy(lane["record"])
        if args.title is not None:
            document["title"] = args.title
        if args.tags is not None:
            document["tags"] = parse_tags(args.tags)
        state.catalog.validate(CORE["lane"], document)
        write_json_atomic(state.repo / lane["path"], document)
        State(state.repo).load().project()
        return {"lane": document}

    bundle = base_bundle(args)
    bundle["records"] = [{
        "kind": "edge",
        "body": {
            "subject": node_id,
            "predicate": "in_lane",
            "object": lane_id,
        },
        "tags": parse_tags(args.tags),
    } for node_id in args.ids]
    return add_bundle(state, bundle)


def parser():
    p = argparse.ArgumentParser(prog="factum")
    p.add_argument("--repo")
    p.add_argument("--at")
    sub = p.add_subparsers(dest="command", required=True)

    for name in ("init", "status", "doctor", "rebuild", "export"):
        sub.add_parser(name)

    verify = sub.add_parser("verify")
    verify.add_argument("--blobs", action="store_true")

    add = sub.add_parser("add")
    add.add_argument("--input", required=True)

    schema = sub.add_parser("schema")
    ss = schema.add_subparsers(dest="action", required=True)
    ss.add_parser("list")
    describe = ss.add_parser("describe")
    describe.add_argument("schema_id")
    assigned = ss.add_parser("assigned")
    assigned.add_argument("category", choices=["observable", "observation", "event", "predicate"])
    assigned.add_argument("name")
    validate = ss.add_parser("validate")
    validate.add_argument("--schema", required=True)
    validate.add_argument("--input", required=True)
    install = ss.add_parser("install")
    install.add_argument("directory")
    install.add_argument("--approve", action="store_true")

    template = sub.add_parser("template")
    template.add_argument("--type", default="web.capture")

    def submission(command):
        command.add_argument("--key", required=True)
        command.add_argument("--actor", required=True)
        command.add_argument("--tags")
        return command

    cap = submission(sub.add_parser("capture"))
    cap.add_argument("--url")
    cap.add_argument("--dataset")
    cap.add_argument("--revision")
    cap.add_argument("--file", action="append")
    cap.add_argument("--storage", choices=["git", "local"])
    cap.add_argument("--observed-at")
    cap.add_argument("--final-url")
    cap.add_argument("--status", type=int)
    cap.add_argument("--coverage", choices=[
        "complete", "partial", "metadata_only", "unknown",
    ], default="unknown")
    cap.add_argument("--lane")

    ext = submission(sub.add_parser("extract"))
    ext.add_argument("observation")
    ext.add_argument("--artifact")
    ext.add_argument("--types", default="url,domain,sha256")
    ext.add_argument("--max-bytes", type=int, default=20 * 1024 * 1024)
    ext.add_argument("--max-matches", type=int, default=10000)

    note = submission(sub.add_parser("note"))
    note.add_argument("--subject", required=True)
    note.add_argument("--property", required=True)
    note.add_argument("--value", required=True)
    note.add_argument("--basis", choices=["OBSERVED", "UPSTREAM", "INFERENCE"], required=True)
    note.add_argument("--cite", action="append", required=True)

    get = sub.add_parser("get")
    get.add_argument("id")
    get.add_argument("--context", type=int)

    matching = sub.add_parser("match")
    matching.add_argument("--input")
    values = matching.add_mutually_exclusive_group()
    for name in ("value", "url", "sha256", "text"):
        values.add_argument("--" + name)
    matching.add_argument("--type")
    matching.add_argument("--mode", choices=["exact", "key", "fuzzy"], default="exact")
    matching.add_argument("--limit", type=int, default=25)

    query = sub.add_parser("query")
    query.add_argument("--input", required=True)

    graph_p = sub.add_parser("graph")
    graph_p.add_argument("node")
    graph_p.add_argument("--depth", type=int, default=2)
    graph_p.add_argument("--limit", type=int, default=200)

    lane = sub.add_parser("lane")
    ls = lane.add_subparsers(dest="action", required=True)
    ls.add_parser("list")
    new = ls.add_parser("new")
    new.add_argument("title")
    new.add_argument("--kind", default="lane")
    new.add_argument("--date")
    new.add_argument("--parent", action="append", default=[])
    new.add_argument("--tags")
    show = ls.add_parser("show")
    show.add_argument("lane")
    edit = ls.add_parser("edit")
    edit.add_argument("lane")
    edit.add_argument("--title")
    edit.add_argument("--tags")
    link = submission(ls.add_parser("link"))
    link.add_argument("lane")
    link.add_argument("ids", nargs="+")
    return p


def dispatch(repo, args):
    if args.command == "init":
        if args.at:
            fail("READ_ONLY", "Cannot initialize a historical state.")
        state = initialize(repo)
        return {
            "initialized": True,
            "corpus_id": state.corpus["corpus_id"],
            "repo": str(repo),
        }

    if not args.at and not (repo / "data/corpus.json").exists():
        if args.command in {"status", "doctor"}:
            return {"initialized": False, "next": "init"}
        fail("NOT_INITIALIZED", "Run init.")

    state = State(repo, args.at).load()
    mutating = (
        args.command in {"add", "capture", "extract", "note", "export"}
        or args.command == "lane" and args.action in {"new", "edit", "link"}
        or args.command == "schema" and args.action == "install"
    )
    if args.at and mutating:
        fail("READ_ONLY", "--at is read-only.")

    if args.command in {"status", "doctor"}:
        stale = True
        try:
            db = state.connect()
            db.close()
            stale = False
        except (FactumError, sqlite3.Error):
            pass
        return {
            "initialized": True,
            "repo": str(repo),
            "version": TOOLKIT_VERSION,
            "format_version": FORMAT_VERSION,
            "records": len(state.records),
            "lanes": len(state.lanes),
            "pending": len(state.pending),
            "stale": stale,
            "database": str(state.db_path),
            "searched": scope(state),
        }

    if args.command == "rebuild":
        state.project()
        return {"database": str(state.db_path), "searched": scope(state)}

    if args.command == "verify":
        result = {
            "verified": True,
            "records": len(state.records),
            "pending": len(state.pending),
            "searched": scope(state),
        }
        if args.blobs:
            result["artifacts"] = state.verify_blobs()
        return result

    if args.command == "export":
        return export_pending(state)

    if args.command == "schema":
        if args.action == "list":
            return {
                "schemas": sorted(state.catalog.documents),
                "definitions": state.catalog.definitions,
                "packs": state.lock["packs"],
            }
        if args.action == "describe":
            if args.schema_id not in state.catalog.documents:
                fail("SCHEMA", "Unknown schema ID.")
            return {"schema": state.catalog.documents[args.schema_id]}
        if args.action == "assigned":
            return {"definition": state.catalog.definition(args.category, args.name)}
        if args.action == "validate":
            state.catalog.validate(args.schema, read_json(args.input))
            return {
                "valid": True,
                "scope": "JSON Schema validation; ingestion also checks graph semantics.",
            }
        result = install_pack(repo, args.directory, args.approve)
        if result.get("installed"):
            State(repo).load().project()
        return result

    if args.command == "template":
        definition = state.catalog.definition("observation", args.type)
        return {
            "note": "Fill data using the assigned schema; this is a scaffold, not a valid capture.",
            "data_schema": state.catalog.documents[definition["schema"]],
            "bundle": {
                "bundle": FORMAT_VERSION,
                "idempotency_key": "replace-with-stable-request-key",
                "actor": "agent:researcher",
                "tags": {},
                "records": [
                    {
                        "ref": "source",
                        "kind": "source",
                        "body": {
                            "source_type": "submitted",
                            "locator": "replace-with-source-locator",
                        },
                    },
                    {
                        "ref": "observation",
                        "kind": "observation",
                        "body": {
                            "type": args.type,
                            "source": "@source",
                            "files": [],
                            "data_schema": definition["schema"],
                            "data": {},
                        },
                        "tags": {},
                    },
                ],
            },
        }

    if args.command == "add":
        return add_bundle(state, read_json(args.input))
    if args.command == "capture":
        return capture(state, args)
    if args.command == "extract":
        return extract(state, args)
    if args.command == "match":
        return match(state, args)
    if args.command == "query":
        return query_records(state, args)
    if args.command == "graph":
        return graph(state, args)
    if args.command == "lane":
        return lane_command(state, args)

    if args.command == "note":
        bundle = base_bundle(args)
        bundle["records"] = [{
            "ref": "claim",
            "kind": "claim",
            "body": {
                "subject": args.subject,
                "property": args.property,
                "value": parse_json(args.value),
                "basis": args.basis,
                "cites": args.cite,
            },
            "tags": parse_tags(args.tags),
        }]
        return add_bundle(state, bundle)

    if args.command == "get":
        record = state.records.get(args.id)
        if record is None:
            fail("NOT_FOUND", args.id)
        result = {"record": record}
        if args.context is not None:
            if not 0 <= args.context <= 10000 or record["record_kind"] != "sighting":
                fail("CONTEXT", "Use a sighting ID and context between 0 and 10000.")
            locator = record["body"]["locator"]
            if "text_pos" not in locator:
                fail("LOCATOR", "No text-position selector.")
            text = state.artifact_bytes(locator["artifact"]).decode("utf-8", "strict")
            start, end = locator["text_pos"]["start"], locator["text_pos"]["end"]
            if end > len(text):
                fail("LOCATOR", "Text range exceeds artifact length.")
            exact = text[start:end]
            if "quote" in locator and locator["quote"]["exact"] != exact:
                fail("LOCATOR", "Quote differs from stored bytes.")
            result["exact"] = exact
            result["context"] = text[
                max(0, start - args.context):min(len(text), end + args.context)
            ]
        return result

    fail("COMMAND", "Unsupported command.")


def main():
    args = parser().parse_args()
    try:
        repo = resolve_repo(args.repo)
        lock = checked_path(repo, "data/.local/writer.lock")
        durable_mkdir(lock.parent)
        with FileLock(str(lock), timeout=30):
            emit(dispatch(repo, args))
    except FactumError as error:
        emit({"error": {"code": error.code, "message": str(error)}}, ok=False)
        raise SystemExit(1)
    except SchemaError as error:
        emit({"error": {"code": "SCHEMA", "message": str(error)}}, ok=False)
        raise SystemExit(1)
    except Timeout:
        emit({
            "error": {
                "code": "LOCK_TIMEOUT",
                "message": "Another Factum command is using this checkout.",
            }
        }, ok=False)
        raise SystemExit(1)
    except Exception as error:
        emit({
            "error": {
                "code": type(error).__name__,
                "message": str(error),
            }
        }, ok=False)
        raise SystemExit(1)