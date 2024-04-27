import os

REMOVE_PATHS = [
    '{% if cookiecutter.scripts == "make" %}tasks.py{% endif %}',
    '{% if cookiecutter.scripts == "invoke" %}Makefile{% endif %}',
    '{% if cookiecutter.scripts == "invoke" %}scripts/compile_requirements.sh{% endif %}',
    '{% if not cookiecutter.pyproject %}pyproject.toml{% endif %}',
    '{% if not cookiecutter.pyproject %}scripts/include_pyproject_requirements.py{% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        os.unlink(path) if os.path.isfile(path) else os.rmdir(path)
