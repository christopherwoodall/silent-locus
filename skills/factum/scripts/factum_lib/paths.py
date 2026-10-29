"""Resolve plugin assets and the host repository without changing the FS."""

from pathlib import Path

from .store import fail, resolve_repo


def skill_root():
    """Source layout: <skill>/scripts/factum_lib/paths.py."""
    return Path(__file__).resolve().parents[2]


def assets_root():
    """Support both a cloned skill and a built Python package."""
    cloned = Path(__file__).resolve().parent / "assets"
    if cloned.is_dir():
        return cloned

    packaged = Path(__file__).resolve().parent / "assets"
    if packaged.is_dir():
        return packaged

    fail(
        "ASSETS_MISSING",
        "Factum assets are missing. Install the complete skill directory.",
    )


def is_repository(path):
    """Support ordinary repositories and Git worktrees."""
    marker = Path(path) / ".git"
    return marker.is_dir() or marker.is_file()


def enclosing_repository(start, excluded=None):
    excluded = {
        Path(path).resolve() for path in (excluded or [])
    }
    current = Path(start).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if candidate not in excluded and is_repository(candidate):
            return candidate

    return None


def resolve_repository(explicit=None):
    """Use the same host resolution and toolkit refusal as the public CLI."""
    return resolve_repo(explicit)