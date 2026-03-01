---
title: REIXS Implementation Plan
date: 2026-03-01
keywords: [reixs, implementation, python, real-estate, specification]
lastUpdated: 2026-03-01
---

# REIXS Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a working REIXS prototype that can parse, validate, and compile real estate AI execution specs from Markdown to runtime JSON.

**Architecture:** Layered pipeline — markdown-it-py parses REIXS `.md` files into Pydantic models, a 5-pass validator checks structural/OFD/domain/SESF/cross-field rules, and a compiler emits `reixs.runtime.json` + `reixs.manifest.json`. SESF validation uses a vendored copy of the SESF v3 validator.

**Tech Stack:** Python 3.11+, Pydantic v2, Click, markdown-it-py, Rich, pytest

**Design doc:** `docs/plans/2026-03-01-reixs-design.md` (in reggie-life-plan repo)

**Repo:** Standalone `reggiechan74/reixs` (create fresh)

---

## Task 0: Create repo and bootstrap project

**Files:**
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `src/reixs/__init__.py`
- Create: `src/reixs/cli.py` (skeleton)
- Create: all `__init__.py` files for subpackages

**Step 1: Create the GitHub repo**

```bash
cd /workspaces
gh repo create reggiechan74/reixs --public --clone --description "Real Estate Intelligence Execution Specification — versioned, testable AI workflow specs"
cd reixs
```

**Step 2: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68.0", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "reixs"
version = "0.1.0"
description = "Real Estate Intelligence Execution Specification"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [{name = "Reggie Chan"}]

dependencies = [
    "pydantic>=2.0",
    "click>=8.0",
    "markdown-it-py>=3.0",
    "rich>=13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov",
]

[project.scripts]
reixs = "reixs.cli:cli"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Step 3: Create directory structure**

```bash
mkdir -p src/reixs/{parser,schema,validate,sesf,compile,registry,utils}
mkdir -p specs/{templates,examples,invalid,schemas}
mkdir -p tests/golden
mkdir -p docs/ADR
```

**Step 4: Create `__init__.py` files**

Create `src/reixs/__init__.py`:

```python
"""REIXS — Real Estate Intelligence Execution Specification."""

__version__ = "0.1.0"
```

Create empty `__init__.py` in every subpackage:

```bash
touch src/reixs/parser/__init__.py
touch src/reixs/schema/__init__.py
touch src/reixs/validate/__init__.py
touch src/reixs/sesf/__init__.py
touch src/reixs/compile/__init__.py
touch src/reixs/registry/__init__.py
touch src/reixs/utils/__init__.py
```

**Step 5: Create CLI skeleton**

Create `src/reixs/cli.py`:

```python
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
```

**Step 6: Install in dev mode and verify**

```bash
pip install -e ".[dev]"
reixs --version
reixs --help
```

Expected: version shows `0.1.0`, help shows `validate`, `compile`, `init` commands.

**Step 7: Commit**

```bash
git add -A
git commit -m "feat: bootstrap REIXS project with CLI skeleton"
```

---

## Task 1: Vendor SESF validator

**Files:**
- Create: `src/reixs/sesf/validate_sesf.py` (vendored copy)

**Step 1: Copy the vendored validator**

```bash
cp /home/codespace/.claude/plugins/marketplaces/cc-plugins/structured-english/skills/structured-english/scripts/validate_sesf.py src/reixs/sesf/validate_sesf.py
```

**Step 2: Verify it imports cleanly**

```bash
python -c "from reixs.sesf.validate_sesf import parse_sesf, check_structural_completeness, ValidationResult, SESFDocument; print('SESF validator imported OK')"
```

Expected: `SESF validator imported OK`

**Step 3: Commit**

```bash
git add src/reixs/sesf/validate_sesf.py
git commit -m "feat: vendor SESF v3 validator from structured-english plugin"
```

---

## Task 2: Define enums and data models

**Files:**
- Create: `src/reixs/schema/enums.py`
- Create: `src/reixs/schema/reixs_models.py`
- Create: `src/reixs/schema/runtime_payload.py`
- Create: `src/reixs/validate/report.py`
- Test: `tests/test_models.py`

**Step 1: Write tests for models**

Create `tests/test_models.py`:

```python
"""Tests for REIXS data models."""

import pytest
from datetime import date
from pydantic import ValidationError

from reixs.schema.enums import Tier, FieldStatus
from reixs.schema.reixs_models import (
    MetaSection,
    OFDSection,
    DomainContextSection,
    InputsSection,
    ConstraintsSection,
    OutputContractSection,
    EvaluationSection,
    BehaviorSpecSection,
    ReixsSpec,
)
from reixs.schema.runtime_payload import RuntimePayload, Manifest
from reixs.validate.report import Finding, ValidationReport


class TestEnums:
    def test_tier_values(self):
        assert Tier.MICRO == "micro"
        assert Tier.STANDARD == "standard"
        assert Tier.COMPLEX == "complex"

    def test_field_status_values(self):
        assert FieldStatus.FACT == "fact"
        assert FieldStatus.INFERENCE == "inference"
        assert FieldStatus.MISSING == "missing"
        assert FieldStatus.CONFLICT == "conflict"


class TestMetaSection:
    def test_valid_meta(self):
        meta = MetaSection(
            spec_id="REIXS-LA-ON-001",
            version="1.0.0",
            task_type="Lease Abstraction",
            tier=Tier.STANDARD,
            author="Reggie Chan",
            date=date(2026, 3, 1),
        )
        assert meta.spec_id == "REIXS-LA-ON-001"
        assert meta.tier == Tier.STANDARD

    def test_invalid_tier_rejected(self):
        with pytest.raises(ValidationError):
            MetaSection(
                spec_id="X",
                version="1.0.0",
                task_type="X",
                tier="invalid",
                author="X",
                date=date(2026, 1, 1),
            )


class TestOFDSection:
    def test_required_fields_only(self):
        ofd = OFDSection(
            primary_objective="Extract lease terms",
            hard_constraints=["No fabrication"],
            autofail_conditions=["Fabricated term"],
            optimization_priority_order=["Factual correctness"],
            uncertainty_policy="Mark as INFERENCE",
        )
        assert ofd.secondary_objectives is None
        assert ofd.scoring_model is None

    def test_all_fields(self):
        ofd = OFDSection(
            primary_objective="Extract lease terms",
            hard_constraints=["No fabrication"],
            autofail_conditions=["Fabricated term"],
            optimization_priority_order=["Factual correctness"],
            uncertainty_policy="Mark as INFERENCE",
            secondary_objectives=["Find renewals"],
            tradeoff_policies=["Prefer MISSING over GUESS"],
            scoring_model="Weighted F1",
            escalation_triggers=["Low confidence"],
            error_severity_model={"critical": ["fabricated term"]},
        )
        assert ofd.secondary_objectives == ["Find renewals"]

    def test_empty_hard_constraints_accepted_by_pydantic(self):
        # Pydantic accepts empty list; validator Pass 2 catches this
        ofd = OFDSection(
            primary_objective="X",
            hard_constraints=[],
            autofail_conditions=["X"],
            optimization_priority_order=["X"],
            uncertainty_policy="X",
        )
        assert ofd.hard_constraints == []


class TestFinding:
    def test_finding_creation(self):
        f = Finding(
            pass_number=1,
            severity="error",
            section="meta",
            field="version",
            message="Version format invalid",
            suggestion="Use semver format: X.Y.Z",
        )
        assert f.severity == "error"
        assert f.pass_number == 1

    def test_finding_minimal(self):
        f = Finding(
            pass_number=2,
            severity="warning",
            section=None,
            field=None,
            message="OFD scoring model missing",
            suggestion=None,
        )
        assert f.section is None


class TestValidationReport:
    def test_status_derived_from_findings(self):
        report = ValidationReport(
            spec_id="TEST-001",
            spec_version="1.0.0",
            findings=[
                Finding(pass_number=1, severity="info", section="meta",
                        field=None, message="OK", suggestion=None),
            ],
            pass_summaries={},
            sesf_findings=[],
        )
        assert report.status == "pass"

    def test_status_fail_on_error(self):
        report = ValidationReport(
            spec_id="TEST-001",
            spec_version="1.0.0",
            findings=[
                Finding(pass_number=1, severity="error", section="meta",
                        field=None, message="Missing", suggestion=None),
            ],
            pass_summaries={},
            sesf_findings=[],
        )
        assert report.status == "fail"

    def test_status_warn_on_warnings_only(self):
        report = ValidationReport(
            spec_id="TEST-001",
            spec_version="1.0.0",
            findings=[
                Finding(pass_number=1, severity="warning", section="ofd",
                        field=None, message="Missing scoring", suggestion=None),
            ],
            pass_summaries={},
            sesf_findings=[],
        )
        assert report.status == "warn"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_models.py -v
```

Expected: ImportError — modules don't exist yet.

**Step 3: Implement enums**

Create `src/reixs/schema/enums.py`:

```python
"""REIXS enumerations."""

from enum import Enum


class Tier(str, Enum):
    MICRO = "micro"
    STANDARD = "standard"
    COMPLEX = "complex"


class FieldStatus(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    MISSING = "missing"
    CONFLICT = "conflict"
```

**Step 4: Implement Pydantic models**

Create `src/reixs/schema/reixs_models.py`:

```python
"""REIXS specification data models."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel

from reixs.schema.enums import Tier


class MetaSection(BaseModel):
    spec_id: str
    version: str
    task_type: str
    tier: Tier
    author: str
    date: date


class DomainContextSection(BaseModel):
    jurisdiction: str
    currency: str | None = None
    area_unit: str | None = None
    ddd_reference: str | None = None
    adr_references: list[str] | None = None
    extra: dict[str, str] = {}


class InputsSection(BaseModel):
    items: list[dict[str, str]]


class OFDSection(BaseModel):
    primary_objective: str
    hard_constraints: list[str]
    autofail_conditions: list[str]
    optimization_priority_order: list[str]
    uncertainty_policy: str
    secondary_objectives: list[str] | None = None
    tradeoff_policies: list[str] | None = None
    scoring_model: str | dict | None = None
    escalation_triggers: list[str] | None = None
    error_severity_model: dict[str, list[str]] | None = None


class ConstraintsSection(BaseModel):
    items: list[str]


class OutputContractSection(BaseModel):
    description: str
    fields: list[dict[str, str]] = []


class EvaluationSection(BaseModel):
    edd_suite_id: str | None = None
    min_pass_rate: str | None = None
    zero_tolerance: str | None = None
    regression_cases: list[str] = []
    raw_text: str = ""


class BehaviorSpecSection(BaseModel):
    raw_sesf: str
    sesf_blocks: list[str] = []


class ReixsSpec(BaseModel):
    meta: MetaSection
    objective: str
    domain_context: DomainContextSection
    inputs: InputsSection
    ofd: OFDSection
    constraints: ConstraintsSection
    output_contract: OutputContractSection
    evaluation: EvaluationSection
    behavior_spec: BehaviorSpecSection
    validation_checklist: list[str]
    source_hash: str
```

**Step 5: Implement runtime payload models**

Create `src/reixs/schema/runtime_payload.py`:

```python
"""REIXS compiler output models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class RuntimePayload(BaseModel):
    spec_metadata: dict[str, Any]
    task_context: dict[str, Any]
    ofd: dict[str, Any]
    behavior_rules: dict[str, Any]
    output_contract: dict[str, Any]
    eval_config: dict[str, Any]
    references: dict[str, Any]
    validation_status: str


class Manifest(BaseModel):
    spec_id: str
    version: str
    source_hash: str
    compile_timestamp: str
    artifacts: list[str]
```

**Step 6: Implement Finding and ValidationReport**

Create `src/reixs/validate/report.py`:

```python
"""Validation report models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, computed_field


class Finding(BaseModel):
    pass_number: int
    severity: Literal["error", "warning", "info"]
    section: str | None = None
    field: str | None = None
    message: str
    suggestion: str | None = None


class PassSummary(BaseModel):
    pass_number: int
    name: str
    errors: int = 0
    warnings: int = 0
    infos: int = 0


class ValidationReport(BaseModel):
    spec_id: str
    spec_version: str
    findings: list[Finding]
    pass_summaries: dict[int, PassSummary] = {}
    sesf_findings: list[dict[str, Any]] = []

    @computed_field
    @property
    def status(self) -> str:
        if any(f.severity == "error" for f in self.findings):
            return "fail"
        if any(f.severity == "warning" for f in self.findings):
            return "warn"
        return "pass"

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]
```

**Step 7: Run tests**

```bash
pytest tests/test_models.py -v
```

Expected: all tests pass.

**Step 8: Commit**

```bash
git add src/reixs/schema/ src/reixs/validate/report.py tests/test_models.py
git commit -m "feat: add Pydantic data models and validation report types"
```

---

## Task 3: Write the lease abstraction template (SESF v3 format)

**Files:**
- Create: `specs/templates/lease_abstraction_ontario.reixs.md`
- Create: `specs/invalid/missing_ofd.reixs.md`
- Create: `specs/invalid/missing_sesf.reixs.md`
- Create: `specs/invalid/missing_ddd_ref.reixs.md`
- Create: `specs/invalid/complex_no_adr.reixs.md`

This is the "Step 0" from the design plan — write the spec by hand FIRST.

**Step 1: Create the valid template**

Create `specs/templates/lease_abstraction_ontario.reixs.md`. This is the canonical example. The SESF block uses full SESF v3 format with a BEHAVIOR declaration:

```markdown
# REIXS: Lease Abstraction — Ontario Commercial

## Meta

- Spec ID: REIXS-LA-ON-001
- Version: 1.0.0
- Task Type: Lease Abstraction
- Tier: standard
- Author: Reggie Chan
- Date: 2026-03-01

## Objective

Extract structured lease terms from a commercial lease document (Ontario jurisdiction)
and produce a normalized term sheet with field-level provenance.

## Domain Context

- Jurisdiction: Ontario, Canada
- Currency: CAD
- Area Unit: sq ft (default), sq m (accepted)
- DDD Reference: re-ddd:lease_core_terms_ontario@0.1.0
- ADR References: ADR-001, ADR-003

## Inputs

- Source document: PDF (scanned or native)
- Document type: Commercial lease agreement
- Expected length: 5-200 pages

## Objective Function Design (OFD)

### Primary Objective
Extract all lease terms defined in DDD with factual accuracy >= 98%.

### Hard Constraints
- NEVER fabricate a term not present in the source document
- NEVER silently resolve conflicting dates — flag as CONFLICT
- ALL extracted values MUST carry provenance (page, clause, verbatim quote)
- Currency MUST be CAD unless explicitly stated otherwise in source

### AutoFail Conditions
- Any fabricated term (not traceable to source text)
- Missing commencement_date without MISSING status flag
- Provenance absent on any FACT-status field

### Optimization Priority Order
1. Factual correctness
2. Completeness of extraction
3. Provenance quality
4. Formatting consistency

### Uncertainty Policy
When a term is ambiguous or requires interpretation, mark as INFERENCE
with confidence score and reasoning. Never present inferences as facts.

### Secondary Objectives
- Identify renewal options and escalation clauses
- Flag unusual or non-standard provisions

### Tradeoff Policies
- Prefer MISSING over GUESS — an empty field with MISSING status is better than a plausible but unverified value
- Prefer verbatim extraction over normalized form when normalization is lossy

### Scoring Model
- Weighted F1: precision weight 0.7, recall weight 0.3
- Critical fields (commencement, expiry, rent): 2x weight

### Escalation Triggers
- Confidence < 0.6 on any critical field
- More than 3 fields marked CONFLICT in single document
- Document language is not English

### Error Severity Model
- critical: fabricated term, wrong currency, wrong dates
- high: missing critical field without flag, provenance gap
- medium: formatting inconsistency, missing non-critical field
- low: minor normalization differences, whitespace issues

## Constraints

- Processing time: < 120 seconds per document
- Output format: JSON conforming to lease_abstraction_output_v1.json schema
- No external API calls during extraction (offline-capable)

## Output Contract

Each extracted field MUST include:
- `value`: the extracted or derived value
- `status`: FACT | INFERENCE | MISSING | CONFLICT
- `provenance`: { page, clause, verbatim_quote } (required for FACT status)
- `confidence`: 0.0-1.0 (required for INFERENCE status)
- `reasoning`: string (required for INFERENCE and CONFLICT status)

## Evaluation / EDD

- EDD Suite ID: edd:lease_abstraction_core_v1
- Minimum pass rate: 95%
- Zero tolerance: critical-severity errors
- Regression cases: basic_valid_case, conflicting_dates_case, missing_commencement_case

## Behavior Spec (SESF)

```sesf
Lease Term Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

Purpose
Define extraction, conflict detection, and provenance rules for commercial lease term extraction.

BEHAVIOR extract_lease_terms: Extract and classify lease terms from source document

  RULE verbatim_extraction:
    WHEN a field value is found verbatim in the source document
    THEN status MUST be FACT
    AND provenance MUST include page number, clause reference, and verbatim quote

  RULE inference_handling:
    WHEN a field value requires interpretation or calculation
    THEN status MUST be INFERENCE
    AND confidence score MUST be provided (0.0 to 1.0)
    AND reasoning MUST explain how the value was derived

  RULE missing_field:
    WHEN a DDD-defined field is not found in the source document
    THEN status MUST be MISSING
    AND the value field MUST be null
    AND the agent MUST NOT fabricate a value

  RULE conflict_detection:
    WHEN multiple conflicting values are found for the same field
    THEN status MUST be CONFLICT
    AND all conflicting values MUST be listed with individual provenance
    AND reasoning MUST explain the nature of the conflict

  RULE currency_default:
    WHEN currency is not explicitly stated in the source document
    THEN assume CAD for Ontario jurisdiction leases

  ERROR fabricated_value:
    WHEN an extracted value cannot be traced to source text
    SEVERITY critical
    ACTION reject the extraction and flag for human review
    MESSAGE "Extracted value has no source provenance — possible fabrication"

  ERROR missing_provenance:
    WHEN a FACT-status field lacks provenance metadata
    SEVERITY critical
    ACTION fail validation for this field
    MESSAGE "FACT-status field requires provenance (page, clause, verbatim quote)"

  EXAMPLE standard_extraction:
    INPUT: lease document with commencement date "January 1, 2026" on page 3, clause 2.1
    EXPECTED: { "value": "2026-01-01", "status": "FACT", "provenance": { "page": 3, "clause": "2.1", "verbatim_quote": "January 1, 2026" } }
    NOTES: Clear verbatim extraction with full provenance

  EXAMPLE conflicting_dates:
    INPUT: lease with "commencing January 1, 2026" in clause 2.1 and "effective March 1, 2026" in clause 5.3
    EXPECTED: { "status": "CONFLICT", "values": ["2026-01-01", "2026-03-01"], "reasoning": "Conflicting commencement dates in clauses 2.1 and 5.3" }
    NOTES: Conflicting dates MUST be flagged, never silently resolved

  EXAMPLE missing_term:
    INPUT: lease document with no operating cost provisions
    EXPECTED: { "value": null, "status": "MISSING" }
    NOTES: Missing field with MISSING status — no fabrication

Constraints
* Extraction MUST process all fields defined in DDD reference before completion
```

## Validation Checklist

- [ ] All DDD-defined fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] AutoFail conditions have corresponding test fixtures
- [ ] SESF rules cover extraction, conflict, and missing-value scenarios
- [ ] Ontario jurisdiction metadata (currency, units) declared
- [ ] EDD suite ID references at least 3 test cases
```

**Step 2: Create invalid test specs**

Create `specs/invalid/missing_ofd.reixs.md` — same as template but with the entire OFD section removed.

Create `specs/invalid/missing_sesf.reixs.md` — same as template but with the SESF code block removed (section header remains, no fenced block).

Create `specs/invalid/missing_ddd_ref.reixs.md` — same as template but `DDD Reference` line removed from Domain Context.

Create `specs/invalid/complex_no_adr.reixs.md` — same as template but Tier changed to `complex` and ADR References line removed.

Each should be a minimal edit from the valid template — change only the thing being tested.

**Step 3: Commit**

```bash
git add specs/
git commit -m "feat: add lease abstraction template and invalid test specs"
```

---

## Task 4: Implement Markdown parser

**Files:**
- Create: `src/reixs/parser/markdown_parser.py`
- Create: `src/reixs/parser/sesf_extractor.py`
- Create: `src/reixs/utils/hashing.py`
- Test: `tests/test_parser.py`

**Step 1: Write parser tests**

Create `tests/test_parser.py`:

```python
"""Tests for REIXS Markdown parser."""

import pytest
from pathlib import Path

from reixs.parser.markdown_parser import parse_reixs_markdown, SECTION_ALIASES
from reixs.parser.sesf_extractor import extract_sesf_blocks
from reixs.schema.enums import Tier


VALID_SPEC = Path("specs/templates/lease_abstraction_ontario.reixs.md")


class TestSectionDetection:
    def test_all_required_sections_found(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        required = set(SECTION_ALIASES.keys())
        assert required.issubset(set(sections.keys())), (
            f"Missing sections: {required - set(sections.keys())}"
        )

    def test_meta_parsed_as_dict(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        meta = sections["meta"]
        assert meta["spec_id"] == "REIXS-LA-ON-001"
        assert meta["tier"] == "standard"
        assert meta["version"] == "1.0.0"

    def test_ofd_subheadings_parsed(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        ofd = sections["ofd"]
        assert "primary_objective" in ofd
        assert "hard_constraints" in ofd
        assert isinstance(ofd["hard_constraints"], list)
        assert len(ofd["hard_constraints"]) >= 3

    def test_alias_resolution(self):
        """'Objective Function Design (OFD)' should resolve to 'ofd'."""
        sections = parse_reixs_markdown(VALID_SPEC)
        assert "ofd" in sections

    def test_evaluation_alias(self):
        """'Evaluation / EDD' should resolve to 'evaluation'."""
        sections = parse_reixs_markdown(VALID_SPEC)
        assert "evaluation" in sections

    def test_behavior_spec_alias(self):
        """'Behavior Spec (SESF)' should resolve to 'behavior_spec'."""
        sections = parse_reixs_markdown(VALID_SPEC)
        assert "behavior_spec" in sections


class TestSESFExtraction:
    def test_sesf_block_extracted(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        blocks = extract_sesf_blocks(sections)
        assert len(blocks) >= 1
        assert "BEHAVIOR extract_lease_terms" in blocks[0]

    def test_sesf_block_contains_rules(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        blocks = extract_sesf_blocks(sections)
        assert "RULE verbatim_extraction" in blocks[0]
        assert "RULE conflict_detection" in blocks[0]

    def test_no_sesf_block_returns_empty(self):
        missing_sesf = Path("specs/invalid/missing_sesf.reixs.md")
        if missing_sesf.exists():
            sections = parse_reixs_markdown(missing_sesf)
            blocks = extract_sesf_blocks(sections)
            assert len(blocks) == 0


class TestKeyValueParsing:
    def test_domain_context_key_values(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        dc = sections["domain_context"]
        assert dc["jurisdiction"] == "Ontario, Canada"
        assert dc["currency"] == "CAD"
        assert "re-ddd:" in dc["ddd_reference"]

    def test_evaluation_key_values(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        ev = sections["evaluation"]
        assert "edd_suite_id" in ev or "edd suite id" in str(ev).lower()


class TestValidationChecklist:
    def test_checklist_items_extracted(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        checklist = sections["validation_checklist"]
        assert isinstance(checklist, list)
        assert len(checklist) >= 4
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_parser.py -v
```

Expected: ImportError.

**Step 3: Implement hashing utility**

Create `src/reixs/utils/hashing.py`:

```python
"""Hashing utilities for source file integrity."""

import hashlib
from pathlib import Path


def compute_source_hash(filepath: Path) -> str:
    """Compute SHA-256 hash of a file's contents."""
    content = filepath.read_bytes()
    return hashlib.sha256(content).hexdigest()
```

**Step 4: Implement SESF extractor**

Create `src/reixs/parser/sesf_extractor.py`:

```python
"""Extract SESF fenced code blocks from parsed REIXS sections."""

from __future__ import annotations


def extract_sesf_blocks(sections: dict) -> list[str]:
    """Extract raw text from ```sesf fenced code blocks.

    Looks in the 'behavior_spec' section for code blocks tagged 'sesf'.
    Returns a list of raw SESF text strings.
    """
    behavior = sections.get("behavior_spec", {})
    if isinstance(behavior, dict):
        blocks = behavior.get("_code_blocks", [])
        return [b["content"] for b in blocks if b.get("lang") == "sesf"]
    return []
```

**Step 5: Implement Markdown parser**

Create `src/reixs/parser/markdown_parser.py`:

```python
"""REIXS Markdown parser — converts .reixs.md files into section dictionaries.

Uses markdown-it-py to parse the AST, then walks it to extract sections,
key-value pairs, lists, sub-headings, and fenced code blocks.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt


# ---------------------------------------------------------------------------
# Section alias map
# ---------------------------------------------------------------------------

SECTION_ALIASES: dict[str, list[str]] = {
    "meta": ["meta"],
    "objective": ["objective"],
    "domain_context": ["domain context", "domain"],
    "inputs": ["inputs", "input"],
    "ofd": [
        "objective function design",
        "objective function design (ofd)",
        "ofd",
    ],
    "constraints": ["constraints"],
    "output_contract": ["output contract"],
    "evaluation": ["evaluation", "evaluation / edd", "eval", "edd"],
    "behavior_spec": [
        "behavior spec",
        "behavior spec (sesf)",
        "sesf",
        "behavior",
    ],
    "validation_checklist": ["validation checklist", "checklist"],
}

_ALIAS_LOOKUP: dict[str, str] = {}
for canonical, aliases in SECTION_ALIASES.items():
    for alias in aliases:
        _ALIAS_LOOKUP[alias.lower()] = canonical


def _normalize_heading(text: str) -> str | None:
    """Map a heading string to its canonical section name, or None."""
    cleaned = text.strip().lower()
    # Try exact match first
    if cleaned in _ALIAS_LOOKUP:
        return _ALIAS_LOOKUP[cleaned]
    # Try stripping markdown formatting artifacts
    cleaned = re.sub(r"[#*_`]", "", cleaned).strip()
    if cleaned in _ALIAS_LOOKUP:
        return _ALIAS_LOOKUP[cleaned]
    return None


def _normalize_key(key: str) -> str:
    """Normalize a key-value key to snake_case."""
    return re.sub(r"[\s\-]+", "_", key.strip().lower())


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_reixs_markdown(filepath: Path) -> dict[str, Any]:
    """Parse a REIXS markdown file into a section dictionary.

    Returns a dict keyed by canonical section names. Each value is either:
    - dict: for sections with key-value pairs or sub-headings
    - list[str]: for sections with bullet lists
    - str: for sections with free text
    """
    md = MarkdownIt()
    content = filepath.read_text(encoding="utf-8")
    tokens = md.parse(content)

    sections: dict[str, Any] = {}
    current_section: str | None = None
    current_subsection: str | None = None
    current_data: dict[str, Any] = {}

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # --- Heading detection ---
        if token.type == "heading_open":
            level = int(token.tag[1])  # h1=1, h2=2, h3=3
            # Next token is the inline content
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                heading_text = tokens[i + 1].content

                if level == 2:
                    # Flush previous section
                    if current_section is not None:
                        sections[current_section] = _finalize_section(current_data)
                    canonical = _normalize_heading(heading_text)
                    if canonical:
                        current_section = canonical
                        current_data = {}
                        current_subsection = None
                    else:
                        current_section = None
                        current_data = {}

                elif level == 3 and current_section is not None:
                    # Sub-heading within a section
                    current_subsection = _normalize_key(heading_text)

            i += 3  # skip heading_open, inline, heading_close
            continue

        # --- Bullet list ---
        if token.type == "bullet_list_open" and current_section is not None:
            items = _extract_list_items(tokens, i)
            target_key = current_subsection or "_items"

            if current_section == "meta":
                # Parse key-value pairs from meta bullets
                for item in items:
                    k, v = _parse_kv(item)
                    if k:
                        current_data[k] = v
            elif current_section == "validation_checklist":
                # Strip checkbox markers
                cleaned = [re.sub(r"^\[[ x]\]\s*", "", item) for item in items]
                current_data.setdefault("_items", []).extend(cleaned)
            elif current_subsection:
                current_data[current_subsection] = items
            else:
                # Try to parse as key-value pairs
                parsed_any_kv = False
                for item in items:
                    k, v = _parse_kv(item)
                    if k:
                        current_data[k] = v
                        parsed_any_kv = True
                if not parsed_any_kv:
                    current_data.setdefault("_items", []).extend(items)

            # Skip past the list
            depth = 1
            i += 1
            while i < len(tokens) and depth > 0:
                if tokens[i].type == "bullet_list_open":
                    depth += 1
                elif tokens[i].type == "bullet_list_close":
                    depth -= 1
                i += 1
            continue

        # --- Ordered list ---
        if token.type == "ordered_list_open" and current_section is not None:
            items = _extract_ordered_items(tokens, i)
            target_key = current_subsection or "_items"
            if current_subsection:
                current_data[current_subsection] = items
            else:
                current_data.setdefault("_items", []).extend(items)
            depth = 1
            i += 1
            while i < len(tokens) and depth > 0:
                if tokens[i].type == "ordered_list_open":
                    depth += 1
                elif tokens[i].type == "ordered_list_close":
                    depth -= 1
                i += 1
            continue

        # --- Fenced code block ---
        if token.type == "fence" and current_section is not None:
            lang = (token.info or "").strip()
            current_data.setdefault("_code_blocks", []).append({
                "lang": lang,
                "content": token.content,
            })
            i += 1
            continue

        # --- Paragraph (free text) ---
        if token.type == "paragraph_open" and current_section is not None:
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                text = tokens[i + 1].content
                if current_subsection:
                    existing = current_data.get(current_subsection, "")
                    if isinstance(existing, str) and existing:
                        current_data[current_subsection] = existing + "\n" + text
                    else:
                        current_data[current_subsection] = text
                else:
                    existing = current_data.get("_text", "")
                    if existing:
                        current_data["_text"] = existing + "\n" + text
                    else:
                        current_data["_text"] = text
            i += 3  # paragraph_open, inline, paragraph_close
            continue

        i += 1

    # Flush last section
    if current_section is not None:
        sections[current_section] = _finalize_section(current_data)

    return sections


def _finalize_section(data: dict[str, Any]) -> Any:
    """Convert raw section data to final format."""
    # If section only has _items, return the list directly
    if list(data.keys()) == ["_items"]:
        return data["_items"]
    # If section only has _text, return the string directly
    if list(data.keys()) == ["_text"]:
        return data["_text"]
    return data


def _extract_list_items(tokens: list, start: int) -> list[str]:
    """Extract text content from a bullet_list starting at `start`."""
    items = []
    depth = 0
    i = start
    while i < len(tokens):
        t = tokens[i]
        if t.type == "bullet_list_open":
            depth += 1
        elif t.type == "bullet_list_close":
            depth -= 1
            if depth == 0:
                break
        elif t.type == "inline" and depth == 1:
            items.append(t.content)
        i += 1
    return items


def _extract_ordered_items(tokens: list, start: int) -> list[str]:
    """Extract text content from an ordered_list starting at `start`."""
    items = []
    depth = 0
    i = start
    while i < len(tokens):
        t = tokens[i]
        if t.type == "ordered_list_open":
            depth += 1
        elif t.type == "ordered_list_close":
            depth -= 1
            if depth == 0:
                break
        elif t.type == "inline" and depth == 1:
            # Strip leading number+dot if present
            text = re.sub(r"^\d+\.\s*", "", t.content)
            items.append(text)
        i += 1
    return items


def _parse_kv(text: str) -> tuple[str | None, str]:
    """Try to parse 'Key: Value' from a bullet item.

    Returns (normalized_key, value) or (None, original_text).
    """
    match = re.match(r"^([^:]+):\s*(.+)$", text, re.DOTALL)
    if match:
        key = _normalize_key(match.group(1))
        value = match.group(2).strip()
        return key, value
    return None, text
```

**Step 6: Run parser tests**

```bash
pytest tests/test_parser.py -v
```

Expected: most tests pass. Debug any failures against the actual template content. The parser may need iteration — this is expected.

**Step 7: Commit**

```bash
git add src/reixs/parser/ src/reixs/utils/ tests/test_parser.py
git commit -m "feat: implement REIXS Markdown parser with SESF extraction"
```

---

## Task 5: Implement section-to-model mapper

**Files:**
- Create: `src/reixs/parser/section_model.py`
- Test: `tests/test_section_model.py`

**Step 1: Write tests**

Create `tests/test_section_model.py`:

```python
"""Tests for section dict → ReixsSpec model mapping."""

import pytest
from pathlib import Path

from reixs.parser.markdown_parser import parse_reixs_markdown
from reixs.parser.section_model import build_reixs_spec
from reixs.schema.enums import Tier


VALID_SPEC = Path("specs/templates/lease_abstraction_ontario.reixs.md")


class TestBuildReixsSpec:
    def test_valid_spec_parses_to_model(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        assert spec.meta.spec_id == "REIXS-LA-ON-001"
        assert spec.meta.tier == Tier.STANDARD
        assert spec.meta.version == "1.0.0"

    def test_ofd_required_fields_present(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        assert len(spec.ofd.hard_constraints) >= 3
        assert len(spec.ofd.autofail_conditions) >= 2
        assert spec.ofd.primary_objective != ""

    def test_domain_context_fields(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        assert spec.domain_context.jurisdiction == "Ontario, Canada"
        assert spec.domain_context.currency == "CAD"
        assert spec.domain_context.ddd_reference is not None

    def test_behavior_spec_contains_sesf(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        assert "BEHAVIOR" in spec.behavior_spec.raw_sesf
        assert len(spec.behavior_spec.sesf_blocks) >= 1

    def test_source_hash_populated(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        assert len(spec.source_hash) == 64  # SHA-256 hex

    def test_validation_checklist_parsed(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        assert len(spec.validation_checklist) >= 4
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_section_model.py -v
```

**Step 3: Implement section_model.py**

Create `src/reixs/parser/section_model.py`:

```python
"""Map parsed section dictionaries into ReixsSpec Pydantic models."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from reixs.parser.sesf_extractor import extract_sesf_blocks
from reixs.schema.enums import Tier
from reixs.schema.reixs_models import (
    BehaviorSpecSection,
    ConstraintsSection,
    DomainContextSection,
    EvaluationSection,
    InputsSection,
    MetaSection,
    OFDSection,
    OutputContractSection,
    ReixsSpec,
)
from reixs.utils.hashing import compute_source_hash


def build_reixs_spec(sections: dict[str, Any], filepath: Path) -> ReixsSpec:
    """Build a ReixsSpec from parsed section data."""
    meta = _build_meta(sections.get("meta", {}))
    ofd = _build_ofd(sections.get("ofd", {}))
    domain_context = _build_domain_context(sections.get("domain_context", {}))
    inputs = _build_inputs(sections.get("inputs", {}))
    constraints = _build_constraints(sections.get("constraints", []))
    output_contract = _build_output_contract(sections.get("output_contract", {}))
    evaluation = _build_evaluation(sections.get("evaluation", {}))
    behavior_spec = _build_behavior_spec(sections)
    checklist = _build_checklist(sections.get("validation_checklist", []))
    objective = _extract_text(sections.get("objective", ""))

    return ReixsSpec(
        meta=meta,
        objective=objective,
        domain_context=domain_context,
        inputs=inputs,
        ofd=ofd,
        constraints=constraints,
        output_contract=output_contract,
        evaluation=evaluation,
        behavior_spec=behavior_spec,
        validation_checklist=checklist,
        source_hash=compute_source_hash(filepath),
    )


def _extract_text(section: Any) -> str:
    """Extract plain text from a section value."""
    if isinstance(section, str):
        return section
    if isinstance(section, dict):
        return section.get("_text", "")
    return ""


def _build_meta(data: dict) -> MetaSection:
    """Build MetaSection from parsed meta dict."""
    date_str = data.get("date", "2000-01-01")
    try:
        parsed_date = date.fromisoformat(date_str)
    except (ValueError, TypeError):
        parsed_date = date(2000, 1, 1)

    tier_str = data.get("tier", "standard").lower().strip()
    try:
        tier = Tier(tier_str)
    except ValueError:
        tier = Tier.STANDARD

    return MetaSection(
        spec_id=data.get("spec_id", ""),
        version=data.get("version", "0.0.0"),
        task_type=data.get("task_type", ""),
        tier=tier,
        author=data.get("author", ""),
        date=parsed_date,
    )


def _build_ofd(data: dict) -> OFDSection:
    """Build OFDSection from parsed OFD dict."""
    return OFDSection(
        primary_objective=_extract_text(data.get("primary_objective", "")),
        hard_constraints=_ensure_list(data.get("hard_constraints", [])),
        autofail_conditions=_ensure_list(data.get("autofail_conditions", [])),
        optimization_priority_order=_ensure_list(
            data.get("optimization_priority_order", [])
        ),
        uncertainty_policy=_extract_text(data.get("uncertainty_policy", "")),
        secondary_objectives=_ensure_list_or_none(
            data.get("secondary_objectives")
        ),
        tradeoff_policies=_ensure_list_or_none(data.get("tradeoff_policies")),
        scoring_model=_extract_text(data.get("scoring_model", "")) or None,
        escalation_triggers=_ensure_list_or_none(
            data.get("escalation_triggers")
        ),
        error_severity_model=_parse_severity_model(
            data.get("error_severity_model")
        ),
    )


def _build_domain_context(data: dict) -> DomainContextSection:
    """Build DomainContextSection."""
    return DomainContextSection(
        jurisdiction=data.get("jurisdiction", ""),
        currency=data.get("currency"),
        area_unit=data.get("area_unit"),
        ddd_reference=data.get("ddd_reference"),
        adr_references=_parse_csv(data.get("adr_references")),
    )


def _build_inputs(data: dict) -> InputsSection:
    """Build InputsSection."""
    items = []
    if isinstance(data, list):
        for item in data:
            k, v = item if isinstance(item, tuple) else (None, item)
            if k:
                items.append({"key": k, "value": v})
            else:
                parts = str(item).split(":", 1)
                if len(parts) == 2:
                    items.append({"key": parts[0].strip(), "value": parts[1].strip()})
                else:
                    items.append({"key": item, "value": ""})
    elif isinstance(data, dict):
        for k, v in data.items():
            if not k.startswith("_"):
                items.append({"key": k, "value": str(v)})
        # Also check _items
        for item in data.get("_items", []):
            parts = str(item).split(":", 1)
            if len(parts) == 2:
                items.append({"key": parts[0].strip(), "value": parts[1].strip()})
    return InputsSection(items=items)


def _build_constraints(data: Any) -> ConstraintsSection:
    """Build ConstraintsSection."""
    if isinstance(data, list):
        return ConstraintsSection(items=data)
    if isinstance(data, dict):
        return ConstraintsSection(items=data.get("_items", []))
    return ConstraintsSection(items=[])


def _build_output_contract(data: dict) -> OutputContractSection:
    """Build OutputContractSection."""
    text = _extract_text(data)
    fields = []
    items = []
    if isinstance(data, dict):
        items = data.get("_items", [])
    for item in items:
        parts = str(item).split(":", 1)
        if len(parts) == 2:
            fields.append({"name": parts[0].strip().strip("`"), "description": parts[1].strip()})
    return OutputContractSection(description=text, fields=fields)


def _build_evaluation(data: dict) -> EvaluationSection:
    """Build EvaluationSection."""
    if isinstance(data, str):
        return EvaluationSection(raw_text=data)

    raw_parts = []
    for k, v in data.items():
        if not k.startswith("_"):
            raw_parts.append(f"{k}: {v}")

    regression = data.get("regression_cases", "")
    if isinstance(regression, str):
        regression = [r.strip() for r in regression.split(",") if r.strip()]

    return EvaluationSection(
        edd_suite_id=data.get("edd_suite_id"),
        min_pass_rate=data.get("minimum_pass_rate") or data.get("min_pass_rate"),
        zero_tolerance=data.get("zero_tolerance"),
        regression_cases=regression,
        raw_text="\n".join(raw_parts),
    )


def _build_behavior_spec(sections: dict) -> BehaviorSpecSection:
    """Build BehaviorSpecSection by extracting SESF code blocks."""
    blocks = extract_sesf_blocks(sections)
    raw = "\n\n".join(blocks) if blocks else ""
    return BehaviorSpecSection(raw_sesf=raw, sesf_blocks=blocks)


def _build_checklist(data: Any) -> list[str]:
    """Build validation checklist."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("_items", [])
    return []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_list(val: Any) -> list[str]:
    if isinstance(val, list):
        return val
    if isinstance(val, str) and val:
        return [val]
    return []


def _ensure_list_or_none(val: Any) -> list[str] | None:
    if val is None:
        return None
    result = _ensure_list(val)
    return result if result else None


def _parse_csv(val: Any) -> list[str] | None:
    if val is None:
        return None
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return [v.strip() for v in val.split(",") if v.strip()]
    return None


def _parse_severity_model(val: Any) -> dict[str, list[str]] | None:
    if val is None:
        return None
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        # Parse "critical: x, y\nhigh: a, b" format
        result = {}
        for line in val.split("\n"):
            line = line.strip().lstrip("-").strip()
            if ":" in line:
                k, v = line.split(":", 1)
                result[k.strip()] = [x.strip() for x in v.split(",")]
        return result if result else None
    return None
```

**Step 4: Run tests**

```bash
pytest tests/test_section_model.py -v
```

Debug and iterate until tests pass. The mapping logic may need adjustment based on how markdown-it-py structures the actual AST.

**Step 5: Commit**

```bash
git add src/reixs/parser/section_model.py tests/test_section_model.py
git commit -m "feat: implement section-to-model mapper (parsed dict → ReixsSpec)"
```

---

## Task 6: Implement 5-pass validator

**Files:**
- Create: `src/reixs/validate/structural.py`
- Create: `src/reixs/validate/ofd.py`
- Create: `src/reixs/validate/domain.py`
- Create: `src/reixs/validate/cross_field.py`
- Create: `src/reixs/sesf/adapter.py`
- Create: `src/reixs/registry/task_types.py`
- Create: `src/reixs/registry/jurisdictions.py`
- Create: `src/reixs/registry/ddd_refs.py`
- Create: `src/reixs/validate/__init__.py` (runner)
- Test: `tests/test_validator.py`
- Test: `tests/test_sesf_adapter.py`

**Step 1: Write validator tests**

Create `tests/test_validator.py`:

```python
"""Tests for REIXS 5-pass validator."""

import pytest
from pathlib import Path

from reixs.parser.markdown_parser import parse_reixs_markdown
from reixs.parser.section_model import build_reixs_spec
from reixs.validate import run_validation
from reixs.validate.report import ValidationReport


VALID_SPEC = Path("specs/templates/lease_abstraction_ontario.reixs.md")


class TestFullValidation:
    def test_valid_spec_passes(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        report = run_validation(spec, strict_sesf=True)
        assert report.status in ("pass", "warn"), (
            f"Expected pass/warn, got {report.status}. "
            f"Errors: {[f.message for f in report.errors]}"
        )

    def test_valid_spec_has_no_errors(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        report = run_validation(spec, strict_sesf=True)
        errors = report.errors
        assert len(errors) == 0, (
            f"Unexpected errors: {[e.message for e in errors]}"
        )


class TestMissingOFD:
    def test_missing_ofd_fails(self):
        spec_path = Path("specs/invalid/missing_ofd.reixs.md")
        if not spec_path.exists():
            pytest.skip("missing_ofd.reixs.md not created yet")
        sections = parse_reixs_markdown(spec_path)
        spec = build_reixs_spec(sections, spec_path)
        report = run_validation(spec, strict_sesf=False)
        ofd_errors = [f for f in report.errors if f.pass_number == 2]
        assert len(ofd_errors) > 0


class TestMissingSESF:
    def test_missing_sesf_fails(self):
        spec_path = Path("specs/invalid/missing_sesf.reixs.md")
        if not spec_path.exists():
            pytest.skip("missing_sesf.reixs.md not created yet")
        sections = parse_reixs_markdown(spec_path)
        spec = build_reixs_spec(sections, spec_path)
        report = run_validation(spec, strict_sesf=True)
        sesf_errors = [f for f in report.errors if f.pass_number == 4]
        assert len(sesf_errors) > 0


class TestMissingDDDRef:
    def test_missing_ddd_ref_fails(self):
        spec_path = Path("specs/invalid/missing_ddd_ref.reixs.md")
        if not spec_path.exists():
            pytest.skip("missing_ddd_ref.reixs.md not created yet")
        sections = parse_reixs_markdown(spec_path)
        spec = build_reixs_spec(sections, spec_path)
        report = run_validation(spec, strict_sesf=False)
        domain_errors = [f for f in report.errors if f.pass_number == 3]
        assert len(domain_errors) > 0
```

Create `tests/test_sesf_adapter.py`:

```python
"""Tests for SESF validator adapter."""

import pytest
import tempfile
from pathlib import Path

from reixs.sesf.adapter import validate_sesf_block
from reixs.validate.report import Finding


VALID_SESF = """\
Lease Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

Purpose
Extract lease terms with provenance tracking.

BEHAVIOR extract_terms: Extract and classify terms

  RULE basic_extraction:
    WHEN field value is found verbatim
    THEN status MUST be FACT

  ERROR no_source:
    WHEN value has no source
    SEVERITY critical
    ACTION reject
    MESSAGE "No source found"

  EXAMPLE found:
    INPUT: term on page 3
    EXPECTED: { "status": "FACT" }

Constraints
* Must process all DDD fields
"""


class TestSESFAdapter:
    def test_valid_sesf_returns_no_errors(self):
        findings = validate_sesf_block(VALID_SESF, pass_number=4)
        errors = [f for f in findings if f.severity == "error"]
        assert len(errors) == 0, (
            f"Unexpected errors: {[e.message for e in errors]}"
        )

    def test_empty_sesf_returns_error(self):
        findings = validate_sesf_block("", pass_number=4)
        errors = [f for f in findings if f.severity == "error"]
        assert len(errors) > 0

    def test_findings_have_correct_pass_number(self):
        findings = validate_sesf_block(VALID_SESF, pass_number=4)
        for f in findings:
            assert f.pass_number == 4
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_validator.py tests/test_sesf_adapter.py -v
```

**Step 3: Implement registry modules**

Create `src/reixs/registry/task_types.py`:

```python
"""Known REIXS task types."""

KNOWN_TASK_TYPES = {
    "lease abstraction",
    "lease_abstraction",
}


def is_known_task_type(task_type: str) -> bool:
    return task_type.lower().strip() in KNOWN_TASK_TYPES
```

Create `src/reixs/registry/jurisdictions.py`:

```python
"""Known jurisdiction profiles."""

KNOWN_JURISDICTIONS = {
    "ontario, canada": {"currency": "CAD", "area_unit": "sq ft"},
    "ontario": {"currency": "CAD", "area_unit": "sq ft"},
}


def is_known_jurisdiction(jurisdiction: str) -> bool:
    return jurisdiction.lower().strip() in KNOWN_JURISDICTIONS
```

Create `src/reixs/registry/ddd_refs.py`:

```python
"""DDD reference format validation and registry."""

import re

DDD_REF_PATTERN = re.compile(r"^re-ddd:[\w_]+@\d+\.\d+\.\d+$")

KNOWN_DDD_REFS = {
    "re-ddd:lease_core_terms_ontario@0.1.0",
}


def is_valid_ddd_format(ref: str) -> bool:
    return bool(DDD_REF_PATTERN.match(ref))


def is_known_ddd_ref(ref: str) -> bool:
    return ref in KNOWN_DDD_REFS
```

**Step 4: Implement SESF adapter**

Create `src/reixs/sesf/adapter.py`:

```python
"""SESF validator adapter — maps SESF validation results to REIXS findings."""

from __future__ import annotations

import tempfile
from pathlib import Path

from reixs.validate.report import Finding

try:
    from reixs.sesf.validate_sesf import (
        parse_sesf,
        check_structural_completeness,
        check_error_consistency,
        check_example_consistency,
    )
    SESF_AVAILABLE = True
except ImportError:
    SESF_AVAILABLE = False


def validate_sesf_block(sesf_text: str, pass_number: int = 4) -> list[Finding]:
    """Validate a SESF text block and return REIXS findings."""
    findings: list[Finding] = []

    if not sesf_text or not sesf_text.strip():
        findings.append(Finding(
            pass_number=pass_number,
            severity="error",
            section="behavior_spec",
            field=None,
            message="SESF block is empty",
            suggestion="Add SESF v3 behavior rules in the ```sesf fenced block",
        ))
        return findings

    if not SESF_AVAILABLE:
        findings.append(Finding(
            pass_number=pass_number,
            severity="warning",
            section="behavior_spec",
            field=None,
            message="SESF validator not available — skipping deep validation",
            suggestion=None,
        ))
        return findings

    # Write to temp file for the SESF parser
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(sesf_text)
        tmp_path = f.name

    try:
        doc = parse_sesf(tmp_path)

        if not doc.meta:
            findings.append(Finding(
                pass_number=pass_number,
                severity="error",
                section="behavior_spec",
                field=None,
                message="SESF block has no Meta section — not a valid SESF v3 spec",
                suggestion="Add Meta line: Version X.Y.Z | Date: YYYY-MM-DD | Domain: ... | Status: active | Tier: micro",
            ))
            return findings

        # Run SESF validation passes
        sesf_results = check_structural_completeness(doc)
        sesf_results.extend(check_error_consistency(doc))
        sesf_results.extend(check_example_consistency(doc))

        # Map SESF ValidationResult → REIXS Finding
        for r in sesf_results:
            severity = _map_sesf_status(r.status)
            findings.append(Finding(
                pass_number=pass_number,
                severity=severity,
                section="behavior_spec",
                field=r.category,
                message=f"[SESF] {r.message}",
                suggestion=None,
            ))
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return findings


def _map_sesf_status(status: str) -> str:
    """Map SESF status (PASS/WARN/FAIL) to REIXS severity."""
    return {
        "PASS": "info",
        "WARN": "warning",
        "FAIL": "error",
    }.get(status, "info")
```

**Step 5: Implement validator passes**

Create `src/reixs/validate/structural.py`:

```python
"""Pass 1: Structural validation."""

from __future__ import annotations

import re

from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import Finding

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PASS = 1


def validate_structural(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []

    # Version format
    if not SEMVER_RE.match(spec.meta.version):
        findings.append(Finding(
            pass_number=PASS, severity="error", section="meta",
            field="version", message=f"Version '{spec.meta.version}' is not valid semver",
            suggestion="Use format: X.Y.Z (e.g., 1.0.0)",
        ))

    # Spec ID present
    if not spec.meta.spec_id:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="meta",
            field="spec_id", message="Spec ID is missing",
            suggestion="Add a unique spec ID (e.g., REIXS-LA-ON-001)",
        ))

    # Task type present
    if not spec.meta.task_type:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="meta",
            field="task_type", message="Task Type is missing",
            suggestion="Specify the task type (e.g., Lease Abstraction)",
        ))

    # Objective present
    if not spec.objective:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="objective",
            field=None, message="Objective section is empty",
            suggestion="Describe what this spec accomplishes",
        ))

    # Validation checklist present
    if not spec.validation_checklist:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="validation_checklist",
            field=None, message="Validation checklist is empty",
            suggestion="Add checklist items to verify spec completeness",
        ))

    return findings
```

Create `src/reixs/validate/ofd.py`:

```python
"""Pass 2: OFD validation."""

from __future__ import annotations

from reixs.schema.enums import Tier
from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import Finding

PASS = 2


def validate_ofd(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []
    ofd = spec.ofd
    tier = spec.meta.tier

    # Required for all tiers
    if not ofd.primary_objective:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="primary_objective", message="Primary Objective is missing",
            suggestion="Define the primary goal of this spec",
        ))

    if not ofd.hard_constraints:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="hard_constraints", message="Hard Constraints list is empty",
            suggestion="Add at least one hard constraint",
        ))

    if not ofd.autofail_conditions:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="autofail_conditions", message="AutoFail Conditions list is empty",
            suggestion="Define conditions that should cause automatic failure",
        ))

    if not ofd.optimization_priority_order:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="optimization_priority_order",
            message="Optimization Priority Order is empty",
            suggestion="List priorities in order (e.g., factual correctness first)",
        ))

    if not ofd.uncertainty_policy:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="uncertainty_policy", message="Uncertainty Policy is missing",
            suggestion="Define how to handle ambiguous or uncertain values",
        ))

    # Heuristic: priority order should mention accuracy/factual
    if ofd.optimization_priority_order:
        combined = " ".join(ofd.optimization_priority_order).lower()
        if "factual" not in combined and "accuracy" not in combined and "correct" not in combined:
            findings.append(Finding(
                pass_number=PASS, severity="warning", section="ofd",
                field="optimization_priority_order",
                message="Priority order does not mention factual accuracy",
                suggestion="Consider including 'Factual correctness' as a priority",
            ))

    # Required for standard/complex tiers
    if tier in (Tier.STANDARD, Tier.COMPLEX):
        sev = "error"
    else:
        sev = "warning"

    if not ofd.secondary_objectives:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="secondary_objectives",
            message="Secondary Objectives not defined",
            suggestion="Add secondary goals for standard/complex tiers",
        ))

    if not ofd.tradeoff_policies:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="tradeoff_policies",
            message="Tradeoff Policies not defined",
            suggestion=None,
        ))

    if not ofd.scoring_model:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="scoring_model",
            message="Scoring Model not defined",
            suggestion=None,
        ))

    if not ofd.escalation_triggers:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="escalation_triggers",
            message="Escalation Triggers not defined",
            suggestion=None,
        ))

    if not ofd.error_severity_model:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="error_severity_model",
            message="Error Severity Model not defined",
            suggestion="Define severity levels: critical, high, medium, low",
        ))

    return findings
```

Create `src/reixs/validate/domain.py`:

```python
"""Pass 3: Domain validation."""

from __future__ import annotations

import re

from reixs.schema.enums import Tier
from reixs.schema.reixs_models import ReixsSpec
from reixs.registry.task_types import is_known_task_type
from reixs.registry.ddd_refs import is_valid_ddd_format, is_known_ddd_ref
from reixs.validate.report import Finding

PASS = 3


def validate_domain(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []

    # Task type known
    if not is_known_task_type(spec.meta.task_type):
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="meta",
            field="task_type",
            message=f"Task type '{spec.meta.task_type}' not in known registry",
            suggestion="Known types: Lease Abstraction",
        ))

    # Jurisdiction declared
    if not spec.domain_context.jurisdiction:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="domain_context",
            field="jurisdiction", message="Jurisdiction not declared",
            suggestion="Add jurisdiction (e.g., Ontario, Canada)",
        ))

    # DDD reference
    ddd = spec.domain_context.ddd_reference
    if not ddd:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="domain_context",
            field="ddd_reference", message="DDD Reference is missing",
            suggestion="Add DDD ref (format: re-ddd:<name>@<semver>)",
        ))
    elif not is_valid_ddd_format(ddd):
        findings.append(Finding(
            pass_number=PASS, severity="error", section="domain_context",
            field="ddd_reference",
            message=f"DDD Reference '{ddd}' has invalid format",
            suggestion="Use format: re-ddd:<name>@X.Y.Z",
        ))
    elif not is_known_ddd_ref(ddd):
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="domain_context",
            field="ddd_reference",
            message=f"DDD Reference '{ddd}' not found in local registry",
            suggestion="Verify the DDD reference exists",
        ))

    # Output contract mentions provenance
    oc_text = spec.output_contract.description.lower()
    if "provenance" not in oc_text and "status" not in oc_text:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="output_contract",
            field=None,
            message="Output contract does not mention provenance or status fields",
            suggestion="Include provenance and fact/inference status in output contract",
        ))

    # EDD suite for standard/complex
    if spec.meta.tier in (Tier.STANDARD, Tier.COMPLEX):
        if not spec.evaluation.edd_suite_id:
            findings.append(Finding(
                pass_number=PASS, severity="error", section="evaluation",
                field="edd_suite_id",
                message="EDD Suite ID required for standard/complex tier",
                suggestion="Add an EDD Suite ID referencing test cases",
            ))

    return findings
```

Create `src/reixs/validate/cross_field.py`:

```python
"""Pass 5: Cross-field consistency checks."""

from __future__ import annotations

from reixs.schema.enums import Tier
from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import Finding

PASS = 5


def validate_cross_field(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []

    # Complex tier requires ADR references
    if spec.meta.tier == Tier.COMPLEX:
        if not spec.domain_context.adr_references:
            findings.append(Finding(
                pass_number=PASS, severity="error", section="domain_context",
                field="adr_references",
                message="Complex tier requires ADR references",
                suggestion="Add ADR References to Domain Context",
            ))

    # If hard constraints mention provenance, output contract should too
    hc_text = " ".join(spec.ofd.hard_constraints).lower()
    oc_text = spec.output_contract.description.lower()
    if "provenance" in hc_text and "provenance" not in oc_text:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="output_contract",
            field=None,
            message="OFD hard constraints mention provenance but output contract does not",
            suggestion="Ensure output contract enforces provenance requirements",
        ))

    # Ontario jurisdiction should have currency
    jurisdiction = spec.domain_context.jurisdiction.lower()
    if "ontario" in jurisdiction and not spec.domain_context.currency:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="domain_context",
            field="currency",
            message="Ontario jurisdiction should declare currency (CAD)",
            suggestion="Add 'Currency: CAD' to Domain Context",
        ))

    return findings
```

**Step 6: Implement validation runner**

Update `src/reixs/validate/__init__.py`:

```python
"""REIXS validation — 5-pass validator pipeline."""

from __future__ import annotations

from reixs.schema.reixs_models import ReixsSpec
from reixs.sesf.adapter import validate_sesf_block
from reixs.validate.cross_field import validate_cross_field
from reixs.validate.domain import validate_domain
from reixs.validate.ofd import validate_ofd
from reixs.validate.report import Finding, ValidationReport, PassSummary
from reixs.validate.structural import validate_structural


PASS_NAMES = {
    1: "Structural",
    2: "OFD",
    3: "Domain",
    4: "SESF",
    5: "Cross-field",
}


def run_validation(spec: ReixsSpec, strict_sesf: bool = True) -> ValidationReport:
    """Run all 5 validation passes and return a report."""
    all_findings: list[Finding] = []

    # Pass 1: Structural
    all_findings.extend(validate_structural(spec))

    # Pass 2: OFD
    all_findings.extend(validate_ofd(spec))

    # Pass 3: Domain
    all_findings.extend(validate_domain(spec))

    # Pass 4: SESF
    sesf_findings = validate_sesf_block(spec.behavior_spec.raw_sesf)
    if not strict_sesf:
        # Downgrade errors to warnings
        for f in sesf_findings:
            if f.severity == "error":
                f = f.model_copy(update={"severity": "warning"})
            all_findings.append(f)
    else:
        all_findings.extend(sesf_findings)

    # Pass 5: Cross-field
    all_findings.extend(validate_cross_field(spec))

    # Build pass summaries
    summaries = {}
    for pn, name in PASS_NAMES.items():
        pf = [f for f in all_findings if f.pass_number == pn]
        summaries[pn] = PassSummary(
            pass_number=pn,
            name=name,
            errors=sum(1 for f in pf if f.severity == "error"),
            warnings=sum(1 for f in pf if f.severity == "warning"),
            infos=sum(1 for f in pf if f.severity == "info"),
        )

    return ValidationReport(
        spec_id=spec.meta.spec_id,
        spec_version=spec.meta.version,
        findings=all_findings,
        pass_summaries=summaries,
        sesf_findings=[],
    )
```

**Step 7: Run tests**

```bash
pytest tests/test_validator.py tests/test_sesf_adapter.py -v
```

Debug until tests pass.

**Step 8: Commit**

```bash
git add src/reixs/validate/ src/reixs/sesf/adapter.py src/reixs/registry/ tests/test_validator.py tests/test_sesf_adapter.py
git commit -m "feat: implement 5-pass validator with SESF adapter"
```

---

## Task 7: Implement compiler

**Files:**
- Create: `src/reixs/compile/compiler.py`
- Test: `tests/test_compiler.py`

**Step 1: Write compiler tests**

Create `tests/test_compiler.py`:

```python
"""Tests for REIXS compiler."""

import json
import pytest
import tempfile
from pathlib import Path

from reixs.parser.markdown_parser import parse_reixs_markdown
from reixs.parser.section_model import build_reixs_spec
from reixs.validate import run_validation
from reixs.compile.compiler import compile_reixs


VALID_SPEC = Path("specs/templates/lease_abstraction_ontario.reixs.md")


class TestCompiler:
    def test_compile_produces_runtime_json(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        report = run_validation(spec)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir)
            result = compile_reixs(spec, report, output)
            runtime_path = output / "reixs.runtime.json"
            assert runtime_path.exists()
            data = json.loads(runtime_path.read_text())
            assert "spec_metadata" in data
            assert "ofd" in data
            assert "behavior_rules" in data

    def test_compile_produces_manifest(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        report = run_validation(spec)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir)
            compile_reixs(spec, report, output)
            manifest_path = output / "reixs.manifest.json"
            assert manifest_path.exists()
            data = json.loads(manifest_path.read_text())
            assert data["spec_id"] == "REIXS-LA-ON-001"
            assert data["version"] == "1.0.0"
            assert len(data["source_hash"]) == 64

    def test_compile_refuses_on_fail(self):
        sections = parse_reixs_markdown(VALID_SPEC)
        spec = build_reixs_spec(sections, VALID_SPEC)
        # Create a fake failed report
        from reixs.validate.report import Finding, ValidationReport
        report = ValidationReport(
            spec_id="X", spec_version="1.0.0",
            findings=[Finding(
                pass_number=1, severity="error", section="meta",
                field=None, message="Test error", suggestion=None,
            )],
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="Cannot compile"):
                compile_reixs(spec, report, Path(tmpdir))
```

**Step 2: Implement compiler**

Create `src/reixs/compile/compiler.py`:

```python
"""REIXS compiler — converts validated ReixsSpec to runtime JSON artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import ValidationReport


def compile_reixs(
    spec: ReixsSpec,
    report: ValidationReport,
    output_dir: Path,
    include_validation: bool = False,
) -> dict[str, Path]:
    """Compile a validated ReixsSpec to runtime JSON.

    Raises ValueError if validation status is 'fail'.
    Returns dict of artifact name → file path.
    """
    if report.status == "fail":
        raise ValueError(
            f"Cannot compile spec with validation failures. "
            f"Found {len(report.errors)} error(s). Run 'reixs validate' first."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, Path] = {}

    # --- Runtime payload ---
    runtime = {
        "spec_metadata": {
            "spec_id": spec.meta.spec_id,
            "version": spec.meta.version,
            "task_type": spec.meta.task_type,
            "tier": spec.meta.tier.value,
            "author": spec.meta.author,
            "date": spec.meta.date.isoformat(),
        },
        "task_context": {
            "objective": spec.objective,
            "jurisdiction": spec.domain_context.jurisdiction,
            "currency": spec.domain_context.currency,
            "area_unit": spec.domain_context.area_unit,
        },
        "ofd": {
            "primary_objective": spec.ofd.primary_objective,
            "hard_constraints": spec.ofd.hard_constraints,
            "autofail_conditions": spec.ofd.autofail_conditions,
            "optimization_priority_order": spec.ofd.optimization_priority_order,
            "uncertainty_policy": spec.ofd.uncertainty_policy,
        },
        "behavior_rules": {
            "raw_sesf": spec.behavior_spec.raw_sesf,
            "block_count": len(spec.behavior_spec.sesf_blocks),
        },
        "output_contract": {
            "description": spec.output_contract.description,
            "fields": spec.output_contract.fields,
        },
        "eval_config": {
            "edd_suite_id": spec.evaluation.edd_suite_id,
            "min_pass_rate": spec.evaluation.min_pass_rate,
            "regression_cases": spec.evaluation.regression_cases,
        },
        "references": {
            "ddd_reference": spec.domain_context.ddd_reference,
            "adr_references": spec.domain_context.adr_references or [],
        },
        "validation_status": report.status,
    }

    runtime_path = output_dir / "reixs.runtime.json"
    runtime_path.write_text(json.dumps(runtime, indent=2, default=str))
    artifacts["runtime"] = runtime_path

    # --- Manifest ---
    manifest = {
        "spec_id": spec.meta.spec_id,
        "version": spec.meta.version,
        "source_hash": spec.source_hash,
        "compile_timestamp": datetime.now(timezone.utc).isoformat(),
        "artifacts": [str(p.name) for p in artifacts.values()],
    }
    # Add manifest itself to artifact list
    manifest["artifacts"].append("reixs.manifest.json")

    manifest_path = output_dir / "reixs.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    artifacts["manifest"] = manifest_path

    # --- Optional validation report ---
    if include_validation:
        val_path = output_dir / "reixs.validation.json"
        val_path.write_text(report.model_dump_json(indent=2))
        artifacts["validation"] = val_path

    return artifacts
```

**Step 3: Run tests**

```bash
pytest tests/test_compiler.py -v
```

**Step 4: Commit**

```bash
git add src/reixs/compile/ tests/test_compiler.py
git commit -m "feat: implement REIXS compiler (spec → runtime JSON + manifest)"
```

---

## Task 8: Wire up CLI

**Files:**
- Modify: `src/reixs/cli.py`
- Test: manual CLI testing

**Step 1: Implement full CLI**

Replace the skeleton in `src/reixs/cli.py` with working commands that wire parser → validator → compiler:

```python
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

    # Find the template file
    template_name = template.replace("-", "_")
    template_file = TEMPLATES_DIR / f"{template_name}.reixs.md"
    if not template_file.exists():
        console.print(f"[red]Template not found: {template}[/red]")
        console.print(f"  Looked for: {template_file}")
        sys.exit(1)

    dest = output_file or f"{template_name}.reixs.md"
    shutil.copy2(template_file, dest)
    console.print(f"[green]Created {dest} from template '{template}'[/green]")
```

**Step 2: Test CLI manually**

```bash
reixs validate specs/templates/lease_abstraction_ontario.reixs.md
reixs validate specs/templates/lease_abstraction_ontario.reixs.md --json
reixs compile specs/templates/lease_abstraction_ontario.reixs.md -o build/
reixs init --list-templates
reixs init --template lease-abstraction-ontario -o test_output.reixs.md
```

Verify: validate shows Rich table, compile produces `build/reixs.runtime.json` and `build/reixs.manifest.json`, init copies template.

**Step 3: Clean up test artifacts**

```bash
rm -rf build/ test_output.reixs.md
```

**Step 4: Commit**

```bash
git add src/reixs/cli.py
git commit -m "feat: wire CLI commands (validate, compile, init)"
```

---

## Task 9: Write ADRs and README

**Files:**
- Create: `docs/ADR/ADR-001-layered-artifacts.md`
- Create: `docs/ADR/ADR-003-hard-constraints-before-scoring.md`
- Create: `README.md`

**Step 1: Write ADR-001**

Create `docs/ADR/ADR-001-layered-artifacts.md`:

```markdown
# ADR-001: Layered Artifact Boundaries

## Status
Accepted

## Context
REIXS specs reference multiple supporting artifacts: domain data dictionaries (DDD), architecture decision records (ADR), and evaluation datasets (EDD). The question is whether to embed these fully in the REIXS spec or reference them externally.

## Decision
REIXS runtime specs REFERENCE supporting artifacts (DDD, ADR, EDD) by versioned identifier rather than embedding their full content.

## Consequences
- REIXS specs stay focused on task execution, not domain definitions
- DDD/ADR/EDD can evolve independently with their own versioning
- Validator checks that references exist and are well-formatted
- Downstream consumers must resolve references to access full content
```

**Step 2: Write ADR-003**

Create `docs/ADR/ADR-003-hard-constraints-before-scoring.md`:

```markdown
# ADR-003: Hard Constraints Before Scoring

## Status
Accepted

## Context
The OFD section defines both hard constraints (absolute requirements) and a scoring model (weighted optimization). When evaluating AI outputs, the system must decide whether to score first and then check constraints, or vice versa.

## Decision
Hard constraint violations cause AUTOMATIC FAILURE before any weighted scoring is applied. An output that violates a hard constraint receives no score — it is rejected.

## Consequences
- AutoFail conditions are checked first in all evaluation paths
- The scoring model only applies to outputs that pass all hard constraints
- This prevents "high-scoring but factually wrong" results from passing
- Constraint checking is computationally cheaper than scoring, so this is also more efficient
```

**Step 3: Write README**

Create `README.md` with quickstart (under 5 minutes to understand):

```markdown
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
```

**Step 4: Commit**

```bash
git add docs/ADR/ README.md
git commit -m "docs: add ADR-001, ADR-003, and README quickstart"
```

---

## Task 10: Run full test suite and generate golden files

**Files:**
- Create: `tests/golden/valid_report.json`
- Create: `tests/golden/valid_runtime.json`

**Step 1: Run full test suite**

```bash
pytest tests/ -v --tb=short
```

All tests must pass. Fix any failures.

**Step 2: Generate golden files**

```bash
reixs validate specs/templates/lease_abstraction_ontario.reixs.md --json > tests/golden/valid_report.json
reixs compile specs/templates/lease_abstraction_ontario.reixs.md -o /tmp/reixs_golden/ && cp /tmp/reixs_golden/reixs.runtime.json tests/golden/valid_runtime.json
rm -rf /tmp/reixs_golden/
```

**Step 3: Verify success criteria**

```bash
# Valid spec passes
reixs validate specs/templates/lease_abstraction_ontario.reixs.md && echo "PASS: valid spec validates"

# Invalid specs fail
reixs validate specs/invalid/missing_ofd.reixs.md 2>/dev/null; [ $? -eq 1 ] && echo "PASS: missing OFD fails"
reixs validate specs/invalid/missing_sesf.reixs.md 2>/dev/null; [ $? -ne 0 ] && echo "PASS: missing SESF fails"
reixs validate specs/invalid/missing_ddd_ref.reixs.md 2>/dev/null; [ $? -ne 0 ] && echo "PASS: missing DDD ref fails"

# Compile produces artifacts
reixs compile specs/templates/lease_abstraction_ontario.reixs.md -o /tmp/reixs_test/ && ls /tmp/reixs_test/
rm -rf /tmp/reixs_test/

# Init works
reixs init --template lease-abstraction-ontario -o /tmp/test_init.reixs.md && echo "PASS: init works"
rm -f /tmp/test_init.reixs.md

# Tests pass
pytest tests/ -v
```

**Step 4: Commit golden files and final state**

```bash
git add tests/golden/
git commit -m "test: add golden regression files for validation and runtime output"
```

**Step 5: Push to GitHub**

```bash
git push -u origin main
```

---

## Summary

| Task | What | Key Files |
|---|---|---|
| 0 | Bootstrap project | `pyproject.toml`, `cli.py` skeleton, directory structure |
| 1 | Vendor SESF validator | `src/reixs/sesf/validate_sesf.py` |
| 2 | Data models | `schema/enums.py`, `schema/reixs_models.py`, `validate/report.py` |
| 3 | Template specs | `specs/templates/`, `specs/invalid/` |
| 4 | Markdown parser | `parser/markdown_parser.py`, `parser/sesf_extractor.py` |
| 5 | Section-to-model mapper | `parser/section_model.py` |
| 6 | 5-pass validator | `validate/structural.py`, `ofd.py`, `domain.py`, `cross_field.py`, `sesf/adapter.py` |
| 7 | Compiler | `compile/compiler.py` |
| 8 | Wire CLI | `cli.py` full implementation |
| 9 | ADRs + README | `docs/ADR/`, `README.md` |
| 10 | Golden files + verification | `tests/golden/`, success criteria checks |
