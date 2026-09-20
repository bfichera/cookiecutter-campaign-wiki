"""MkDocs macros module.

Exposes a `statblock(path)` macro that renders a D&D 5e (2014) stat block from a
YAML file into styled HTML. Paths are resolved relative to the docs directory
(``content/``), or relative to the current page's directory.
"""

import os

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "overrides")

_env = Environment(
    loader=FileSystemLoader(_TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml", "j2"]),
)


def _ability_mod(score):
    try:
        score = int(score)
    except (TypeError, ValueError):
        return ""
    mod = (score - 10) // 2
    return "+{}".format(mod) if mod >= 0 else str(mod)


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def define_env(env):
    """Hook picked up by mkdocs-macros-plugin."""

    docs_dir = env.conf["docs_dir"]

    @env.macro
    def statblock(path):
        # Resolve relative to the current page first, then to docs_dir.
        candidates = []
        page = env.variables.get("page")
        if page is not None and getattr(page, "file", None) is not None:
            page_dir = os.path.dirname(page.file.abs_src_path)
            candidates.append(os.path.join(page_dir, path))
        candidates.append(os.path.join(docs_dir, path))
        candidates.append(path)

        src = next((p for p in candidates if os.path.isfile(p)), None)
        if src is None:
            return (
                '<div class="statblock-error">Statblock not found: '
                "<code>{}</code></div>".format(path)
            )

        with open(src, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}

        template = _env.get_template("statblock.html.j2")
        return template.render(sb=data, mod=_ability_mod, as_list=_as_list)

    # Make helpers available inside pages too, if ever useful.
    env.filter(_ability_mod, name="ability_mod")
