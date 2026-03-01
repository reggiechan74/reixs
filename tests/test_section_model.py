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
