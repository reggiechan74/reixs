"""REIXS compiler output models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class RuntimePayload(BaseModel):
    spec_metadata: dict[str, Any]
    task_context: dict[str, Any]
    ofd: dict[str, Any]
    behavior_rules: dict[str, Any]
    output_contract: dict[str, Any]
    eval_config: dict[str, Any]
    references: dict[str, Any]
    validation_status: str


class Manifest(BaseModel):
    spec_id: str
    version: str
    source_hash: str
    compile_timestamp: str
    artifacts: list[str]
