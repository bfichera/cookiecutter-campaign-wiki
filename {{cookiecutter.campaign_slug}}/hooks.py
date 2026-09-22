"""MkDocs build hooks for the session marker.

Reads ``session.yml`` (``current_encounter``), works out the *next* encounter in
numeric order, and:

  * injects a "start here next" banner where the homepage has the
    ``<!-- SESSION_BANNER -->`` placeholder;
  * prepends a highlight callout to the next encounter's page;
  * tints encounters up to and including the marker as "played".

The session file is also registered as a watched path so ``mkdocs serve``
re-renders when ``make mark-session-end`` changes it.
"""

import os
import re

import yaml

_ENCOUNTER_RE = re.compile(r"^(\d+)_(.+)\.md$")


def _add_callout(markdown, callout):
    lines = markdown.splitlines()
    return lines[0] + '\n' + callout + '\n'.join(lines[1:])


def _project_dir(config):
    return os.path.dirname(os.path.abspath(config["config_file_path"]))


def _load_marker(config):
    path = os.path.join(_project_dir(config), "session.yml")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("current_encounter")


def _encounters_dir(config):
    return os.path.join(config["docs_dir"], "encounters")


def _ordered_encounters(config):
    """Return [(slug, filename, pretty_title), ...] sorted by numeric prefix."""
    directory = _encounters_dir(config)
    if not os.path.isdir(directory):
        return []
    items = []
    for name in os.listdir(directory):
        m = _ENCOUNTER_RE.match(name)
        if not m:
            continue
        number, rest = m.groups()
        slug = name[:-3]  # strip .md
        pretty = rest.replace("_", " ").title()
        items.append((int(number), slug, name, pretty))
    items.sort(key=lambda t: t[0])
    return [(slug, name, pretty) for _, slug, name, pretty in items]


def _titleize(slug):
    return re.sub(r"^\d+_", "", slug).replace("_", " ").title()


# --- exposed state, computed lazily per build ------------------------------

_STATE = {}


def on_config(config, **kwargs):
    marker = _load_marker(config)
    encounters = _ordered_encounters(config)
    slugs = [slug for slug, _, _ in encounters]

    next_slug = None
    played = set()
    if marker in slugs:
        idx = slugs.index(marker)
        played = set(slugs[: idx + 1])
        if idx + 1 < len(slugs):
            next_slug = slugs[idx + 1]
    elif marker is None and slugs:
        # Nothing marked yet: the very first encounter is "next".
        next_slug = slugs[0]

    _STATE["marker"] = marker
    _STATE["next_slug"] = next_slug
    _STATE["played"] = played

    # Keep the browser live-reloading when the marker changes.
    try:
        server = kwargs.get("server")
    except Exception:
        server = None
    if server is not None:
        server.watch(os.path.join(_project_dir(config), "session.yml"))
    return config


def on_serve(server, config, builder, **kwargs):
    server.watch(os.path.join(_project_dir(config), "session.yml"))
    return server


def _banner_markdown():
    next_slug = _STATE.get("next_slug")
    if not next_slug:
        return (
            '<div class="session-banner" markdown="0">'
            "\N{PARTY POPPER} No upcoming encounter marked yet. "
            "Set one with <code>make mark-session-end &lt;encounter&gt;</code>."
            "</div>"
        )
    title = _titleize(next_slug)
    return (
        '<div class="session-banner" markdown="0">'
        "\N{BLACK RIGHT-POINTING TRIANGLE} <strong>Start here next:</strong> "
        '<a href="../encounters/{slug}/">{title}</a>'
        "</div>".format(slug=next_slug, title=title)
    )


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_path.replace("\\", "/")

    # Homepage banner.
    if "<!-- SESSION_BANNER -->" in markdown:
        markdown = markdown.replace("<!-- SESSION_BANNER -->", _banner_markdown())

    # Encounter pages: highlight next / tint played.
    if src.startswith("encounters/") and src.endswith(".md"):
        slug = os.path.basename(src)[:-3]
        if slug == _STATE.get("next_slug"):
            callout = (
                '<div class="encounter-next" markdown="0">'
                "\N{BLACK RIGHT-POINTING TRIANGLE} Start here \N{EM DASH} "
                "this is the next encounter."
                "</div>\n\n"
            )
            markdown = _add_callout(markdown, callout)
        elif slug in _STATE.get("played", set()):
            callout = (
                '<div class="encounter-played" markdown="0">'
                "\N{HEAVY CHECK MARK} Already played."
                "</div>\n\n"
            )
            markdown = _add_callout(markdown, callout)

    return markdown
