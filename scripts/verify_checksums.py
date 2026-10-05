#!/usr/bin/env python3
"""Read-only SHA256SUMS audit; CRLF-only drift is reported separately.

Run from anywhere: python3 -B scripts/verify_checksums.py [data/collection ...]
No manifests or evidence are repaired by this command.
"""

import argparse
import hashlib
import re
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
LINE = re.compile(r"^([0-9a-fA-F]{64})  ([*]?)(.+)$")
CHUNK = 1024 * 1024


def digest(path: Path, normalize_crlf: bool = False) -> str:
    result = hashlib.sha256()
    carry = b""
    with path.open("rb") as stream:
        while block := stream.read(CHUNK):
            if normalize_crlf:
                block = carry + block
                carry = block[-1:] if block.endswith(b"\r") else b""
                if carry:
                    block = block[:-1]
                block = block.replace(b"\r\n", b"\n")
            result.update(block)
    result.update(carry)
    return result.hexdigest()


def manifests(target: Path):
    if target.is_file():
        if target.name not in {"SHA256SUMS", "SHA256SUMS.txt"}:
            raise ValueError(f"not a checksum manifest: {target}")
        return [target]
    return sorted(
        path for path in target.rglob("*")
        if path.is_file() and path.name in {"SHA256SUMS", "SHA256SUMS.txt"}
    )


def audit(targets: list[Path]) -> int:
    counts = {"ok": 0, "crlf": 0, "missing": 0, "mismatch": 0, "invalid": 0}
    for target in targets:
        for manifest in manifests(target):
            try:
                lines = manifest.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as error:
                print(f"INVALID {manifest}: {error}")
                counts["invalid"] += 1
                continue
            for number, line in enumerate(lines, 1):
                if not line or line.startswith("#"):
                    continue
                match = LINE.fullmatch(line)
                if not match:
                    print(f"INVALID {manifest}:{number}: malformed checksum entry")
                    counts["invalid"] += 1
                    continue
                expected, _, filename = match.groups()
                # Root-relative historical manifests use data/; most manifests
                # refer to paths relative to the manifest's own directory.
                base = REPO if filename.startswith("data/") else manifest.parent
                path = (base / filename).resolve()
                if not path.is_relative_to(REPO) or Path(filename).is_absolute():
                    print(f"INVALID {manifest}:{number}: path outside repository: {filename}")
                    counts["invalid"] += 1
                    continue
                label = f"{manifest.relative_to(REPO)}:{number} {filename}"
                if not path.is_file():
                    print(f"MISSING {label}")
                    counts["missing"] += 1
                    continue
                try:
                    actual = digest(path)
                    if actual == expected.lower():
                        counts["ok"] += 1
                        continue
                    # A checkout with CRLF bytes can disagree with a manifest
                    # calculated from LF bytes; never modify either file.
                    normalized = digest(path, normalize_crlf=True)
                except OSError as error:
                    print(f"INVALID {label}: {error}")
                    counts["invalid"] += 1
                    continue
                if normalized == expected.lower() and normalized != actual:
                    print(f"CRLF_ONLY {label} (raw={actual}, LF={normalized})")
                    counts["crlf"] += 1
                else:
                    print(f"MISMATCH {label} (expected={expected}, actual={actual}, LF={normalized})")
                    counts["mismatch"] += 1
    print("Checksum summary: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    return int(any(counts[key] for key in ("missing", "mismatch", "invalid")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets", nargs="*", type=Path, default=[REPO / "data"],
        help="manifest, collection, or directory (default: repository data/)",
    )
    args = parser.parse_args()
    targets = [(REPO / target).resolve() for target in args.targets]
    for target in targets:
        if not target.is_relative_to(REPO) or not target.exists():
            parser.error(f"target must exist inside repository: {target}")
    try:
        return audit(targets)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
