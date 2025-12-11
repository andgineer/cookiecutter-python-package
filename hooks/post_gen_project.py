import os
import sys

REMOVE_PATHS = [
    '{% if cookiecutter.scripts == "make" %}tasks.py{% endif %}',
    '{% if cookiecutter.scripts == "make" %}invoke.yml{% endif %}',
    '{% if cookiecutter.scripts == "invoke" %}Makefile{% endif %}',
    '{% if cookiecutter.scripts == "invoke" %}scripts/compile_requirements.sh{% endif %}',
    '{% if not cookiecutter.pyproject %}pyproject.toml{% endif %}',
    '{% if not cookiecutter.pyproject %}scripts/include_pyproject_requirements.py{% endif %}',
    '{% if cookiecutter.pyproject or cookiecutter.typechecker != "pyright"%}pyrightconfig.json{% endif %}',
    '{% if cookiecutter.pyproject %}.ruff.toml{% endif %}',
    '{% if cookiecutter.typechecker != "mypy" %}.mypy.ini{% endif %}',
    '{% if not cookiecutter.docker %}Dockerfile{% endif %}',
    '{% if not cookiecutter.docker %}.github/workflows/dockerhub.yml{% endif %}',
    '{% if not cookiecutter.docker %}build.sh{% endif %}',
    '{% if not cookiecutter.docker %}compose.sh{% endif %}',
    '{% if not cookiecutter.docker %}docker-compose.yml{% endif %}',
    '{% if cookiecutter.dependencies == "uv" or cookiecutter.anaconda %}scripts/compile_requirements.sh{% endif %}',
    '{% if cookiecutter.dependencies == "uv" or cookiecutter.anaconda %}scripts/include_pyproject_requirements.py{% endif %}',
    '{% if cookiecutter.dependencies == "uv" or cookiecutter.anaconda %}requirements.in{% endif %}',
    '{% if cookiecutter.dependencies == "uv" or cookiecutter.anaconda %}requirements.txt{% endif %}',
    '{% if cookiecutter.dependencies == "uv" or cookiecutter.anaconda %}requirements.dev.in{% endif %}',
    '{% if cookiecutter.dependencies == "uv" or cookiecutter.anaconda %}requirements.dev.txt{% endif %}',
    '{% if not cookiecutter.anaconda %}environment.yml{% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        os.unlink(path) if os.path.isfile(path) else os.rmdir(path)


def validate_inputs():
    use_conda = {{ cookiecutter.anaconda }}
    use_uv = {{ cookiecutter.uv }}

    if use_conda and use_uv:
        print("ERROR: If Anaconda env is selected we cannot use uv venv. Please choose only one.")
        sys.exit(1)
        
validate_inputs()
