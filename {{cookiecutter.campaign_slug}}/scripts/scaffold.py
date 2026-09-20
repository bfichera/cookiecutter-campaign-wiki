#!/usr/bin/env python3
"""Scaffold new campaign content.

Usage:
    python scripts/scaffold.py encounter "The Old Bridge"
    python scripts/scaffold.py character kael
    python scripts/scaffold.py monster dire_wolf
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
ENCOUNTERS = os.path.join(CONTENT, "encounters")
CHARACTERS = os.path.join(CONTENT, "characters")
MONSTERS = os.path.join(CONTENT, "monsters")

_ENC_RE = re.compile(r"^(\d+)_")


def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def titleize(slug):
    return slug.replace("_", " ").title()


def next_encounter_number():
    if not os.path.isdir(ENCOUNTERS):
        return 1
    highest = 0
    for name in os.listdir(ENCOUNTERS):
        m = _ENC_RE.match(name)
        if m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


STATBLOCK_STUB = """\
name: {name}
size: Medium
type: humanoid
alignment: unaligned
ac: 10
hp: 1
speed: 30 ft.
str: 10
dex: 10
con: 10
int: 10
wis: 10
cha: 10
senses: passive Perception 10
languages: Common
cr: null
traits: []
actions:
  - name: Unarmed Strike
    desc: "Melee Weapon Attack: +2 to hit, reach 5 ft., one target. Hit: 1 bludgeoning damage."
"""


def make_encounter(name):
    os.makedirs(ENCOUNTERS, exist_ok=True)
    slug = slugify(name)
    number = "{:02d}".format(next_encounter_number())
    filename = "{}_{}.md".format(number, slug)
    path = os.path.join(ENCOUNTERS, filename)
    if os.path.exists(path):
        print("error: {} already exists".format(path), file=sys.stderr)
        return 1
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# {}\n\n".format(titleize(slug)))
        fh.write('!!! quote "Read aloud"\n    Describe the scene here.\n\n')
        fh.write("## Setup\n\nWhat happens when the party arrives.\n\n")
        fh.write("## Combatants\n\n")
        fh.write("<!-- {% raw %}{{ statblock('monsters/<name>.yml') }}{% endraw %} -->\n")
    # Optional adjacent images folder.
    imgdir = os.path.join(ENCOUNTERS, "{}_{}.images".format(number, slug))
    os.makedirs(imgdir, exist_ok=True)
    open(os.path.join(imgdir, ".gitkeep"), "a").close()
    print("Created {}".format(os.path.relpath(path, ROOT)))
    return 0


def make_character(name):
    slug = slugify(name)
    cdir = os.path.join(CHARACTERS, slug)
    if os.path.isdir(cdir):
        print("error: character '{}' already exists".format(slug), file=sys.stderr)
        return 1
    os.makedirs(cdir)
    with open(os.path.join(cdir, "description.md"), "w", encoding="utf-8") as fh:
        fh.write("# {}\n\n".format(titleize(slug)))
        fh.write("_Class, background._\n\n")
        fh.write("Backstory goes here.\n\n")
        fh.write("## Personality\n\n- **Trait:**\n- **Ideal:**\n- **Bond:**\n- **Flaw:**\n\n")
        fh.write("## Statistics\n")
    with open(os.path.join(cdir, "statblock.yml"), "w", encoding="utf-8") as fh:
        fh.write(STATBLOCK_STUB.format(name=titleize(slug)))
    print("Created {}".format(os.path.relpath(cdir, ROOT)))
    return 0


def make_monster(name):
    os.makedirs(MONSTERS, exist_ok=True)
    slug = slugify(name)
    path = os.path.join(MONSTERS, "{}.yml".format(slug))
    if os.path.exists(path):
        print("error: monster '{}' already exists".format(slug), file=sys.stderr)
        return 1
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(STATBLOCK_STUB.format(name=titleize(slug)))
    print("Created {}".format(os.path.relpath(path, ROOT)))
    return 0


def main(argv):
    if len(argv) < 2:
        print("usage: scaffold.py {encounter|character|monster} <name>", file=sys.stderr)
        return 2
    kind, name = argv[0], " ".join(argv[1:])
    if kind == "encounter":
        return make_encounter(name)
    if kind == "character":
        return make_character(name)
    if kind == "monster":
        return make_monster(name)
    print("error: unknown kind '{}'".format(kind), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
