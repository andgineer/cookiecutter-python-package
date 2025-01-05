#!/usr/bin/env bash
#
# "Set-ups or/and activates development environment"
#
{% if cookiecutter.anaconda %}
ENV_NAME="{{ cookiecutter.package_name }}"
ENV_FILE="environment.yml"
{% else %}
VENV_FOLDER=".venv"
{% endif %}
PRIMARY_PYTHON_VERSION="3.12"  # sync with .github/workflows/docs.yml&static.yml

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

if ! (return 0 2>/dev/null) ; then
    # If return is used in the top-level scope of a non-sourced script,
    # an error message is emitted, and the exit code is set to 1
    echo
    echo -e $RED"This script should be sourced like"$NC
    echo "    . ./activate.sh"
    echo
    exit 1
fi

{% if cookiecutter.anaconda %}
if [[ ! -d "$HOME/anaconda3/" ]] ; then
  echo -e $RED"(!) Please install anaconda https://docs.anaconda.com/anaconda/install/"$NC
  return 1  # we are source'd so we cannot use exit
fi

source "$HOME/anaconda3/bin/activate"
conda init

if conda info --envs | grep "\b${ENV_NAME}\s"; then
  echo -e $CYAN"activating environment ${ENV_NAME}"$NC
else
  if [[ -z $(conda list --name base | grep "^mamba ") ]]; then
    echo -e $CYAN"..installing mamba.."$NC
    conda install mamba>=2.0.5 --name base --channel conda-forge --yes
  fi
  echo -e $CYAN"..creating environment ${ENV_NAME} with ${PRIMARY_PYTHON_VERSION}.."$NC
  conda create -y -n ${ENV_NAME} python="${PRIMARY_PYTHON_VERSION}"
  conda activate ${ENV_NAME}
  echo -e $CYAN"..installing dependencies from ${ENV_FILE}.."$NC
  mamba env update --quiet -n ${ENV_NAME} -f ${ENV_FILE}
  pip install -e .
  conda deactivate  # RE-activate conda env so python will have access to conda installed deps
fi

conda activate ${ENV_NAME}
{% else %}
if [[ ! -d ${VENV_FOLDER} ]] ; then
    unset CONDA_PREFIX  # if conda is installed, it will mess with the virtual env

    echo -e $CYAN"Creating virtual environment for python in ${VENV_FOLDER}"$NC
    START_TIME=$(date +%s)

    # Check if the required Python version is installed
    if ! command -v python${PRIMARY_PYTHON_VERSION} &> /dev/null; then
        echo -e $RED"Error: Python ${PRIMARY_PYTHON_VERSION} is not installed."$NC
        echo -e $YELLOW"Please install Python ${PRIMARY_PYTHON_VERSION} before proceeding."$NC
        echo -e $YELLOW"You can download it from https://www.python.org/downloads/"$NC
        return 1
    fi
    {% if cookiecutter.uv %}
    if command -v uv &> /dev/null; then
        if uv venv ${VENV_FOLDER} --python=python${PRIMARY_PYTHON_VERSION}; then
    {% else %}
    if command -v virtualenv &> /dev/null; then
        if virtualenv ${VENV_FOLDER} --python=python${PRIMARY_PYTHON_VERSION}; then
            python -m venv ${VENV_FOLDER}
    {% endif %}
            . ${VENV_FOLDER}/bin/activate{% if cookiecutter.dependencies == "uv" %}
            uv sync --frozen{% else %}
            {% if cookiecutter.uv %}uv {% endif %}pip install --upgrade pip
            {% if cookiecutter.uv %}uv {% endif %}pip install -r requirements.dev.txt
            {% endif %}
            END_TIME=$(date +%s)
            echo "Environment created in $((END_TIME - $START_TIME)) seconds"
        else
            echo -e $RED"Error creating virtual environment. Please check the output above for more details."$NC
            return 1
        fi
    else
        {% if cookiecutter.uv %}
        echo -e $RED"Error: Astral's UV is not installed."$NC
        echo -e $YELLOW"Please install UV from https://github.com/astral-sh/uv before proceeding."$NC
        {% else %}
        echo -e $RED"Error: Virtualenv is not installed."$NC
        echo -e $YELLOW"Please install Virtualenv from https://virtualenv.pypa.io/en/latest/ before proceeding."$NC
        {% endif %}
        return 1
    fi
else
    echo -e $CYAN"Activating virtual environment ..."$NC
    . ${VENV_FOLDER}/bin/activate
fi
{% endif %}