#!/usr/bin/env bash
#
# Pin current dependencies versions.
#
unset CONDA_PREFIX  # if conda is installed, it will mess with the virtual env

START_TIME=$(date +%s)

{% if cookiecutter.uv %}uv pip compile{% else %}pip-compile{% endif %} requirements.in --output-file=requirements.txt  --upgrade
REQS_TIME=$(date +%s)

{% if cookiecutter.uv %}uv pip compile{% else %}pip-compile{% endif %} requirements.dev.in --output-file=requirements.dev.txt  --upgrade

END_TIME=$(date +%s)

echo "Req‘s compilation time: $((REQS_TIME - $START_TIME)) seconds"
echo "Req‘s dev compilation time: $((END_TIME - REQS_TIME)) seconds"
echo "Total execution time: $((END_TIME - $START_TIME)) seconds"

{% if cookiecutter.pyproject %}
# do not pin dependencies in the package
scripts/include_pyproject_requirements.py requirements.in
{% endif %}
