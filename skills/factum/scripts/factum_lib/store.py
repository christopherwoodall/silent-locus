from __future__ import annotations

import copy
import hashlib
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from . import FORMAT_VERSION, TOOLKIT_VERSION
from .resources import materialized_seed_packs
from .schemas import (
    CORE,
    KINDS,
    Catalog,
    canonical,
    checked_path,
    durable_mkdir,
    no_symlink_path,
    pack_inventory,
    parse_json,
    read_json,
    sha256,
    sync_directory,
    write_json_atomic,
)


class FactumError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def fail(code, message):
    raise FactumError(code, message)


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def new_id(kind):
    return f"{kind}_{uuid.uuid4().hex}"


def digest(value):
    return sha256(canonical(value).encode("utf-8"))


def atomic_bytes(path, raw):
    path = no_symlink_path(path)
    durable_mkdir(path.parent)

    fd, temporary = tempfile.mkstemp(
        prefix=".factum-",
        dir=path.parent,
    )

    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def append_lines(path, lines):
    path = no_symlink_path(path)
    old = path.read_bytes() if path.exists() else b""
    existing = set(old.splitlines())
    missing = [line.encode("utf-8") for line in lines if line.encode("utf-8") not in existing]

    if missing:
        separator = b"" if not old or old.endswith(b"\n") else b"\n"
        atomic_bytes(path, old + separator + b"\n".join(missing) + b"\n")


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if result.returncode:
        fail(
            "GIT",
            result.stderr.decode("utf-8", "replace").strip(),
        )

    return result.stdout


def head(repo):
    try:
        return git(
            repo,
            "rev-parse",
            "--verify",
            "HEAD",
        ).decode().strip()
    except FactumError:
        return None


def toolkit_checkout() -> Path | None:
    """
    Return the source/skill checkout when running from one.

    An installed distribution normally has neither SKILL.md nor
    scripts/factum.py at this location, so it returns None.
    """
    candidate = Path(__file__).resolve().parents[2]

    if (
        (candidate / "SKILL.md").is_file()
        and (candidate / "scripts/factum.py").is_file()
    ):
        return candidate

    return None


def resolve_repo(explicit=None):
    """
    Resolve the host Git repository.

    Precedence:
    1. Explicit --repo.
    2. FACTUM_REPO.
    3. Current Git repository.

    When invoked from a nested Factum source checkout without an explicit
    repository, discover the containing host repository.
    """
    toolkit = toolkit_checkout()
    value = explicit or os.environ.get("FACTUM_REPO")

    if value:
        root = Path(value).expanduser().resolve()
    else:
        root = Path(
            git(
                Path.cwd(),
                "rev-parse",
                "--show-toplevel",
            ).decode().strip()
        ).resolve()

        if toolkit is not None and root == toolkit:
            root = Path(
                git(
                    toolkit.parent,
                    "rev-parse",
                    "--show-toplevel",
                ).decode().strip()
            ).resolve()

    if toolkit is not None and root == toolkit:
        fail(
            "REPO",
            "Use the host repository, not the installed Factum clone.",
        )

    actual = Path(
        git(
            root,
            "rev-parse",
            "--show-toplevel",
        ).decode().strip()
    ).resolve()

    if root != actual:
        fail("REPO", f"Pass the repository root: {actual}")

    return root


def initialize(repo):
    """
    Initialize a new corpus or verify an existing compatible corpus.

    Seed packs are loaded as package resources. This does not depend on
    the toolkit being installed as a source clone.

    Existing corpus schemas are never reseeded by this function.
    """
    repo = Path(repo)
    check_layout(repo)
    data = repo / "data"
    corpus_path = data / "corpus.json"

    if corpus_path.exists():
        # Fail before changing ignore rules or local site state if the
        # existing corpus is incompatible or invalid.
        state = State(repo).load()
    else:
        managed_paths = (
            "schema-packs",
            "schema-lock.json",
            "records",
        )

        if any((data / path).exists() for path in managed_paths):
            fail(
                "PARTIAL_INIT",
                "Managed Factum paths exist without corpus.json. "
                "Inspect the partial initialization before retrying.",
            )

        packs = []

        with materialized_seed_packs() as assets:
            for source in sorted(assets.glob("*/*")):
                if not (source / "pack.json").is_file():
                    continue

                entry = pack_inventory(source)
                destination = data / entry["path"]
                durable_mkdir(destination.parent)

                shutil.copytree(source, destination)
                for relative in entry["files"]:
                    installed = checked_path(destination, relative)
                    with installed.open("rb") as stream:
                        os.fsync(stream.fileno())
                    sync_directory(installed.parent)
                sync_directory(destination)
                sync_directory(destination.parent)

                # Verify the actual installed copy, not only the source.
                if pack_inventory(destination) != entry:
                    fail(
                        "ASSETS",
                        "Seed pack copy verification failed: "
                        f"{entry['name']}@{entry['version']}",
                    )

                packs.append(entry)

        if not packs:
            fail(
                "ASSETS",
                "The installation contains no seed schema packs.",
            )

        packs.sort(key=lambda entry: (entry["name"], entry["version"]))

        lock = {
            "lock_format": 1,
            "packs": packs,
            "tags": {},
        }

        # Validate the copied seed catalog before activating the corpus.
        Catalog(
            lambda path: (repo / path).read_bytes(),
            lock,
        )

        write_json_atomic(data / "schema-lock.json", lock)

        write_json_atomic(
            corpus_path,
            {
                "corpus_id": uuid.uuid4().hex,
                "format_version": FORMAT_VERSION,
                "created_at": now(),
                "tags": {},
            },
        )

        state = State(repo).load()

    append_lines(
        repo / ".gitignore",
        ["/data/.local/"],
    )

    append_lines(
        repo / ".gitattributes",
        [
            "data/blobs/** -text -diff",
            "data/records/**/*.jsonl text eol=lf",
            "data/records/**/*.json text eol=lf",
            "data/schema-packs/** -text",
            "data/schema-lock.json text eol=lf",
        ],
    )

    site_path = data / ".local/site.json"

    if not site_path.exists():
        write_json_atomic(
            site_path,
            {
                "site_id": uuid.uuid4().hex,
                "tags": {},
            },
        )

    state.project()
    return state


DDL = """
PRAGMA foreign_keys=ON;

CREATE TABLE meta(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE nodes(
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL
);

CREATE TABLE records(
    id TEXT PRIMARY KEY REFERENCES nodes(id),
    kind TEXT NOT NULL,
    accepted_at TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    document TEXT NOT NULL CHECK(json_valid(document))
);
CREATE INDEX records_kind ON records(kind);

CREATE TABLE lanes(
    id TEXT PRIMARY KEY REFERENCES nodes(id),
    title TEXT NOT NULL,
    path TEXT NOT NULL,
    document TEXT NOT NULL CHECK(json_valid(document))
);

CREATE TABLE refs(
    from_id TEXT NOT NULL REFERENCES nodes(id),
    to_id TEXT NOT NULL REFERENCES nodes(id),
    PRIMARY KEY(from_id,to_id)
);
CREATE INDEX refs_target ON refs(to_id);

CREATE TABLE edges(
    id TEXT PRIMARY KEY REFERENCES records(id),
    subject_id TEXT NOT NULL REFERENCES nodes(id),
    predicate TEXT NOT NULL,
    object_id TEXT NOT NULL REFERENCES nodes(id)
);
CREATE INDEX edges_out ON edges(subject_id,predicate);
CREATE INDEX edges_in ON edges(object_id,predicate);

CREATE TABLE search_values(
    node_id TEXT NOT NULL REFERENCES nodes(id),
    value_type TEXT NOT NULL,
    raw_value TEXT NOT NULL,
    match_key TEXT NOT NULL
);
CREATE INDEX search_raw ON search_values(raw_value);
CREATE INDEX search_key ON search_values(value_type,match_key);

CREATE VIRTUAL TABLE search_fts USING fts5(
    node_id UNINDEXED,
    raw_value,
    tokenize='trigram'
);

CREATE TABLE receipts(
    request_key TEXT PRIMARY KEY,
    request_hash TEXT NOT NULL,
    result TEXT NOT NULL CHECK(json_valid(result))
);
"""


def make_record(kind, body, actor, tags=None, record_id=None):
    record = {
        "schema": CORE[kind],
        "record_kind": kind,
        "id": record_id or new_id(kind),
        "@timestamp": now(),
        "actor": actor,
        "tags": {} if tags is None else tags,
        "body": body,
    }
    record["fingerprint"] = digest(record)
    return record


def check_layout(repo):
    for relative in (
        "data", "data/corpus.json", "data/schema-lock.json", "data/schema-packs",
        "data/records", "data/lanes", "data/blobs", "data/.local",
        "data/.local/pending", "data/.local/blobs", "data/.local/tmp",
        "data/.local/snapshots", "data/.local/factum.db", "data/.local/site.json",
    ):
        checked_path(repo, relative)


class State:
    def __init__(self, repo, revision=None):
        self.repo = Path(repo)
        self.data = self.repo / "data"
        self.local = self.data / ".local"

        self.revision = None
        self.git_files = None

        if revision:
            self.revision = git(
                repo,
                "rev-parse",
                "--verify",
                f"{revision}^{{commit}}",
            ).decode().strip()

            self.git_files = {
                value.decode("utf-8")
                for value in git(
                    repo,
                    "ls-tree",
                    "-r",
                    "-z",
                    "--name-only",
                    self.revision,
                    "--",
                    "data",
                ).split(b"\0")
                if value
            }

        self.records = {}
        self.lanes = {}
        self.receipts = {}
        self.pending = []

        self.catalog = None
        self.corpus = None
        self.lock = None
        self.state_digest = None

    @property
    def db_path(self):
        if self.revision:
            return self.local / "snapshots" / f"{self.revision}.db"
        return self.local / "factum.db"

    def read(self, path):
        if self.revision:
            return git(
                self.repo,
                "show",
                f"{self.revision}:{path}",
            )

        file = checked_path(self.repo, path)
        resolved = file.resolve()

        if self.data.resolve() not in resolved.parents:
            fail(
                "PATH",
                f"Managed path escapes data/: {path}",
            )

        if file.is_symlink():
            fail("SYMLINK", path)

        return file.read_bytes()

    def json(self, path):
        return parse_json(self.read(path))

    def paths(self, prefix, suffix):
        prefix = "data/" + prefix

        if self.git_files is not None:
            return sorted(
                path
                for path in self.git_files
                if path.startswith(prefix + "/")
                and path.endswith(suffix)
            )

        root = checked_path(self.repo, prefix)

        if not root.exists():
            return []

        result = []

        for path in root.rglob("*"):
            if path.is_symlink():
                fail("SYMLINK", str(path))

            if path.is_file() and path.name.endswith(suffix):
                result.append(path.relative_to(self.repo).as_posix())

        return sorted(result)

    def kind(self, node_id):
        if node_id in self.lanes:
            return "lane"

        record = self.records.get(node_id)
        return record["record_kind"] if record else None

    def lane_id(self, value):
        if value in self.lanes:
            return value

        matches = [
            lane_id
            for lane_id, lane in self.lanes.items()
            if lane["record"]["title"] == value
            or Path(lane["path"]).parent.name == value
        ]

        if len(matches) != 1:
            fail(
                "LANE",
                "Lane not found or ambiguous. Use its ID.",
            )

        return matches[0]

    def insert_record(self, record):
        self.catalog.validate(CORE["record"], record)

        kind = record["record_kind"]

        if (
            record["schema"] != CORE[kind]
            or not record["id"].startswith(kind + "_")
        ):
            fail(
                "IDENTITY",
                "Record kind, schema, and ID disagree.",
            )

        unsigned = {
            key: value
            for key, value in record.items()
            if key != "fingerprint"
        }

        if digest(unsigned) != record["fingerprint"]:
            fail(
                "HASH",
                f"Record fingerprint mismatch: {record['id']}",
            )

        self.catalog.validate_body(kind, record["body"])

        previous = self.records.get(record["id"])

        if previous is not None and previous != record:
            fail("IMMUTABLE_CONFLICT", record["id"])

        self.records[record["id"]] = record

    def insert_receipt(self, receipt):
        if (
            not isinstance(receipt, dict)
            or set(receipt) != {"key", "request_hash", "result"}
            or not isinstance(receipt["key"], str)
            or not isinstance(receipt["request_hash"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", receipt["request_hash"])
            or not isinstance(receipt["result"], dict)
        ):
            fail("RECEIPT", "Invalid receipt.")

        result = receipt["result"]
        if (
            not receipt["key"]
            or not isinstance(result.get("ids"), dict)
            or not all(isinstance(key, str) and isinstance(value, str) for key, value in result["ids"].items())
            or not isinstance(result.get("record_ids"), list)
            or not all(isinstance(value, str) for value in result["record_ids"])
        ):
            fail("RECEIPT", "Invalid receipt result IDs.")

        old = self.receipts.get(receipt["key"])

        if old is not None and old != receipt:
            fail("IDEMPOTENCY_CONFLICT", receipt["key"])

        self.receipts[receipt["key"]] = receipt

    def load(self):
        check_layout(self.repo)
        self.corpus = self.json("data/corpus.json")

        if self.corpus.get("format_version") != FORMAT_VERSION:
            fail(
                "FORMAT",
                "Unsupported corpus format; explicit migration required.",
            )

        self.lock = self.json("data/schema-lock.json")
        self.catalog = Catalog(self.read, self.lock)

        for path in self.paths("lanes", "lane.json"):
            lane = self.json(path)
            self.catalog.validate(CORE["lane"], lane)

            if lane["id"] in self.lanes:
                fail("LANE_CONFLICT", lane["id"])

            self.lanes[lane["id"]] = {
                "record": lane,
                "path": path,
            }

        consumed = set()

        for path in self.paths("records", "manifest.json"):
            manifest = self.json(path)

            expected = {
                "format_version",
                "batch_id",
                "corpus_id",
                "records_sha256",
                "record_count",
                "receipt",
                "tags",
            }

            if (
                not isinstance(manifest, dict)
                or set(manifest) != expected
            ):
                fail("MANIFEST", path)

            if manifest["format_version"] != FORMAT_VERSION:
                fail("FORMAT", path)

            if manifest["corpus_id"] != self.corpus["corpus_id"]:
                fail("CORPUS", path)

            if Path(path).parent.name != manifest["batch_id"]:
                fail(
                    "MANIFEST",
                    "Batch ID and directory disagree.",
                )

            record_path = (
                str(Path(path).parent / "records.jsonl")
                .replace("\\", "/")
            )

            raw = self.read(record_path)

            if sha256(raw) != manifest["records_sha256"]:
                fail("HASH", record_path)

            lines = raw.splitlines()

            if len(lines) != manifest["record_count"]:
                fail("COUNT", record_path)

            for line in lines:
                self.insert_record(parse_json(line))

            self.insert_receipt(manifest["receipt"])
            consumed.add(record_path)

        if consumed != set(self.paths("records", ".jsonl")):
            fail(
                "ORPHAN_JSONL",
                "A records JSONL file has no manifest.",
            )

        if not self.revision:
            for path in self.paths(".local/pending", ".json"):
                document = self.json(path)

                if (
                    not isinstance(document, dict)
                    or set(document) != {
                        "batch_id",
                        "records",
                        "receipt",
                        "tags",
                    }
                ):
                    fail("PENDING", path)

                if Path(path).stem != document["batch_id"]:
                    fail(
                        "PENDING",
                        "Pending filename and ID disagree.",
                    )

                for record in document["records"]:
                    self.insert_record(record)

                self.insert_receipt(document["receipt"])
                self.pending.append((path, document))

        self.validate_references()

        self.state_digest = digest(
            {
                "corpus": self.corpus,
                "lock": self.lock,
                "records": sorted(
                    (key, value["fingerprint"])
                    for key, value in self.records.items()
                ),
                "lanes": sorted(
                    (key, value["record"])
                    for key, value in self.lanes.items()
                ),
                "receipts": sorted(self.receipts.items()),
            }
        )

        return self

    def references_for(self, record):
        result = []

        def collect(value, kinds):
            result.append((value, kinds))
            return value

        self.catalog.body_references(
            record["record_kind"],
            copy.deepcopy(record["body"]),
            collect,
        )

        return result

    def validate_references(self):
        def check(value, kinds):
            actual = self.kind(value)

            if actual is None:
                fail("DANGLING_REFERENCE", value)

            if "*" not in kinds and actual not in kinds:
                fail(
                    "REFERENCE_TYPE",
                    f"{value}: expected {kinds}, got {actual}",
                )

            return value

        for lane in self.lanes.values():
            self.catalog.walk_references(
                CORE["lane"],
                copy.deepcopy(lane["record"]),
                check,
            )

        for record in self.records.values():
            kind = record["record_kind"]
            body = record["body"]

            self.catalog.body_references(
                kind,
                copy.deepcopy(body),
                check,
            )

            if kind == "edge":
                definition = self.catalog.definition(
                    "predicate",
                    body["predicate"],
                )

                for endpoint in ("subject", "object"):
                    if endpoint in definition:
                        check(
                            body[endpoint],
                            definition[endpoint],
                        )

            if kind == "sighting":
                observation = self.records[
                    body["observation"]
                ]["body"]

                artifact = body["locator"]["artifact"]

                attached = {
                    item["artifact"]
                    for item in observation["files"]
                }

                if artifact not in attached:
                    fail(
                        "LOCATOR",
                        "Sighting artifact is not attached to the observation.",
                    )

                for name in ("text_pos", "bytes"):
                    if name in body["locator"]:
                        interval = body["locator"][name]

                        if interval["end"] < interval["start"]:
                            fail(
                                "LOCATOR",
                                "Range end precedes start.",
                            )

            if kind == "event":
                occurred = body["occurred"]

                if (
                    occurred["basis"] != "unknown"
                    and not any(
                        key in occurred
                        for key in ("start", "on_date", "raw")
                    )
                ):
                    fail(
                        "TIME",
                        "Known event time needs start, on_date, or raw.",
                    )

                if "start" in occurred and "end" in occurred:
                    start = datetime.fromisoformat(
                        occurred["start"].replace("Z", "+00:00")
                    )
                    end = datetime.fromisoformat(
                        occurred["end"].replace("Z", "+00:00")
                    )

                    if end < start:
                        fail("TIME", "Event end precedes start.")

        for receipt in self.receipts.values():
            result = receipt["result"]
            for node_id in [*result["ids"].values(), *result["record_ids"]]:
                check(node_id, ["*"])

    def search_entries(self, record):
        kind = record["record_kind"]
        body = record["body"]

        if kind == "observable":
            return [(body["type"], body["value"])]

        if kind == "source":
            value_type = (
                "url"
                if body["source_type"] == "web"
                else "source"
            )
            return [(value_type, body["locator"])]

        if kind == "artifact" and "sha256" in body:
            return [("sha256", body["sha256"])]

        if kind == "observation":
            return [
                ("url", body["data"][key])
                for key in ("requested_url", "final_url")
                if isinstance(body["data"].get(key), str)
            ]

        if kind == "event":
            return [("text", body["title"])]

        return []

    def project(self):
        no_symlink_path(self.db_path)
        durable_mkdir(self.db_path.parent)

        temporary = self.db_path.with_name(
            self.db_path.name + "." + uuid.uuid4().hex
        )

        db = None

        try:
            db = sqlite3.connect(temporary)
            db.executescript(DDL)

            with db:
                metadata = {
                    "toolkit_version": TOOLKIT_VERSION,
                    "state_digest": self.state_digest,
                    "corpus_id": self.corpus["corpus_id"],
                }

                for key, value in metadata.items():
                    db.execute(
                        "INSERT INTO meta VALUES (?,?)",
                        (key, value),
                    )

                for lane_id, lane in self.lanes.items():
                    db.execute(
                        "INSERT INTO nodes VALUES (?,?)",
                        (lane_id, "lane"),
                    )
                    db.execute(
                        "INSERT INTO lanes VALUES (?,?,?,?)",
                        (
                            lane_id,
                            lane["record"]["title"],
                            lane["path"],
                            canonical(lane["record"]),
                        ),
                    )

                for record in self.records.values():
                    db.execute(
                        "INSERT INTO nodes VALUES (?,?)",
                        (
                            record["id"],
                            record["record_kind"],
                        ),
                    )
                    db.execute(
                        "INSERT INTO records VALUES (?,?,?,?,?)",
                        (
                            record["id"],
                            record["record_kind"],
                            record["@timestamp"],
                            record["fingerprint"],
                            canonical(record),
                        ),
                    )

                for record in self.records.values():
                    record_id = record["id"]

                    for target, _ in self.references_for(record):
                        db.execute(
                            "INSERT OR IGNORE INTO refs VALUES (?,?)",
                            (record_id, target),
                        )

                    if record["record_kind"] == "edge":
                        body = record["body"]
                        db.execute(
                            "INSERT INTO edges VALUES (?,?,?,?)",
                            (
                                record_id,
                                body["subject"],
                                body["predicate"],
                                body["object"],
                            ),
                        )

                    for value_type, raw in self.search_entries(record):
                        db.execute(
                            "INSERT INTO search_values VALUES (?,?,?,?)",
                            (
                                record_id,
                                value_type,
                                raw,
                                self.catalog.match_key(value_type, raw),
                            ),
                        )
                        db.execute(
                            "INSERT INTO search_fts VALUES (?,?)",
                            (record_id, raw),
                        )

                for receipt in self.receipts.values():
                    db.execute(
                        "INSERT INTO receipts VALUES (?,?,?)",
                        (
                            receipt["key"],
                            receipt["request_hash"],
                            canonical(receipt["result"]),
                        ),
                    )

                # These identifiers are fixed application constants,
                # not user-provided table or view names.
                for kind in KINDS:
                    db.execute(
                        f"CREATE VIEW {kind}_records AS "
                        f"SELECT * FROM records WHERE kind='{kind}'"
                    )

            if db.execute("PRAGMA foreign_key_check").fetchall():
                fail(
                    "SQLITE",
                    "Foreign-key verification failed.",
                )

            integrity = db.execute(
                "PRAGMA integrity_check"
            ).fetchone()

            if integrity is None or integrity[0] != "ok":
                fail(
                    "SQLITE",
                    "Integrity verification failed.",
                )

            db.close()
            db = None

            with temporary.open("rb") as stream:
                os.fsync(stream.fileno())

            os.replace(temporary, self.db_path)
            sync_directory(self.db_path.parent)

        finally:
            if db is not None:
                db.close()

            if temporary.exists():
                temporary.unlink()

    def connect(self):
        no_symlink_path(self.db_path)
        if not self.db_path.exists():
            fail("INDEX_MISSING", "Run rebuild.")

        db = sqlite3.connect(
            self.db_path.resolve().as_uri() + "?mode=ro",
            uri=True,
        )
        db.row_factory = sqlite3.Row

        try:
            row = db.execute(
                "SELECT value FROM meta WHERE key='state_digest'"
            ).fetchone()

            if row is None or row[0] != self.state_digest:
                fail("INDEX_STALE", "Run rebuild.")

        except Exception:
            db.close()
            raise

        return db

    def artifact_bytes(self, artifact_id):
        record = self.records.get(artifact_id)

        if (
            record is None
            or record["record_kind"] != "artifact"
        ):
            fail("ARTIFACT", artifact_id)

        body = record["body"]

        if "sha256" not in body:
            fail("REFERENCE_ONLY", artifact_id)

        value = body["sha256"]
        relative = f"blobs/sha256/{value[:2]}/{value}"
        git_path = "data/" + relative

        if self.revision and git_path in self.git_files:
            raw = git(
                self.repo,
                "show",
                f"{self.revision}:{git_path}",
            )
        else:
            roots = (
                [self.local]
                if self.revision
                else [self.data, self.local]
            )

            path = next(
                (
                    checked_path(root, relative)
                    for root in roots
                    if checked_path(root, relative).is_file()
                ),
                None,
            )

            if path is None:
                fail("ARTIFACT_MISSING", artifact_id)

            if path.is_symlink():
                fail("SYMLINK", str(path))

            raw = path.read_bytes()

        if (
            sha256(raw) != value
            or len(raw) != body["size"]
        ):
            fail("HASH", artifact_id)

        return raw

    def verify_blobs(self):
        missing = []
        verified = {}

        for record in self.records.values():
            if (
                record["record_kind"] != "artifact"
                or "sha256" not in record["body"]
            ):
                continue

            value = record["body"]["sha256"]

            if value in verified:
                if record["body"]["size"] != verified[value]:
                    fail("HASH", record["id"])
                continue

            try:
                self.artifact_bytes(record["id"])
                verified[value] = record["body"]["size"]
            except FactumError as error:
                if error.code != "ARTIFACT_MISSING":
                    raise
                missing.append(record["id"])

        return {
            "verified_hashes": len(verified),
            "missing": missing,
        }


def store_file(state, filename, storage):
    check_layout(state.repo)
    if storage not in {"git", "local"}:
        fail("STORAGE", "Storage must be git or local.")

    source = Path(filename).expanduser().resolve()

    if not source.is_file():
        fail("FILE", str(source))

    directory = state.local / "tmp"
    durable_mkdir(directory)

    fd, temporary = tempfile.mkstemp(
        prefix="artifact-",
        dir=directory,
    )

    checksum = hashlib.sha256()
    size = 0

    try:
        with source.open("rb") as incoming, os.fdopen(fd, "wb") as outgoing:
            while chunk := incoming.read(1024 * 1024):
                checksum.update(chunk)
                outgoing.write(chunk)
                size += len(chunk)

            outgoing.flush()
            os.fsync(outgoing.fileno())

        value = checksum.hexdigest()
        root = state.data if storage == "git" else state.local

        destination = (
            root / "blobs/sha256" / value[:2] / value
        )
        durable_mkdir(destination.parent)

        if destination.exists():
            if destination.is_symlink():
                fail("SYMLINK", str(destination))

            current = hashlib.sha256()

            with destination.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    current.update(chunk)

            if (
                current.hexdigest() != value
                or destination.stat().st_size != size
            ):
                fail("HASH", str(destination))
        else:
            os.replace(temporary, destination)
            sync_directory(destination.parent)

        return {
            "sha256": value,
            "size": size,
        }

    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def add_bundle(state, submitted):
    check_layout(state.repo)
    state.catalog.validate(CORE["bundle"], submitted)
    bundle = copy.deepcopy(submitted)
    file_bodies = {}

    for item in bundle.get("files", []):
        if item["ref"] in file_bodies:
            fail("DUPLICATE_REF", item["ref"])

        file_bodies[item["ref"]] = store_file(
            state,
            item["path"],
            item["storage"],
        )

    request_hash = digest(
        {
            "bundle": bundle,
            "file_contents": file_bodies,
        }
    )

    key = bundle["idempotency_key"]
    prior = state.receipts.get(key)

    if prior:
        if prior["request_hash"] != request_hash:
            fail("IDEMPOTENCY_CONFLICT", key)

        return {
            **prior["result"],
            "replayed": True,
        }

    ids = {
        name: new_id("artifact")
        for name in file_bodies
    }

    for entry in bundle["records"]:
        if "ref" in entry:
            if entry["ref"] in ids:
                fail("DUPLICATE_REF", entry["ref"])

            ids[entry["ref"]] = new_id(entry["kind"])

    def resolve(value, kinds):
        if isinstance(value, str) and value.startswith("@"):
            name = value[1:]

            if name not in ids:
                fail("UNKNOWN_REF", value)

            return ids[name]

        return value

    actor = bundle["actor"]

    records = [
        make_record(
            "artifact",
            file_bodies[item["ref"]],
            actor,
            item.get("tags", {}),
            ids[item["ref"]],
        )
        for item in bundle.get("files", [])
    ]

    seen = {}

    for entry in bundle["records"]:
        kind = entry["kind"]
        body = copy.deepcopy(entry["body"])

        if kind == "observation":
            if "observed_at" not in body:
                if (
                    body.get("time_basis", "received_by_factum")
                    != "received_by_factum"
                ):
                    fail(
                        "TIME",
                        "A supplied time_basis requires observed_at.",
                    )

                body["observed_at"] = now()
                body["time_basis"] = "received_by_factum"

            body.setdefault("files", [])

        elif kind == "sighting":
            body.setdefault("method", "agent")

        elif kind == "event":
            body.setdefault(
                "occurred",
                {"basis": "unknown"},
            )
            body.setdefault("data", {})

        state.catalog.assign(kind, body)
        state.catalog.body_references(kind, body, resolve)

        if kind == "observable" and "ref" in entry:
            matches = [
                old["id"]
                for old in state.records.values()
                if old["record_kind"] == "observable"
                and old["body"]["type"] == body["type"]
                and old["body"]["value"] == body["value"]
            ]
            seen[entry["ref"]] = matches or "not_found"

        records.append(
            make_record(
                kind,
                body,
                actor,
                entry.get("tags", {}),
                ids.get(entry.get("ref")),
            )
        )

    if bundle.get("lane"):
        lane_id = state.lane_id(bundle["lane"])

        for record in list(records):
            records.append(
                make_record(
                    "edge",
                    {
                        "subject": record["id"],
                        "predicate": "in_lane",
                        "object": lane_id,
                    },
                    actor,
                )
            )

    for record in records:
        state.insert_record(record)

    state.validate_references()

    batch_id = uuid.uuid4().hex

    result = {
        "durability": "pending",
        "batch_id": batch_id,
        "ids": ids,
        "record_ids": [
            record["id"]
            for record in records
        ],
        "seen_before": seen,
        "seen_before_scope": (
            "Exact previously accepted observable values of the same type."
        ),
    }

    pending = {
        "batch_id": batch_id,
        "records": records,
        "receipt": {
            "key": key,
            "request_hash": request_hash,
            "result": result,
        },
        "tags": bundle.get("tags", {}),
    }

    write_json_atomic(
        state.local / "pending" / f"{batch_id}.json",
        pending,
    )

    # Pending data is already durable. If projection fails, rebuild
    # can recover the accepted submission from this file.
    refreshed = State(state.repo).load()
    refreshed.project()

    return result


def export_pending(state):
    check_layout(state.repo)
    exported = []

    for pending_path, pending in state.pending:
        batch_id = pending["batch_id"]
        destination = state.data / "records" / batch_id

        raw = "".join(
            canonical(record) + "\n"
            for record in pending["records"]
        ).encode("utf-8")

        manifest = {
            "format_version": FORMAT_VERSION,
            "batch_id": batch_id,
            "corpus_id": state.corpus["corpus_id"],
            "records_sha256": sha256(raw),
            "record_count": len(pending["records"]),
            "receipt": pending["receipt"],
            "tags": pending["tags"],
        }

        if destination.exists():
            if (
                (destination / "records.jsonl").read_bytes() != raw
                or read_json(destination / "manifest.json") != manifest
            ):
                fail("BATCH_CONFLICT", batch_id)
        else:
            staging_root = state.local / "tmp"
            durable_mkdir(staging_root)

            staging = Path(
                tempfile.mkdtemp(
                    prefix="batch-",
                    dir=staging_root,
                )
            )

            try:
                atomic_bytes(
                    staging / "records.jsonl",
                    raw,
                )
                write_json_atomic(
                    staging / "manifest.json",
                    manifest,
                )

                durable_mkdir(destination.parent)

                os.replace(staging, destination)
                sync_directory(destination.parent)

            finally:
                if staging.exists():
                    shutil.rmtree(staging)

        pending_file = state.repo / pending_path
        pending_file.unlink()
        sync_directory(pending_file.parent)

        exported.append(
            destination.relative_to(state.repo).as_posix()
        )

    refreshed = State(state.repo).load()
    refreshed.project()

    return {
        "exported": exported,
        "pending": 0,
        "state_digest": refreshed.state_digest,
    }