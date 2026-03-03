"""Tests for DDD reference format validation and registry."""

import pytest

from reixs.registry.ddd_refs import is_known_ddd_ref, is_valid_ddd_format


class TestDDDRefFormat:
    @pytest.mark.parametrize("ref", [
        "re-ddd:lease_core_terms_ontario@0.1.0",
        "re-ddd:lease_abstraction_commercial_na@1.0.0",
        "re-ddd:core_commercial_re_na@1.0.0",
        "re-ddd:property_management_commercial_na@1.0.0",
        "re-ddd:asset_management_commercial_na@1.0.0",
        "re-ddd:leasing_commercial_na@1.0.0",
        "re-ddd:investment_appraisal_commercial_na@1.0.0",
    ])
    def test_valid_ddd_format(self, ref):
        assert is_valid_ddd_format(ref)

    @pytest.mark.parametrize("ref", [
        "",
        "re-ddd:",
        "re-ddd:name",
        "re-ddd:name@1.0",
        "ddd:name@1.0.0",
        "re-ddd:name with spaces@1.0.0",
    ])
    def test_invalid_ddd_format(self, ref):
        assert not is_valid_ddd_format(ref)


class TestKnownDDDRefs:
    @pytest.mark.parametrize("ref", [
        "re-ddd:core_commercial_re_na@1.0.0",
        "re-ddd:property_management_commercial_na@1.0.0",
        "re-ddd:asset_management_commercial_na@1.0.0",
        "re-ddd:leasing_commercial_na@1.0.0",
        "re-ddd:investment_appraisal_commercial_na@1.0.0",
        "re-ddd:lease_abstraction_commercial_na@1.0.0",
        "re-ddd:lease_core_terms_ontario@0.1.0",
    ])
    def test_known_ddd_refs(self, ref):
        assert is_known_ddd_ref(ref)

    def test_unknown_ddd_ref(self):
        assert not is_known_ddd_ref("re-ddd:nonexistent@1.0.0")

    def test_registry_has_expected_count(self):
        from reixs.registry.ddd_refs import KNOWN_DDD_REFS
        assert len(KNOWN_DDD_REFS) == 7
