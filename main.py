#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261119.

The entry is one image: entry.png beside this file, a broadsheet front
page summing up the world news of Thursday 19 November 2026. The
program's whole job is to place that image at /output/entry.png (or at
$MAKEFUN_OUTPUT_DIR/entry.png when run outside the grader's container).

It uses only the Python standard library, reads nothing from the
network, and writes the same bytes on every run.

Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.png"
        shutil.copyfile(SOURCE, target)
    except OSError:
        # Fall back to a local ./output when /output is not writable
        # (e.g. a developer machine rather than the grader's container).
        target = Path.cwd() / "output" / "entry.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE, target)
    data = target.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry image is not a PNG"
    print(f"entry.png written: {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
