#!make
VERSION := $(shell grep '__version__' src/{{ cookiecutter.project_slug }}/__about__.py | cut -d '"' -f2)
export VERSION
unexport CONDA_PREFIX  # if conda is installed, it will mess with the virtual env

# If the first argument is "docs" treat additional "targets" as parameters
ifeq (docs,$(firstword $(MAKECMDGOALS)))
  DOCS_LANGUAGE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # turn the parameters into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.HELP: version ## Show the current version
version:
	echo ${VERSION}

.HELP: ver-bug ## Bump the version for a bug
ver-bug:
	bash ./scripts/verup.sh bug

.HELP: ver-feature ## Bump the version for a feature
ver-feature:
	bash ./scripts/verup.sh feature

.HELP: ver-release ## Bump the version for a release
ver-release:
	bash ./scripts/verup.sh release

.HELP: reqs  ## Upgrade requirements including pre-commit
reqs:
	pre-commit autoupdate
    {% if cookiecutter.dependencies == "uv" %}
    uv lock --upgrade
    {% else %}
	bash ./scripts/compile_requirements.sh
	{% if cookiecutter.uv %}uv {% endif %}pip install -r requirements.dev.txt
    {% endif %}

.PHONY: docs # mark as phony so it always runs even we have a docs folder
.HELP: docs  ## Docs preview for the language specified (bg de en es fr ru)
docs:
	./scripts/docstrings.sh
	open -a "Google Chrome" http://127.0.0.1:8000/{{ cookiecutter.package_name }}/
	scripts/docs-render-config.sh $(DOCS_LANGUAGE)
	mkdocs serve -f docs/_mkdocs.yml


.HELP: uv  ## Install or upgrade uv
uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
