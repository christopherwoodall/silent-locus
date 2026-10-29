from __future__ import annotations

from contextlib import contextmanager
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

from .schemas import SchemaError


def _copy_resource_tree(source: Traversable, destination: Path) -> None:
    """Materialize bundled resources without assuming a filesystem package."""
    if not source.is_dir():
        raise SchemaError("Bundled schema-pack resource is not a directory.")

    destination.mkdir(parents=True, exist_ok=True)

    for child in sorted(source.iterdir(), key=lambda item: item.name):
        name = child.name
        if name in {"", ".", ".."} or "/" in name or "\\" in name:
            raise SchemaError(f"Invalid bundled resource name: {name!r}")

        target = destination / name

        if child.is_dir():
            _copy_resource_tree(child, target)
        elif child.is_file():
            target.write_bytes(child.read_bytes())
        else:
            raise SchemaError(f"Unsupported bundled resource: {name}")


@contextmanager
def materialized_seed_packs() -> Iterator[Path]:
    """
    Yield a temporary filesystem copy of the packaged seed packs.

    This works for both:
    - the clone-based uv script;
    - an installed Python distribution.
    """
    root = files("factum_lib").joinpath("assets").joinpath("packs")

    if not root.is_dir():
        raise SchemaError(
            "Bundled schema packs are missing. "
            "The Factum installation or distribution is incomplete."
        )

    with TemporaryDirectory(prefix="factum-seed-packs-") as temporary:
        destination = Path(temporary) / "packs"
        _copy_resource_tree(root, destination)
        yield destination