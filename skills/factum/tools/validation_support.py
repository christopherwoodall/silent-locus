"""Snapshot and subprocess helpers shared by integration tests and smoke tests."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def run(argv, cwd=None, env=None, check=True):
    result = subprocess.run(
        [str(item) for item in argv], cwd=cwd, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    if check and result.returncode:
        raise AssertionError(
            f"Command failed ({result.returncode}): {argv}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return result


def git(repo, *args, check=True):
    return run(["git", "-C", repo, *args], check=check)


def source_files(root=ROOT):
    """Explicit source inventory, including nonignored new deployment files."""
    root = Path(root)
    if (root / ".git").exists():
        names = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").stdout.split("\0")
    else:
        names = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    top = {
        "README.md", "INSTALL.md", "SKILL.md", "AGENTS.md", "ARCHITECTURE.md",
        "pyproject.toml", ".gitignore", ".gitattributes",
    }
    prefixes = ("scripts/", "docs/", "references/", "examples/", "tests/", "tools/", ".github/")
    suffixes = {".py", ".json", ".md", ".txt", ".yml", ".yaml", ".toml"}
    selected = []
    for name in sorted(set(names)):
        if not name:
            continue
        path = root / name
        parts = Path(name).parts
        if any(p.startswith(".") or p in {"__pycache__", "data", "dist", "build"} or p.endswith(".egg-info") for p in parts[1:-1]):
            continue
        if name not in top and not (name.startswith(prefixes) and path.suffix in suffixes):
            continue
        if path.is_symlink() or not path.is_file():
            raise AssertionError(f"Unsafe or missing source file: {name}")
        selected.append(name)
    return selected


def hashes(root, names):
    return {name: hashlib.sha256((Path(root) / name).read_bytes()).hexdigest() for name in names}


def snapshot(workspace, root=ROOT):
    workspace, root = Path(workspace), Path(root)
    destination = workspace / "factum-under-test"
    destination.mkdir()
    names = source_files(root)
    identity = hashes(root, names)
    for name in names:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    assert hashes(destination, names) == identity
    git(destination, "init", "-q")
    # Preserve snapshot bytes, even when source files currently have CRLF.
    (destination / ".git/info/attributes").write_text("* -text\n", encoding="utf-8")
    git(destination, "add", "--all")
    git(destination, "commit", "-qm", "Synthetic validation snapshot")
    return destination, identity


def install_skill(host, source, identity):
    skill = Path(host) / ".agents/skills/factum"
    skill.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "-c", "core.autocrlf=false", "clone", "-q", source, skill])
    assert hashes(skill, identity) == identity
    exclude = git(host, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    exclude = Path(exclude)
    if not exclude.is_absolute():
        exclude = Path(host) / exclude
    with exclude.open("a", encoding="utf-8") as stream:
        stream.write("\n/.agents/skills/factum/\n")
    return skill


def cli(skill, host, *args, cwd=None, env=None, ok=True, explicit=True):
    environment = os.environ.copy()
    environment.pop("FACTUM_REPO", None)
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        environment.update(env)
    command = ["uv", "run", "--no-project", "--python", os.environ.get("FACTUM_TEST_PYTHON", "3.12"), Path(skill) / "scripts/factum.py"]
    if explicit:
        command += ["--repo", host]
    result = run(command + list(args), cwd=cwd or host, env=environment, check=False)
    try:
        document = json.loads(result.stdout)
    except ValueError as error:
        raise AssertionError(f"Non-JSON CLI output: {result.stdout}\n{result.stderr}") from error
    assert document["ok"] is ok, document
    assert (result.returncode == 0) is ok, result.stderr
    return document
