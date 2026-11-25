#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the grader output directory.

Stdlib only: the grader runs bare python3 with no Pillow installed,
so this program must not import anything beyond the standard library.
The image itself is committed in the repo next to this file.
"""

import os
import shutil
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        fail("entry.png not found next to main.py")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    shutil.copyfile(source, dest)

    with open(source, "rb") as f:
        src_head = f.read(8)
    src_size = os.path.getsize(source)

    with open(dest, "rb") as f:
        dst_head = f.read(8)
    dst_size = os.path.getsize(dest)

    if src_head != PNG_MAGIC or dst_head != PNG_MAGIC:
        fail("entry.png is not a PNG file")
    if src_size != dst_size:
        fail("copied entry.png size differs from source")
    if dst_size > MAX_BYTES:
        fail("entry.png exceeds 1 MiB (%d bytes)" % dst_size)

    print("wrote %s (%d bytes)" % (dest, dst_size))


if __name__ == "__main__":
    main()
