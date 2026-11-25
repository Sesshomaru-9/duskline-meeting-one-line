#!/usr/bin/env python3
"""Duskline Meeting One Line — make.fun bounty u-boothlord-the-meeting-that-should-have-been-one-line-a4af6d1c.

One deadpan line that could have replaced an entire pointless meeting,
written to $MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, standard library
only, no network access. The program never writes into its own repository:
when the output directory is the repo itself (or inside it) it refuses
quietly and exits 0. Nothing here ever raises: any failure exits 0 having
written nothing.
"""

import os
import sys
import tempfile

LINE = (
    "No update, no decision, and nobody in this room can make one \u2014 "
    "see you at the same meeting next week."
)
# The joke: a roll-call of everything the meeting failed to produce — no
# update, no decision, nobody empowered to decide — capped by the sting
# that the same empty meeting recurs next week anyway. The meeting is the
# butt of it, never any one person in it.

HERE = os.path.dirname(os.path.abspath(__file__))


def _inside_repo(directory):
    """True when directory is the repo dir or lives inside it."""
    try:
        target = os.path.realpath(directory)
        root = os.path.realpath(HERE)
    except Exception:
        return True
    return target == root or target.startswith(root + os.sep)


def _valid(line):
    if not line or line != line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    if not 1 <= len(line) <= 200:
        return False
    try:
        line.encode("utf-8")
    except Exception:
        return False
    return True


def run():
    if not _valid(LINE):
        return 0

    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not out:
        try:
            out = tempfile.mkdtemp(prefix="duskline-meeting-one-line-")
        except Exception:
            return 0
    if _inside_repo(out):
        return 0

    try:
        os.makedirs(out, exist_ok=True)
    except Exception:
        return 0
    path = os.path.join(out, "entry.txt")
    if _inside_repo(path):
        return 0

    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(LINE)
        with open(path, "r", encoding="utf-8") as handle:
            if handle.read() != LINE:
                raise ValueError("round-trip mismatch")
    except Exception:
        try:
            os.remove(path)
        except Exception:
            pass
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(run())
