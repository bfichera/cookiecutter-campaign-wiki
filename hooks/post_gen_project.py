"""Post-generation hook.

Runs inside the freshly generated project directory. Handles the two things
Cookiecutter's plain templating can't: conditionally removing sample content
and initializing a git repository.
"""

import os
import shutil
import subprocess

INCLUDE_SAMPLE = "{{ cookiecutter.include_sample_content }}" == "yes"
INIT_GIT = "{{ cookiecutter.initialize_git }}" == "yes"

CONTENT = "content"


def rm(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    elif os.path.exists(path):
        os.remove(path)


def touch_gitkeep(directory):
    os.makedirs(directory, exist_ok=True)
    open(os.path.join(directory, ".gitkeep"), "a").close()


def strip_sample_content():
    """Remove the shipped examples and leave empty, tracked folders."""
    for sub in ("encounters", "characters", "monsters"):
        target = os.path.join(CONTENT, sub)
        rm(target)
        touch_gitkeep(target)

    # Reset the session marker so it points at nothing yet.
    with open("session.yml", "w") as fh:
        fh.write("# Where the last session ended. Set with: make mark-session-end <encounter>\n")
        fh.write("current_encounter: null\n")


def init_git():
    try:
        subprocess.run(["git", "init", "-q"], check=True)
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "Initial campaign scaffold"],
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  [warning] git initialization skipped (git not available or failed).")


def main():
    if not INCLUDE_SAMPLE:
        strip_sample_content()
    if INIT_GIT:
        init_git()
    print("\nCampaign '{{ cookiecutter.campaign_name }}' created.")
    print("Next steps:")
    print("  cd {{ cookiecutter.campaign_slug }}")
    print("  make setup && make serve")


if __name__ == "__main__":
    main()
