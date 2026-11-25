#!/usr/bin/env python3
"""Duskline Meeting One Line — make.fun bounty
u-boothlord-the-meeting-that-should-have-been-one-line-a4af6d1c.

The entry is one deadpan sentence: the single line that could have
replaced an entire pointless meeting. This program writes that line, and
nothing else, to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.

Rules the program lives by:
  * Python standard library only, deterministic, no network.
  * Writes only to $MAKEFUN_OUTPUT_DIR (falling back to a temp dir
    outside the repository when the variable is unset).
  * Never writes into its own repository: when the output directory is
    the repo itself, or lives inside it, the program refuses quietly
    and exits 0 having written nothing.
  * Nothing here ever raises: any failure exits 0 having written
    nothing, so a bad run can never leave a partial entry behind.
"""

import os
import sys
import tempfile

# The entry, byte for byte. 101 characters, one line, one sentence.
# The em dash is written as the escape \u2014 so the source stays
# plain ASCII while the output is exactly the intended character.
LINE = (
    "No update, no decision, and nobody in this room can make one "
    "\u2014 see you at the same meeting next week."
)

# The joke: a roll-call of everything the meeting failed to produce —
# no update, no decision, nobody empowered to decide — capped by the
# sting that the same empty meeting recurs next week anyway. The
# meeting is the butt of it, never any one person in it.

ENTRY_NAME = "entry.txt"

# The repo root, used only to refuse writes that would land inside it.
REPO_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))


def is_inside_repo(path):
    """True when ``path`` is the repo dir or lives inside it."""
    try:
        target = os.path.realpath(path)
    except Exception:
        # If the path cannot be resolved, stay safe and treat it as inside.
        return True
    return target == REPO_ROOT or target.startswith(REPO_ROOT + os.sep)


def is_gate_valid(line):
    """Mirror of the sealed scorer's gate: 1-200 chars, UTF-8, one line,
    not only whitespace."""
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


def resolve_output_dir():
    """Return the directory to write into, or None to refuse quietly."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not out:
        try:
            out = tempfile.mkdtemp(prefix="duskline-meeting-one-line-")
        except Exception:
            return None
    if is_inside_repo(out):
        return None
    return out


def verify_entry(path):
    """True only when the file on disk matches LINE exactly."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read() == LINE
    except Exception:
        return False


def write_entry(directory):
    """Write the line to ``directory/entry.txt`` and verify the round
    trip. Returns True only when the file on disk matches LINE exactly."""
    path = os.path.join(directory, ENTRY_NAME)
    if is_inside_repo(path):
        return False
    try:
        os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(LINE)
        if not verify_entry(path):
            raise ValueError("round-trip mismatch")
    except Exception:
        try:
            os.remove(path)
        except Exception:
            pass
        return False
    return True


def run():
    if not is_gate_valid(LINE):
        return 0
    out = resolve_output_dir()
    if out is None:
        return 0
    write_entry(out)
    return 0


if __name__ == "__main__":
    sys.exit(run())
