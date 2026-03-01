"""Extract SESF fenced code blocks from parsed REIXS sections."""

from __future__ import annotations


def extract_sesf_blocks(sections: dict) -> list[str]:
    """Extract raw text from ```sesf fenced code blocks.

    Looks in the 'behavior_spec' section for code blocks tagged 'sesf'.
    Returns a list of raw SESF text strings.
    """
    behavior = sections.get("behavior_spec", {})
    if isinstance(behavior, dict):
        blocks = behavior.get("_code_blocks", [])
        return [b["content"] for b in blocks if b.get("lang") == "sesf"]
    return []
