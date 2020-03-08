#!/usr/bin/env python3

import sys

from time import strftime
from pathlib import Path

# Add parent folder
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from wilfred.version import version, commit_hash


def main():
    with open("debian/changelog") as f:
        raw = f.read()

    raw = raw.replace("{VERSION}", commit_hash if version == "0.0.0.dev0" else version)
    raw = raw.replace("{HASH}", commit_hash)
    raw = raw.replace("{DATE}", strftime("%a, %d %b %Y %H:%M:%S +0100"))

    with open("debian/changelog", "w") as f:
        f.write(raw)


if __name__ == "__main__":
    main()
