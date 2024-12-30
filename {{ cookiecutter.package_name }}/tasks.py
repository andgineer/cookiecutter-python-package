import os
import shutil
import sys

from invoke import task, Context, Collection
import subprocess


def get_allowed_doc_languages():
    build_docs_file_name = "scripts/build-docs.sh"
    try:
        with open(build_docs_file_name, "r") as f:
            for line in f:
                if "for lang in" in line:
                    langs = line.split("in")[1].strip().split(";")[0].split()
                    return [lang.strip() for lang in langs]
    except FileNotFoundError:
        print(f"No {build_docs_file_name} file found")
    return ["en", "bg", "de", "es", "fr", "ru"]  # default


ALLOWED_DOC_LANGUAGES = get_allowed_doc_languages()
ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]

{% if cookiecutter.docker %}
DOCKER_NAME = "{{ cookiecutter.package_name }}"  # default name for Docker image
DOCKER_FOLDERS = {"": "."}  # <image name>: <build context folder>
BUILD_TASK_PREFIX = 'build'
{% endif %}

@task
def version(c: Context):
    """Show the current version."""
    with open("src/{{ cookiecutter.package_name }}/__about__.py", "r") as f:
        version_line = f.readline()
        version_num = version_line.split('"')[1]
        print(version_num)
        return version_num


def ver_task_factory(version_type: str):
    @task
    def ver(c: Context):
        """Bump the version."""
        c.run(f"./scripts/verup.sh {version_type}")

    return ver


{% if cookiecutter.dependencies != "uv" %}
@task
def compile_requirements(c: Context):
    "Convert requirements.in to requirements.txt and requirements.dev.txt."
    start_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("{% if cookiecutter.uv %}uv pip compile{% else %}pip-compile{% endif %} requirements.in --output-file=requirements.txt --upgrade")  # --refresh-package
    reqs_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("{% if cookiecutter.uv %}uv pip compile{% else %}pip-compile{% endif %} requirements.dev.in --output-file=requirements.dev.txt --upgrade")
    end_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    print(f"Req's compilation time: {int(reqs_time) - int(start_time)} seconds")
    print(f"Req's dev compilation time: {int(end_time) - int(reqs_time)} seconds")
    print(f"Total execution time: {int(end_time) - int(start_time)} seconds")

    {% if cookiecutter.pyproject %}
    c.run("scripts/include_pyproject_requirements.py requirements.in")
    {% endif %}


@task(pre=[compile_requirements]){% endif %}
def reqs(c: Context):
    """Upgrade requirements including pre-commit."""
    c.run("pre-commit autoupdate"){% if cookiecutter.dependencies == "uv" %}
    c.run("uv lock --upgrade"){% else %}
    c.run("{% if cookiecutter.uv %}uv {% endif %}pip install -r requirements.dev.txt")
    {% endif %}
    

def docs_task_factory(language: str):
    @task
    def docs(c: Context):
        """Docs preview for the language specified."""
        c.run("open -a 'Google Chrome' http://127.0.0.1:8000/{{ cookiecutter.package_name }}/")
        c.run(f"scripts/docs-render-config.sh {language}")
        if language != "en":
            shutil.rmtree(f"./docs/src/{language}/images", ignore_errors=True)
            shutil.copytree("./docs/src/en/images", f"./docs/src/{language}/images")
            shutil.copy("./docs/src/en/reference.md", f"./docs/src/{language}/reference.md")
        c.run("mkdocs serve -f docs/_mkdocs.yml")

    return docs


@task
def uv(c: Context):
    """Install or upgrade uv."""
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh")


@task
def pre(c):
    """Run pre-commit checks"""
    c.run("pre-commit run --verbose --all-files")

{% if cookiecutter.docker %}
def docker_build_task_factory(name, target_dir):
    @task
    def docker_build(c):
        """Build Docker image. Place local-specific setup scripts to ../../docker-scripts."""
        shared_scripts_dir = "../../docker-scripts"
        scripts_copy_dir = os.path.join(target_dir, '.setup-scripts')
        try:
            args = ""
            if os.path.exists(shared_scripts_dir):
                os.makedirs(scripts_copy_dir, exist_ok=True)
                shutil.copytree(shared_scripts_dir, scripts_copy_dir, dirs_exist_ok=True)
                args += f" --build-arg SSL_CERT_FILE=/usr/local/share/ca-certificates/custom_cacert.crt"
            args += f" -t {DOCKER_NAME if name == BUILD_TASK_PREFIX else name.split('-')[-1]}"
            c.run(f"docker build {args} {target_dir}")
        finally:
            if os.path.exists(scripts_copy_dir):
                shutil.rmtree(scripts_copy_dir)
                pass

    return docker_build
{% endif %}

namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")
for name in ALLOWED_DOC_LANGUAGES:
    namespace.add_task(docs_task_factory(name), name=f"docs-{name}")
{% if cookiecutter.docker %}
for name, folder in DOCKER_FOLDERS.items():
    task_name = f"{BUILD_TASK_PREFIX}-{name}" if name else BUILD_TASK_PREFIX
    namespace.add_task(docker_build_task_factory(task_name, folder), name=task_name)
{% endif %}