# cookiecutter-campaign-wiki

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for a self-rendering
tabletop RPG campaign wiki, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

Write your campaign in Markdown and YAML with vim (or anything), and get a
beautiful, dark-themeable static site you can flip through at the table.

## Features

- **Encounters** as ordered Markdown pages (`01_goblin_ambush.md`, `02_party_debrief.md`, ...)
  with auto-generated, correctly ordered navigation.
- **Characters** — each is a folder with a `description.md` bio and a `statblock.yml`.
  Bios and stat blocks are combined into one page automatically.
- **Monsters** as `statblock.yml` files, collected into an auto-generated **Bestiary**.
- **D&D 5e statblocks** rendered from YAML into a classic styled stat block via a
  `{% raw %}{{ statblock('...') }}{% endraw %}` macro you can drop into any page.
- **Session marker** — `session.yml` records where you left off. The homepage shows a
  "start here next" banner, the next encounter is highlighted, and played encounters
  are tinted. Update it with `make mark-session-end 03_the_old_bridge`.
- **Live reload** — `make serve` re-renders the site in your browser on every file change.

## Requirements

- Python 3.9+
- [Cookiecutter](https://cookiecutter.readthedocs.io/): `pipx install cookiecutter`
  (or `pip install cookiecutter`)

## Usage

```bash
cookiecutter /Users/bfichera/data/projects/cookiecutter-campaign-wiki
```

Answer the prompts:

| Prompt | Meaning |
| --- | --- |
| `campaign_name` | Human-readable title, used for the site name and homepage. |
| `campaign_slug` | Folder name (auto-derived; press Enter to accept). |
| `dm_name` | Shown on the homepage and in the footer. |
| `system` | Game system label. |
| `include_sample_content` | `yes` scaffolds example characters/monsters/encounters. |
| `initialize_git` | `yes` runs `git init` and makes a first commit. |

Then:

```bash
cd <your_campaign_slug>
make setup      # create venv + install deps
make serve      # http://127.0.0.1:8000  (auto-reloads on edits)
```

## Commands (in a generated campaign)

```bash
make setup                              # create venv and install dependencies
make serve                              # live-reloading wiki
make build                              # render static site into ./site
make mark-session-end 03_the_old_bridge # set the "start here next" marker
make new-encounter "The Old Bridge"     # scaffold the next NN_*.md encounter
make new-character kael                 # scaffold content/characters/kael/
make new-monster dire_wolf              # scaffold content/monsters/dire_wolf.yml
```
