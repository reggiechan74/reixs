"""REIXS CLI — validate, compile, and scaffold REIXS specs."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from reixs.compile.compiler import compile_reixs
from reixs.parser.markdown_parser import parse_reixs_markdown
from reixs.parser.section_model import build_reixs_spec
from reixs.validate import run_validation
from reixs.validate.report import ValidationReport

console = Console()

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "specs" / "templates"


def _parse_and_build(spec_file: str) -> tuple:
    """Parse and build a ReixsSpec from a file path."""
    filepath = Path(spec_file)
    try:
        sections = parse_reixs_markdown(filepath)
    except Exception as e:
        console.print(f"[red]Parse error:[/red] {e}")
        sys.exit(2)

    try:
        spec = build_reixs_spec(sections, filepath)
    except Exception as e:
        console.print(f"[red]Model error:[/red] {e}")
        sys.exit(2)

    return spec, filepath


def _print_report(report: ValidationReport) -> None:
    """Print validation report using Rich."""
    table = Table(title=f"REIXS Validation: {report.spec_id} v{report.spec_version}")
    table.add_column("Pass", style="dim", width=8)
    table.add_column("Severity", width=10)
    table.add_column("Section", width=18)
    table.add_column("Message")

    severity_styles = {
        "error": "red bold",
        "warning": "yellow",
        "info": "dim",
    }

    for f in report.findings:
        style = severity_styles.get(f.severity, "")
        table.add_row(
            str(f.pass_number),
            f"[{style}]{f.severity}[/{style}]",
            f.section or "",
            f.message,
        )

    console.print(table)

    status_style = {"pass": "green", "warn": "yellow", "fail": "red bold"}
    s = status_style.get(report.status, "")
    console.print(f"\nStatus: [{s}]{report.status.upper()}[/{s}]")
    console.print(
        f"  {len(report.errors)} error(s), "
        f"{len(report.warnings)} warning(s), "
        f"{sum(1 for f in report.findings if f.severity == 'info')} info(s)"
    )


@click.group()
@click.version_option(package_name="reixs")
def cli():
    """REIXS — Real Estate Intelligence Execution Specification."""
    pass


@cli.command()
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--no-strict-sesf", is_flag=True, help="Treat SESF failures as warnings")
def validate(spec_file: str, json_output: bool, no_strict_sesf: bool) -> None:
    """Validate a REIXS spec file."""
    spec, _ = _parse_and_build(spec_file)
    report = run_validation(spec, strict_sesf=not no_strict_sesf)

    if json_output:
        click.echo(report.model_dump_json(indent=2))
    else:
        _print_report(report)

    sys.exit(1 if report.status == "fail" else 0)


@cli.command(name="compile")
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_dir", default="build", help="Output directory")
@click.option("--include-validation", is_flag=True, help="Include validation report")
@click.option("--no-strict-sesf", is_flag=True, help="Treat SESF failures as warnings")
def compile_cmd(
    spec_file: str, output_dir: str, include_validation: bool, no_strict_sesf: bool
) -> None:
    """Validate and compile a REIXS spec to runtime JSON."""
    spec, _ = _parse_and_build(spec_file)
    report = run_validation(spec, strict_sesf=not no_strict_sesf)

    if report.status == "fail":
        _print_report(report)
        console.print("\n[red]Compilation aborted — fix validation errors first.[/red]")
        sys.exit(1)

    try:
        out = Path(output_dir)
        artifacts = compile_reixs(spec, report, out, include_validation)
        console.print(f"[green]Compiled successfully to {output_dir}/[/green]")
        for name, path in artifacts.items():
            console.print(f"  {name}: {path}")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--template", type=str, help="Template name")
@click.option("-o", "--output", "output_file", default=None, help="Output file path")
@click.option("--list-templates", is_flag=True, help="List available templates")
def init(template: str | None, output_file: str | None, list_templates: bool) -> None:
    """Scaffold a new REIXS spec from a template."""
    if list_templates:
        console.print("[bold]Available templates:[/bold]")
        if TEMPLATES_DIR.exists():
            for f in sorted(TEMPLATES_DIR.glob("*.reixs.md")):
                name = f.stem.replace(".reixs", "").replace("_", "-")
                console.print(f"  {name}")
        else:
            console.print("  (no templates directory found)")
        return

    if not template:
        console.print("[red]Specify --template <name> or use --list-templates[/red]")
        sys.exit(1)

    template_name = template.replace("-", "_")
    template_file = TEMPLATES_DIR / f"{template_name}.reixs.md"
    if not template_file.exists():
        console.print(f"[red]Template not found: {template}[/red]")
        console.print(f"  Looked for: {template_file}")
        sys.exit(1)

    dest = output_file or f"{template_name}.reixs.md"
    shutil.copy2(template_file, dest)
    console.print(f"[green]Created {dest} from template '{template}'[/green]")
