#!/usr/bin/env python3
"""Mechanically move a reviewed draft out of inbox/ into archive/.

Not a judgment call: the tool moves the file exactly as reviewed and
date-stamps it to pair with its review file. The inbox holds only drafts
awaiting review.

Usage: python tools/archive.py inbox/<draft.md>

Exit codes: 0 moved, 1 refused (not in inbox, missing, or name collision).
"""

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
ARCHIVE = ROOT / "archive"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    src = Path(sys.argv[1]).resolve()
    if not src.exists():
        print("archive: not found: %s" % src)
        return 1
    if src.parent != INBOX:
        print("archive: refusing, %s is not in inbox/" % src.name)
        return 1
    if src.name == "README.md":
        print("archive: refusing, README.md stays in inbox/")
        return 1
    ARCHIVE.mkdir(exist_ok=True)
    dest = ARCHIVE / ("%s-%s" % (date.today().isoformat(), src.name))
    if dest.exists():
        print("archive: refusing, %s already exists" % dest)
        return 1
    src.rename(dest)
    print("archived: inbox/%s -> archive/%s" % (src.name, dest.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
