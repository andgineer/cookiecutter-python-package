#!/usr/bin/env bash
#
# Pin current dependencies versions.
#

# pin test / lint / docs dependencies for reproducibility
uv pipcompile requirements.dev.in

# pin requirements.in versions just as reference for potential incapability bugs in future
uv pipcompile requirements.in

# do not pin dependencies in the package
scripts/include_pyproject_requirements.py requirements.in
