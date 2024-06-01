"""{{ cookiecutter.package_description }}

The file is mandatory for build system to find the package.
"""

from {{ cookiecutter.project_slug }}.__about__ import __version__

__all__ = ["__version__"]
