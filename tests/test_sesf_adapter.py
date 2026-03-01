"""Tests for SESF validator adapter."""

import pytest
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
