"""{{ cookiecutter.package_name }}."""

from pathlib import Path

import rich_click as click

from {{ cookiecutter.project_slug }} import __version__

click.rich_click.USE_MARKDOWN = True
OUTPUT_FILE_DEFAULT = "output"

@click.command()
@click.version_option(version=__version__, prog_name="{{ cookiecutter.package_name }}")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(), required=False)
@click.option("--force", is_flag=True, help="Overwrite the output file if it exists.")
def {{ cookiecutter.project_slug }}(
    input_file: str, output_file: str, force: bool
) -> None:
    """
    `INPUT_FILE` to `OUTPUT_FILE`.
    """
    output_path = (
        Path(output_file)
        if output_file
        else Path(input_file).parent / f"{OUTPUT_FILE_DEFAULT}.txt"
    )
    if output_path.exists() and not force:
        click.echo(f"Output file {output_path} already exists. Use --force to overwrite.")
        raise click.Abort()

    click.echo(f"File saved to {output_path}")


if __name__ == "__main__":  # pragma: no cover
    {{ cookiecutter.project_slug }}()  # pylint: disable=no-value-for-parameter
