#!/usr/bin/env python3
"""Update session.yml to record where the last session ended.

Usage:
    python scripts/mark_session.py 03_the_old_bridge

The argument may be given with or without the .md extension. It is validated
against the encounters in content/encounters/.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENCOUNTERS = os.path.join(ROOT, "content", "encounters")
SESSION = os.path.join(ROOT, "session.yml")
_RE = re.compile(r"^\d+_.+$")


def available():
    if not os.path.isdir(ENCOUNTERS):
        return []
    slugs = [
        f[:-3]
        for f in os.listdir(ENCOUNTERS)
        if f.endswith(".md") and _RE.match(f[:-3])
    ]
    return sorted(slugs)


def main(argv):
    if len(argv) != 1:
        print("usage: mark_session.py <encounter>", file=sys.stderr)
        return 2

    slug = argv[0]
    if slug.endswith(".md"):
        slug = slug[:-3]

    slugs = available()
    if slug not in slugs:
        print("error: unknown encounter '{}'".format(slug), file=sys.stderr)
        if slugs:
            print("available encounters:", file=sys.stderr)
            for s in slugs:
                print("  - {}".format(s), file=sys.stderr)
        return 1

    with open(SESSION, "w", encoding="utf-8") as fh:
        fh.write("# Where the last session ended. Set with: make mark-session-end <encounter>\n")
        fh.write("current_encounter: {}\n".format(slug))

    print("Session marker set to: {}".format(slug))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
