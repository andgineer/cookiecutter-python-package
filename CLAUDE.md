# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Cookiecutter template for generating Python package projects with comprehensive tooling. The repository generates project scaffolds with CI/CD, testing, documentation, and publishing workflows pre-configured.

## Key Architecture

### Template Structure

- **Root level**: Contains `cookiecutter.json` configuration and `hooks/` directory
- **`{{ cookiecutter.package_name }}/`**: The actual template directory that gets rendered when users run cookiecutter
- **`hooks/post_gen_project.py`**: Post-generation hook that removes files based on user choices (e.g., removes Makefile if user chose Invoke, removes requirements files if using uv lock)

### Cookiecutter Variables

The template uses Jinja2 templating with variables from `cookiecutter.json`:
- `package_name`: Kebab-case package name (e.g., 'my-awesome-package')
- `project_slug`: Python-safe name derived from package_name (underscores instead of hyphens)
- `scripts`: Choice between "invoke" (tasks.py) or "make" (Makefile)
- `uv`: Whether to use Astral's uv instead of virtualenv
- `anaconda`: Whether to use Anaconda environments
- `dependencies`: Choice between "uv" (uv.lock) or "pip-tools" (requirements.txt)
- `typechecker`: Choice between "mypy" or "pyright"
- `docker`: Whether to include Docker support

### Generated Project Architecture

#### Environment Management
- `activate.sh`: Sourced script (`. ./activate.sh`) that creates/activates virtual environments
  - Supports uv venv, virtualenv, or Anaconda
  - Checks for required Python version (3.12 by default)
  - Auto-installs dependencies on first run

#### Dependency Management
Generated projects support three approaches:
1. **uv lock** (modern, recommended): Uses `uv.lock` file and `uv sync --frozen`
2. **pip-tools**: Uses `requirements.in`/`requirements.dev.in` compiled to `.txt` files
3. **Anaconda**: Uses `environment.yml`

When using pip-tools, `scripts/include_pyproject_requirements.py` syncs requirements.txt into pyproject.toml's `project.dependencies` array.

#### Task Runners
Projects can use either:
- **Invoke** (`tasks.py`): Python-based task runner with dynamic task generation
- **Makefile**: Traditional make-based tasks

Both provide identical functionality:
- Version bumping: `ver-bug`, `ver-feature`, `ver-release`
- Dependency updates: `reqs`
- Documentation preview: `docs` (with language support)
- Pre-commit: `pre`

#### Version Management
Version bumping workflow via `scripts/verup.sh`:
1. Checks for uncommitted changes (must be clean)
2. Finds latest version tag from git
3. Increments version based on type (release/feature/bug)
4. Updates `src/{{ cookiecutter.project_slug }}/__about__.py`
5. Creates git commit and tag with changelog
6. Pushes tag (triggers PyPI publish workflow)

Version format: `v{major}.{minor}.{build}`
- `release`: Increments major, resets minor and build
- `feature`: Increments minor, resets build
- `bug`: Increments build

#### CI/CD Workflows
Located in `{{ cookiecutter.package_name }}/.github/workflows/`:

- **ci.yml**: Main CI workflow
  - Matrix build: Tests across Python 3.10, 3.11, 3.12 on Ubuntu, macOS, Windows
  - Primary build: Publishes Allure reports, coverage to coveralls/codecov
  - Uses `uv sync --frozen` (uv) or `pip install -r requirements.dev.txt` (pip-tools)

- **pip_publish.yml**: Triggered by version tags, publishes to PyPI

- **docs.yml**: Builds and publishes MkDocs documentation to GitHub Pages

- **static.yml**: Runs static analysis (ruff, mypy/pyright)

#### Documentation
- Uses MkDocs Material with multilingual support
- Docs in `docs/src/{lang}/` directories (en, ru, bg, de, es, fr)
- Auto-generates API reference from docstrings
- Published to GitHub Pages on gh-pages branch

## Common Development Commands

### Setting up a new project from this template
```bash
cookiecutter gh:andgineer/cookiecutter-python-package
```

Or for existing repository:
```bash
cookiecutter gh:andgineer/cookiecutter-python-package --overwrite-if-exists
```

### Testing template changes
When modifying the template, you'll need to:
1. Generate a test project: `cookiecutter . --overwrite-if-exists`
2. Test the generated project's functionality
3. Verify hooks execute correctly (check `hooks/post_gen_project.py`)

### Working with generated projects

#### Initial setup
```bash
. ./activate.sh  # Note the leading dot - must be sourced
pre-commit install
```

#### Running tests
```bash
pytest  # or make/invoke test if defined
```

#### Updating dependencies
With make:
```bash
make reqs
```

With invoke:
```bash
invoke reqs
```

#### Version bumping and release
```bash
make ver-feature  # or ver-bug, ver-release
# Or: invoke ver-feature
```

#### Preview documentation
```bash
make docs en  # English
make docs ru  # Russian
# Or: invoke docs-en, invoke docs-ru
```

## Important Template Patterns

### Conditional File Inclusion
The `post_gen_project.py` hook removes files based on cookiecutter choices. When adding new optional files, update `REMOVE_PATHS` list.

### Dynamic Task Generation
In `tasks.py`, tasks are dynamically generated using factory functions:
- `ver_task_factory()`: Creates version bump tasks for each type
- `docs_task_factory()`: Creates docs preview tasks for each language
- `docker_build_task_factory()`: Creates Docker build tasks when enabled

### Jinja2 Templating
Use `{% raw %}...{% endraw %}` blocks in workflow files to preserve `${{ }}` GitHub Actions syntax.

### Version Synchronization
Version is stored in `src/{{ cookiecutter.project_slug }}/__about__.py` and used by:
- hatchling build backend (reads via `tool.hatch.version.path`)
- Makefile (parses with grep/cut)
- Invoke tasks (reads file directly)

## Configuration Files

- **pyproject.toml**: Main project metadata, build config, tool settings (ruff, pyright)
- **invoke.yml**: Invoke task runner configuration (optional)
- **.pre-commit-config.yaml**: Pre-commit hooks for black, mypy, ruff
- **mkdocs.yml**: Documentation site configuration
- **docker-compose.yml**: Docker Compose setup (optional)
