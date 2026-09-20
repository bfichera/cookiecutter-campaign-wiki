"""Auto-generate browsable pages at build time (mkdocs-gen-files).

  * Bestiary:   one page per content/monsters/*.yml, plus an index.
  * Characters: one page per content/characters/<name>/ combining
                description.md with the embedded statblock, plus an index.

Generated pages are virtual (they don't touch your source tree) and use the
`statblock` macro so they stay consistent with inline embeds.
"""

import os

import mkdocs_gen_files
import yaml

DOCS = "content"
MONSTERS = os.path.join(DOCS, "monsters")
CHARACTERS = os.path.join(DOCS, "characters")


def _title_from_slug(slug):
    return slug.replace("_", " ").title()


def gen_bestiary():
    if not os.path.isdir(MONSTERS):
        return
    files = sorted(f for f in os.listdir(MONSTERS) if f.endswith((".yml", ".yaml")))
    entries = []
    for fname in files:
        slug = os.path.splitext(fname)[0]
        with open(os.path.join(MONSTERS, fname), "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        name = data.get("name", _title_from_slug(slug))
        entries.append((slug, name))

        out_path = "bestiary/{}.md".format(slug)
        with mkdocs_gen_files.open(out_path, "w") as fh:
            fh.write("# {}\n\n".format(name))
            fh.write("{% raw %}{{ statblock('monsters/%s') }}{% endraw %}\n" % fname)
        mkdocs_gen_files.set_edit_path(out_path, os.path.join(MONSTERS, fname))

    with mkdocs_gen_files.open("bestiary/index.md", "w") as fh:
        fh.write("# Bestiary\n\n")
        if not entries:
            fh.write("_No monsters yet. Add one with_ `make new-monster <name>`.\n")
        for slug, name in entries:
            fh.write("- [{}]({}.md)\n".format(name, slug))


def gen_characters():
    if not os.path.isdir(CHARACTERS):
        return
    names = sorted(
        d for d in os.listdir(CHARACTERS)
        if os.path.isdir(os.path.join(CHARACTERS, d))
    )
    entries = []
    for name in names:
        cdir = os.path.join(CHARACTERS, name)
        desc_path = os.path.join(cdir, "description.md")
        statblock_path = os.path.join(cdir, "statblock.yml")

        display = _title_from_slug(name)
        body = ""
        if os.path.isfile(desc_path):
            with open(desc_path, "r", encoding="utf-8") as fh:
                body = fh.read()

        out_path = "characters/{}.md".format(name)
        with mkdocs_gen_files.open(out_path, "w") as fh:
            if body.strip():
                fh.write(body)
                if not body.endswith("\n"):
                    fh.write("\n")
            else:
                fh.write("# {}\n\n".format(display))
            if os.path.isfile(statblock_path):
                fh.write("\n{% raw %}{{ statblock('characters/%s/statblock.yml') }}{% endraw %}\n" % name)
        mkdocs_gen_files.set_edit_path(out_path, desc_path)
        entries.append((name, display))

    with mkdocs_gen_files.open("characters/index.md", "w") as fh:
        fh.write("# Characters\n\n")
        if not entries:
            fh.write("_No characters yet. Add one with_ `make new-character <name>`.\n")
        for name, display in entries:
            fh.write("- [{}]({}.md)\n".format(display, name))


gen_bestiary()
gen_characters()
