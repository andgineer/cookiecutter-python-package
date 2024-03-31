from {{ cookiecutter.project_slug }}.__about__ import __version__
from {{ cookiecutter.project_slug }}.main import {{ cookiecutter.project_slug }}
from click.testing import CliRunner


def test_version():
    assert __version__


def test_version_option():
    runner = CliRunner()
    result = runner.invoke({{ cookiecutter.project_slug }}, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output
