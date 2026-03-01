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
    constraints = _build_constraints(sections.get("constraints", {}))
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
    """Build MetaSection from parsed meta dict.

    Parser output: flat dict of string key-value pairs.
    Example: {'spec_id': 'REIXS-LA-ON-001', 'tier': 'standard', 'date': '2026-03-01', ...}
    """
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
    """Build OFDSection from parsed OFD dict.

    Parser output: dict where sub-heading keys map to either str or list[str].
    - primary_objective: str (paragraph text under ### Primary Objective)
    - hard_constraints: list[str]
    - scoring_model: list[str] (bullet items, not structured)
    - error_severity_model: list[str] (e.g. "critical: fabricated term, wrong currency")
    """
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
        scoring_model=_build_scoring_model(data.get("scoring_model")),
        escalation_triggers=_ensure_list_or_none(
            data.get("escalation_triggers")
        ),
        error_severity_model=_parse_severity_model(
            data.get("error_severity_model")
        ),
    )


def _build_domain_context(data: dict) -> DomainContextSection:
    """Build DomainContextSection.

    Parser output: flat dict of string k/v pairs.
    adr_references is a comma-separated string like 'ADR-001, ADR-003'.
    """
    return DomainContextSection(
        jurisdiction=data.get("jurisdiction", ""),
        currency=data.get("currency"),
        area_unit=data.get("area_unit"),
        ddd_reference=data.get("ddd_reference"),
        adr_references=_parse_csv(data.get("adr_references")),
    )


def _build_inputs(data: Any) -> InputsSection:
    """Build InputsSection.

    Parser output: dict of string k/v pairs (parser treats bullets as k/v).
    Example: {'source_document': 'PDF (scanned or native)', ...}
    """
    items: list[dict[str, str]] = []
    if isinstance(data, dict):
        for k, v in data.items():
            if not k.startswith("_"):
                items.append({"key": k, "value": str(v)})
        # Also handle any _items list (fallback)
        for item in data.get("_items", []):
            parts = str(item).split(":", 1)
            if len(parts) == 2:
                items.append({"key": parts[0].strip(), "value": parts[1].strip()})
            else:
                items.append({"key": str(item), "value": ""})
    elif isinstance(data, list):
        for item in data:
            parts = str(item).split(":", 1)
            if len(parts) == 2:
                items.append({"key": parts[0].strip(), "value": parts[1].strip()})
            else:
                items.append({"key": str(item), "value": ""})
    return InputsSection(items=items)


def _build_constraints(data: Any) -> ConstraintsSection:
    """Build ConstraintsSection.

    Parser output: dict of k/v pairs (parser treats "Processing time: < 120 seconds"
    as key-value). We convert all values to plain strings.
    """
    items: list[str] = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == "_items":
                items.extend(v)
            elif not k.startswith("_"):
                items.append(f"{k}: {v}")
    elif isinstance(data, list):
        items = data
    return ConstraintsSection(items=items)


def _build_output_contract(data: Any) -> OutputContractSection:
    """Build OutputContractSection.

    Parser output: dict with '_text' and backtick-wrapped keys.
    Example: {'_text': 'Each extracted field MUST include:',
              '`value`': 'the extracted or derived value', ...}
    """
    text = ""
    fields: list[dict[str, str]] = []
    if isinstance(data, dict):
        text = data.get("_text", "")
        for k, v in data.items():
            if k.startswith("_"):
                continue
            # Strip backticks from key names like `value`
            name = k.strip("`")
            fields.append({"name": name, "description": str(v)})
    elif isinstance(data, str):
        text = data
    return OutputContractSection(description=text, fields=fields)


def _build_evaluation(data: Any) -> EvaluationSection:
    """Build EvaluationSection.

    Parser output: dict of string k/v pairs.
    regression_cases is a comma-separated string.
    """
    if isinstance(data, str):
        return EvaluationSection(raw_text=data)

    raw_parts: list[str] = []
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
    """Build validation checklist.

    Parser output: list[str] (already cleaned by parser, checkbox markers removed).
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("_items", [])
    return []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ensure_list(val: Any) -> list[str]:
    """Coerce a value into a list of strings."""
    if isinstance(val, list):
        return val
    if isinstance(val, str) and val:
        return [val]
    return []


def _ensure_list_or_none(val: Any) -> list[str] | None:
    """Coerce a value into a list of strings, or None if empty/absent."""
    if val is None:
        return None
    result = _ensure_list(val)
    return result if result else None


def _parse_csv(val: Any) -> list[str] | None:
    """Parse a comma-separated string into a list, or passthrough a list."""
    if val is None:
        return None
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return [v.strip() for v in val.split(",") if v.strip()]
    return None


def _build_scoring_model(val: Any) -> str | dict | None:
    """Convert scoring model data to a string or dict.

    Parser output is list[str] of bullet items. Join them into a single string.
    """
    if val is None:
        return None
    if isinstance(val, list):
        return "\n".join(val) if val else None
    if isinstance(val, (str, dict)):
        return val or None
    return None


def _parse_severity_model(val: Any) -> dict[str, list[str]] | None:
    """Parse error severity model into {severity: [error_types]}.

    Parser output is list[str] like:
        ['critical: fabricated term, wrong currency, wrong dates',
         'high: missing critical field without flag, provenance gap', ...]
    """
    if val is None:
        return None
    if isinstance(val, dict):
        return val

    lines: list[str] = []
    if isinstance(val, list):
        lines = val
    elif isinstance(val, str):
        lines = val.split("\n")

    result: dict[str, list[str]] = {}
    for line in lines:
        line = line.strip().lstrip("-").strip()
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = [x.strip() for x in v.split(",")]
    return result if result else None
