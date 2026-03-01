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
