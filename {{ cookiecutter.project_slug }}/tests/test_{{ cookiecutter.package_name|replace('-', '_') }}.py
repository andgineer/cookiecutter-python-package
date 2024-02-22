from {{ cookiecutter.project_slug }}.__about__ import __version__


def test_version():
    assert __version__
