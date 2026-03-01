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
