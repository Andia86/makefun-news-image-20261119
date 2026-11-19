#!/usr/bin/env python3
"""Ship the bundled news poster to the contest's output slot.

The artwork for this entry is drawn ahead of time and stored in the
repository as ``entry.png`` next to this script.  All this program has
to do at run time is carry those bytes, untouched, to the place the
scorer looks for them:

* ``$MAKEFUN_OUTPUT_DIR/entry.png`` when the harness sets that
  variable, or
* ``/output/entry.png`` otherwise.

The copy is verified on the way in and on the way out: the bundled
file must start with the PNG signature, and the file that lands on
disk must match the bundled bytes exactly and still carry that
signature.  Anything else raises, so a corrupt artefact fails loudly
instead of being graded as a broken image.
"""

import os
import sys
from pathlib import Path

# Every PNG file opens with these eight bytes: 89 50 4E 47 0D 0A 1A 0A.
PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))

ARTWORK_FILENAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def read_bundled_artwork() -> bytes:
    """Load the poster stored beside this script, checking its header."""
    artwork_path = Path(__file__).resolve().parent / ARTWORK_FILENAME
    payload = artwork_path.read_bytes()
    if not payload.startswith(PNG_SIGNATURE):
        raise ValueError(
            f"{artwork_path} is not a PNG: bad signature "
            f"{payload[:8].hex()!r}"
        )
    return payload


def output_path() -> Path:
    """Resolve where the finished image belongs for this run."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return Path(folder) / ARTWORK_FILENAME


def place_artwork() -> Path:
    """Copy the bundled poster to the output path and verify the copy."""
    payload = read_bundled_artwork()
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)

    on_disk = target.read_bytes()
    if on_disk != payload:
        raise OSError(f"{target} does not match the bundled artwork")
    if not on_disk.startswith(PNG_SIGNATURE):
        raise ValueError(f"{target} lost its PNG signature while writing")
    return target


def main() -> int:
    target = place_artwork()
    print(f"delivered {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
