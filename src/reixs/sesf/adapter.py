"""SESF validator adapter — maps SESF validation results to REIXS findings."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Sequence

from reixs.validate.report import Finding

try:
    from reixs.sesf.validate_sesf import (
        parse_sesf,
        check_structural_completeness,
        check_error_consistency,
        check_example_consistency,
        check_type_consistency,
        check_rule_integrity,
        check_cross_behavior,
        check_config_references,
        check_variable_threading,
        check_route_completeness,
        check_error_table_structure,
        check_notation_section,
    )
    SESF_AVAILABLE = True
except ImportError:
    SESF_AVAILABLE = False

# Registry of all available SESF check functions, keyed by name.
# Order matters — structural checks run first, then consistency, then v4.
ALL_CHECKS: dict[str, object] = {}
if SESF_AVAILABLE:
    ALL_CHECKS = {
        "check_structural_completeness": check_structural_completeness,
        "check_type_consistency": check_type_consistency,
        "check_rule_integrity": check_rule_integrity,
        "check_error_consistency": check_error_consistency,
        "check_example_consistency": check_example_consistency,
        "check_cross_behavior": check_cross_behavior,
        "check_config_references": check_config_references,
        "check_variable_threading": check_variable_threading,
        "check_route_completeness": check_route_completeness,
        "check_error_table_structure": check_error_table_structure,
        "check_notation_section": check_notation_section,
    }


def validate_sesf_block(
    sesf_text: str,
    pass_number: int = 4,
    checks: Sequence[str] | None = None,
) -> list[Finding]:
    """Validate a SESF text block and return REIXS findings.

    Args:
        sesf_text: The raw SESF specification text.
        pass_number: The REIXS validation pass number (default 4).
        checks: Optional list of check function names to run.
                Defaults to all available checks. Pass an empty list
                to skip all SESF validation (parse only).
    """
    findings: list[Finding] = []

    if not sesf_text or not sesf_text.strip():
        findings.append(Finding(
            pass_number=pass_number,
            severity="error",
            section="behavior_spec",
            field=None,
            message="SESF block is empty",
            suggestion="Add SESF v4 behavior rules in the ```sesf fenced block",
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

    # Resolve which checks to run
    if checks is None:
        selected = list(ALL_CHECKS.values())
    else:
        selected = [ALL_CHECKS[name] for name in checks if name in ALL_CHECKS]

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
                message="SESF block has no Meta section — not a valid SESF v4 spec",
                suggestion="Add Meta line: Version X.Y.Z | Date: YYYY-MM-DD | Domain: ... | Status: active | Tier: micro",
            ))
            return findings

        # Run selected SESF validation checks
        sesf_results = []
        for check_fn in selected:
            sesf_results.extend(check_fn(doc))

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
