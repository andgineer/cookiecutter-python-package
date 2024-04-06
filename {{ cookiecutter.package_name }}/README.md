[![Build Status](https://github.com/andgineer/{{ cookiecutter.package_name }}/workflows/CI/badge.svg)](https://github.com/andgineer/{{ cookiecutter.package_name }}/actions)
[![Coverage](https://raw.githubusercontent.com/andgineer/{{ cookiecutter.package_name }}/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/{{ cookiecutter.package_name }}/blob/python-coverage-comment-action-data/htmlcov/index.html)
# {{ cookiecutter.package_name }}

{{ cookiecutter.package_description }} 

# Documentation

[{{ cookiecutter.package_name|replace('-', ' ')|title }}](https://andgineer.github.io/{{ cookiecutter.package_name }}/)

# Developers

Do not forget to run `. ./activate.sh`.

# Scripts
Install [invoke](https://docs.pyinvoke.org/en/stable/) preferably with [pipx](https://pypa.github.io/pipx/):

    pipx install invoke

For a list of available scripts run:

    invoke --list

For more information about a script run:

    invoke <script> --help

## Coverage report
* [Codecov](https://app.codecov.io/gh/andgineer/{{ cookiecutter.package_name }}/tree/main/src%2F{{ cookiecutter.project_slug }})
* [Coveralls](https://coveralls.io/github/andgineer/{{ cookiecutter.package_name }})

> Created with cookiecutter using [template](https://github.com/andgineer/cookiecutter-python-package)