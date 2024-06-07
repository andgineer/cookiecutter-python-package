import os

REMOVE_PATHS = [
    '{% if cookiecutter.scripts == "make" %}tasks.py{% endif %}',
    '{% if cookiecutter.scripts == "make" %}invoke.yml{% endif %}',
    '{% if cookiecutter.scripts == "invoke" %}Makefile{% endif %}',
    '{% if cookiecutter.scripts == "invoke" %}scripts/compile_requirements.sh{% endif %}',
    '{% if not cookiecutter.pyproject %}pyproject.toml{% endif %}',
    '{% if not cookiecutter.pyproject %}scripts/include_pyproject_requirements.py{% endif %}',
    '{% if cookiecutter.pyproject or cookiecutter.typechecker == "mypy"%}pyrightconfig.json{% endif %}',
    '{% if cookiecutter.pyproject %}.ruff.toml{% endif %}',
    '{% if cookiecutter.typechecker == "pyright" %}.mypy.ini{% endif %}',
    '{% if not cookiecutter.docker %}Dockerfile{% endif %}',
    '{% if not cookiecutter.docker %}build.sh{% endif %}',
    '{% if not cookiecutter.docker %}compose.sh{% endif %}',
    '{% if not cookiecutter.docker %}docker-compose.yml{% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        os.unlink(path) if os.path.isfile(path) else os.rmdir(path)
