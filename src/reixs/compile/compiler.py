"""REIXS compiler — converts validated ReixsSpec to runtime JSON artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import ValidationReport


def compile_reixs(
    spec: ReixsSpec,
    report: ValidationReport,
    output_dir: Path,
    include_validation: bool = False,
) -> dict[str, Path]:
    """Compile a validated ReixsSpec to runtime JSON.

    Raises ValueError if validation status is 'fail'.
    Returns dict of artifact name -> file path.
    """
    if report.status == "fail":
        raise ValueError(
            f"Cannot compile spec with validation failures. "
            f"Found {len(report.errors)} error(s). Run 'reixs validate' first."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, Path] = {}

    # --- Runtime payload ---
    runtime = {
        "spec_metadata": {
            "spec_id": spec.meta.spec_id,
            "version": spec.meta.version,
            "task_type": spec.meta.task_type,
            "tier": spec.meta.tier.value,
            "author": spec.meta.author,
            "date": spec.meta.date.isoformat(),
        },
        "task_context": {
            "objective": spec.objective,
            "jurisdiction": spec.domain_context.jurisdiction,
            "currency": spec.domain_context.currency,
            "area_unit": spec.domain_context.area_unit,
        },
        "ofd": {
            "primary_objective": spec.ofd.primary_objective,
            "hard_constraints": spec.ofd.hard_constraints,
            "autofail_conditions": spec.ofd.autofail_conditions,
            "optimization_priority_order": spec.ofd.optimization_priority_order,
            "uncertainty_policy": spec.ofd.uncertainty_policy,
        },
        "behavior_rules": {
            "raw_sesf": spec.behavior_spec.raw_sesf,
            "block_count": len(spec.behavior_spec.sesf_blocks),
        },
        "output_contract": {
            "description": spec.output_contract.description,
            "fields": spec.output_contract.fields,
        },
        "eval_config": {
            "edd_suite_id": spec.evaluation.edd_suite_id,
            "min_pass_rate": spec.evaluation.min_pass_rate,
            "regression_cases": spec.evaluation.regression_cases,
        },
        "references": {
            "ddd_reference": spec.domain_context.ddd_reference,
            "adr_references": spec.domain_context.adr_references or [],
        },
        "validation_status": report.status,
    }

    runtime_path = output_dir / "reixs.runtime.json"
    runtime_path.write_text(json.dumps(runtime, indent=2, default=str))
    artifacts["runtime"] = runtime_path

    # --- Manifest ---
    manifest = {
        "spec_id": spec.meta.spec_id,
        "version": spec.meta.version,
        "source_hash": spec.source_hash,
        "compile_timestamp": datetime.now(timezone.utc).isoformat(),
        "artifacts": [str(p.name) for p in artifacts.values()],
    }
    manifest["artifacts"].append("reixs.manifest.json")

    manifest_path = output_dir / "reixs.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    artifacts["manifest"] = manifest_path

    # --- Optional validation report ---
    if include_validation:
        val_path = output_dir / "reixs.validation.json"
        val_path.write_text(report.model_dump_json(indent=2))
        artifacts["validation"] = val_path

    return artifacts
