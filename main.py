#!/usr/bin/env python3
"""Write one short family scene to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The scene is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 280 characters, not only white space.
"""

import os
import sys
from pathlib import Path

SCENE = (
    "Dad still burns the toast on Sundays so Mum can tell him, again, "
    "that he has been doing it wrong for thirty years.\n"
    "He winks at me while she scrapes it, and I have never told her "
    "he does it for the laugh."
)

MIN_CHARS = 1
MAX_CHARS = 280
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 280 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"scene is {chars} characters, outside 1-280")
    if not text.strip():
        raise ValueError("scene is only white space")
    lines = text.split("\n")
    if not (1 <= len(lines) <= 2):
        raise ValueError(f"scene is {len(lines)} lines, must be 1 or 2")
    return chars


def write_entry(path: Path) -> int:
    """Validate the scene and write it to path. Returns the char count."""
    chars = validate(SCENE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SCENE, encoding="utf-8")
    return chars


def main() -> int:
    path = resolve_output_path()
    try:
        chars = write_entry(path)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
