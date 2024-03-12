#!/usr/bin/env bash
#
# Extract docstrings to docs/
# make a copy for all languages
#

lazydocs \
    --output-path="./docs/src/en/api-reference" \
    --overview-file="index.md" \
    --src-base-url="https://github.com/andgineer/{{ cookiecutter.package_name }}/blob/master/" \
    src/{{ cookiecutter.project_slug }}

cp -r ./docs/src/en/api-reference ./docs/src/ru/api-reference
