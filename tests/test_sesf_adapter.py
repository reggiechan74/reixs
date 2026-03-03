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


VALID_SESF_V4 = """\
Standard Tier Spec

Meta
* Version: 1.0.0
* Date: 2026-03-03
* Domain: Test
* Status: active
* Tier: standard

Notation
* $ -- references a variable or config value
* @ -- marks a structured block
* -> -- means "produces" or "routes to"
* MUST/SHOULD/MAY/CAN -- requirement strength keywords

Purpose
Test spec for v4 validation.

Scope
* IN SCOPE: testing v4 features
* OUT OF SCOPE: production use

Inputs
* document: string - the source document - required

Outputs
* result: string - the extracted result

@config
  max_retries: 3

Types
-- none: all data structures are inline

Functions
-- none: all logic is expressed directly in behavior rules

BEHAVIOR test_behavior: Test behavior for v4 validation

  RULE basic_rule:
    WHEN input is provided
    THEN output MUST be produced

  @route classify_input [first_match_wins]
    input is type A   -> handler_a
    input is type B   -> handler_b
    input is type C   -> handler_c
    *                 -> default_handler

  ERRORS:
  | name | when | severity | action | message |
  |------|------|----------|--------|---------|
  | no_input | input is missing | critical | halt | "Input required" |

  EXAMPLES:
    valid_input: input="hello" -> output produced
    missing_input: input=null -> rejected with "Input required"

Constraints
* Output MUST be non-empty

Dependencies
* None
"""


class TestConfigurableChecks:
    def test_default_runs_all_checks(self):
        """Default (no checks param) runs all available checks."""
        findings = validate_sesf_block(VALID_SESF, pass_number=4)
        categories = {f.field for f in findings}
        assert "meta" in categories or "sections" in categories

    def test_custom_checks_subset(self):
        """Passing a subset of check names limits which checks run."""
        findings = validate_sesf_block(
            VALID_SESF, pass_number=4,
            checks=["check_structural_completeness"],
        )
        error_findings = [f for f in findings if f.field == "error_consistency"]
        assert len(error_findings) == 0

    def test_empty_checks_returns_no_validation_findings(self):
        """Empty checks list means no SESF validation runs (only parse)."""
        findings = validate_sesf_block(VALID_SESF, pass_number=4, checks=[])
        assert len(findings) == 0

    def test_v4_features_validated(self):
        """v4 spec with @config, @route, compact tables passes validation."""
        findings = validate_sesf_block(VALID_SESF_V4, pass_number=4)
        errors = [f for f in findings if f.severity == "error"]
        assert len(errors) == 0, (
            f"Unexpected errors: {[e.message for e in errors]}"
        )

    def test_v3_message_updated(self):
        """Empty SESF block message references v4 not v3."""
        findings = validate_sesf_block("", pass_number=4)
        error_msgs = [f.message for f in findings if f.severity == "error"]
        assert any("v4" in m or "SESF" in m for m in error_msgs)
        assert not any("v3" in m for m in error_msgs)
