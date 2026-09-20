VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MKDOCS := $(VENV)/bin/mkdocs

# Silences an unsolicited advertisement some dependencies print during builds.
export DISABLE_MKDOCS_2_WARNING := true

# Grab every word after the first goal as arguments, e.g.
#   make mark-session-end 03_the_old_bridge
#   make new-encounter "The Old Bridge"
# $(firstword ...) is the real target; the rest are treated as arguments and
# swallowed by the catch-all rule at the bottom.
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

.PHONY: help setup serve build clean mark-session-end new-encounter new-character new-monster

help:
	@echo "Campaign wiki commands:"
	@echo "  make setup                              create venv and install dependencies"
	@echo "  make serve                              live-reloading wiki at http://127.0.0.1:8000"
	@echo "  make build                              render static site into ./site"
	@echo "  make clean                              remove the built site"
	@echo "  make mark-session-end <encounter>       set the 'start here next' marker"
	@echo "  make new-encounter \"Name\"               scaffold the next NN_*.md encounter"
	@echo "  make new-character <name>               scaffold a character folder"
	@echo "  make new-monster <name>                 scaffold a monster statblock"

$(VENV):
	python3 -m venv $(VENV)

setup: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

serve:
	$(MKDOCS) serve

build:
	$(MKDOCS) build --clean

clean:
	rm -rf site

mark-session-end:
	@$(PY) scripts/mark_session.py $(ARGS)

new-encounter:
	@$(PY) scripts/scaffold.py encounter $(ARGS)

new-character:
	@$(PY) scripts/scaffold.py character $(ARGS)

new-monster:
	@$(PY) scripts/scaffold.py monster $(ARGS)

# Swallow the extra argument words so make doesn't treat them as targets.
%:
	@:
