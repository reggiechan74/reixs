# REIXS

**Real Estate Intelligence Execution Specification** — versioned, testable execution specs for real estate AI workflows.

## The Problem

When you ask an AI agent to do a real estate task — say, "extract lease terms from this PDF" — you need a way to specify **exactly** what the agent must do, what it must never do, and how to evaluate whether it did it right.

Without REIXS, these rules live in scattered prompts, ad-hoc instructions, or someone's head. REIXS puts them in a single Markdown file that is both **human-readable** (authors write it) and **machine-validatable** (the tool catches errors before an agent runs).

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

## How It Works

### The REIXS File

A `.reixs.md` file has 10 mandatory sections:

| Section | Purpose |
|---|---|
| **Meta** | Spec ID, version (semver), tier, author, date |
| **Objective** | One sentence: what this task accomplishes |
| **Domain Context** | Jurisdiction, currency, DDD reference |
| **Inputs** | What goes into the task |
| **OFD** | Objective Function Design — the hard rules |
| **Constraints** | Operational limits (time, format, connectivity) |
| **Output Contract** | What comes out, with field-level requirements |
| **Evaluation / EDD** | How to test the output |
| **Behavior Spec** | SESF v3 rules — machine-parseable behavior |
| **Validation Checklist** | Self-audit items for spec authors |

The two most important sections are **OFD** and **Behavior Spec**:

- **OFD** defines *what* the agent must optimize for — hard constraints that cause instant failure (e.g., "never fabricate a lease term"), priority ordering (factual accuracy > completeness > formatting), and what to do when uncertain.

- **Behavior Spec** defines *how* using [SESF v3](https://github.com/reggiechan74/cc-plugins/tree/main/structured-english) (Structured English Specification Format) — machine-parseable rules like:

```
RULE verbatim_extraction:
  WHEN a field value is found verbatim in the source document
  THEN status MUST be FACT
  AND provenance MUST include page number, clause reference, and verbatim quote
```

### The Pipeline

```
your_spec.reixs.md
       │
       ▼
   ┌────────┐    markdown-it-py parses the AST,
   │ PARSE  │    section aliases map headings to canonical names,
   │        │    key-value bullets → dict, SESF blocks extracted
   └────┬───┘
        │  dict[str, Any]  (raw section data)
        ▼
   ┌────────┐    section_model.py maps raw dicts into
   │  MAP   │    typed Pydantic models with coercion
   │        │    (date strings → date, tier → enum, etc.)
   └────┬───┘
        │  ReixsSpec  (fully typed Pydantic model)
        ▼
   ┌────────┐    5 passes, each returns list[Finding]:
   │VALIDATE│    1. Structural (semver? spec_id? objective?)
   │        │    2. OFD (5 mandatory + 5 tier-dependent fields)
   │        │    3. Domain (task type known? DDD ref valid?)
   │        │    4. SESF (vendored validator: real parse + check)
   │        │    5. Cross-field (provenance consistency, ADR for complex)
   └────┬───┘
        │  ValidationReport  (pass | warn | fail)
        ▼
   ┌────────┐    Only runs if status ≠ fail
   │COMPILE │    Emits reixs.runtime.json (for downstream agents)
   │        │         reixs.manifest.json (metadata envelope)
   └────────┘
```

Each validation pass is independent and testable in isolation. Pass 1 catches structural issues (missing sections) before Pass 3 tries to look up a DDD reference that might not even be parseable yet. Error messages are always actionable — fix structural issues first, then domain issues, etc.

### SESF Integration

The SESF block inside a REIXS spec is a complete, standalone SESF v3 document — with its own `Meta:` line, `BEHAVIOR` declarations, `RULE`/`ERROR`/`EXAMPLE` blocks, and `Constraints`.

REIXS doesn't just store this text — it **validates it** using a vendored copy of the SESF v3 validator (~1,480 lines of pure Python). The adapter writes the SESF text to a temp file, calls `parse_sesf()`, runs structural/error/example consistency checks, then maps each SESF `ValidationResult` (PASS/WARN/FAIL) to a REIXS `Finding` (info/warning/error).

When you run `reixs validate`, you get **two validation systems** working together — REIXS's 5-pass validator checking the spec structure, AND the SESF validator checking the behavioral rules inside it.

### The Tier System

Specs declare themselves as `micro`, `standard`, or `complex`:

| Tier | OFD Fields Required | ADR Required? | EDD Suite Required? |
|---|---|---|---|
| micro | 5 mandatory only | No | No |
| standard | 5 mandatory + 5 recommended | No | Yes |
| complex | All 10 | Yes | Yes |

This prevents over-engineering simple tasks while ensuring complex tasks have proper documentation.

### Compiler Output

When you run `reixs compile`, you get two JSON files:

- **`reixs.runtime.json`** — Everything a downstream AI agent needs: the objective, hard constraints, SESF rules, output contract, eval config, and DDD/ADR references. This is what gets fed into agent prompts.

- **`reixs.manifest.json`** — Metadata envelope with spec ID, version, source hash (SHA-256 of the original `.reixs.md`), compile timestamp, and artifact list. This enables reproducibility — you can always trace a runtime payload back to the exact spec that generated it.

The compiler refuses to emit runtime JSON if validation status is `fail`, enforcing the principle that hard constraints are checked before any downstream processing.

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
