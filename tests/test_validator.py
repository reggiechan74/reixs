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
