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
