"""REIXS CLI — validate, compile, and scaffold REIXS specs."""

import click


@click.group()
@click.version_option(package_name="reixs")
def cli():
    """REIXS — Real Estate Intelligence Execution Specification."""
    pass


@cli.command()
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--no-strict-sesf", is_flag=True, help="Treat SESF failures as warnings")
def validate(spec_file, json_output, no_strict_sesf):
    """Validate a REIXS spec file."""
    click.echo(f"Validating {spec_file}...")
    # TODO: wire up parser + validator


@cli.command()
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_dir", default="build", help="Output directory")
@click.option("--include-validation", is_flag=True, help="Include validation report")
def compile(spec_file, output_dir, include_validation):
    """Validate and compile a REIXS spec to runtime JSON."""
    click.echo(f"Compiling {spec_file} → {output_dir}/...")
    # TODO: wire up parser + validator + compiler


@cli.command()
@click.option("--template", type=str, help="Template name")
@click.option("-o", "--output", "output_file", default=None, help="Output file path")
@click.option("--list-templates", is_flag=True, help="List available templates")
def init(template, output_file, list_templates):
    """Scaffold a new REIXS spec from a template."""
    if list_templates:
        click.echo("Available templates:")
        click.echo("  lease-abstraction-ontario")
        return
    click.echo(f"Initializing from template: {template}")
    # TODO: wire up template copying
