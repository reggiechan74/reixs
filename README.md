# REIXS

**Real Estate Intelligence Execution Specification** — versioned, testable execution specs for real estate AI workflows.

## What It Does

REIXS lets you write a Markdown file that defines what an AI task must accomplish, then validates that spec and compiles it to machine-readable JSON. Catches errors in the spec before any AI agent runs.

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Scaffold a spec from a template
reixs init --template lease-abstraction-ontario -o my_spec.reixs.md

# Validate the spec
reixs validate my_spec.reixs.md

# Compile to runtime JSON
reixs compile my_spec.reixs.md -o build/
```

## Commands

| Command | Description |
|---|---|
| `reixs validate <spec.md>` | Parse and validate a REIXS spec (5-pass validation) |
| `reixs compile <spec.md> -o <dir>` | Validate and compile to runtime JSON |
| `reixs init --template <name>` | Scaffold a new spec from a template |

### Options

- `--json` — Output validation report as JSON
- `--no-strict-sesf` — Treat SESF validation failures as warnings
- `--include-validation` — Include validation report in compiled output
- `--list-templates` — Show available templates

## Validation Passes

1. **Structural** — Required sections, meta fields, version format
2. **OFD** — Objective Function Design completeness (5 mandatory + 5 tier-dependent)
3. **Domain** — Task type, jurisdiction, DDD reference, EDD suite
4. **SESF** — Validates embedded SESF v3 behavior rules
5. **Cross-field** — Consistency between sections (e.g., provenance in constraints ↔ output contract)

## Exit Codes

- `0` — Success
- `1` — Validation failure
- `2` — Parse error
- `3` — SESF validation failure
