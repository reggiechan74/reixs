"""REIXS Markdown parser — converts .reixs.md files into section dictionaries.

Uses markdown-it-py to parse the AST, then walks it to extract sections,
key-value pairs, lists, sub-headings, and fenced code blocks.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt


# ---------------------------------------------------------------------------
# Section alias map
# ---------------------------------------------------------------------------

SECTION_ALIASES: dict[str, list[str]] = {
    "meta": ["meta"],
    "objective": ["objective"],
    "domain_context": ["domain context", "domain"],
    "inputs": ["inputs", "input"],
    "ofd": [
        "objective function design",
        "objective function design (ofd)",
        "ofd",
    ],
    "constraints": ["constraints"],
    "output_contract": ["output contract"],
    "evaluation": ["evaluation", "evaluation / edd", "eval", "edd"],
    "behavior_spec": [
        "behavior spec",
        "behavior spec (sesf)",
        "sesf",
        "behavior",
    ],
    "validation_checklist": ["validation checklist", "checklist"],
}

_ALIAS_LOOKUP: dict[str, str] = {}
for canonical, aliases in SECTION_ALIASES.items():
    for alias in aliases:
        _ALIAS_LOOKUP[alias.lower()] = canonical


def _normalize_heading(text: str) -> str | None:
    """Map a heading string to its canonical section name, or None."""
    cleaned = text.strip().lower()
    if cleaned in _ALIAS_LOOKUP:
        return _ALIAS_LOOKUP[cleaned]
    cleaned = re.sub(r"[#*_`]", "", cleaned).strip()
    if cleaned in _ALIAS_LOOKUP:
        return _ALIAS_LOOKUP[cleaned]
    return None


def _normalize_key(key: str) -> str:
    """Normalize a key-value key to snake_case."""
    return re.sub(r"[\s\-]+", "_", key.strip().lower())


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_reixs_markdown(filepath: Path) -> dict[str, Any]:
    """Parse a REIXS markdown file into a section dictionary.

    Returns a dict keyed by canonical section names. Each value is either:
    - dict: for sections with key-value pairs or sub-headings
    - list[str]: for sections with bullet lists
    - str: for sections with free text
    """
    md = MarkdownIt()
    content = filepath.read_text(encoding="utf-8")
    tokens = md.parse(content)

    sections: dict[str, Any] = {}
    current_section: str | None = None
    current_subsection: str | None = None
    current_data: dict[str, Any] = {}

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # --- Heading detection ---
        if token.type == "heading_open":
            level = int(token.tag[1])  # h1=1, h2=2, h3=3
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                heading_text = tokens[i + 1].content

                if level == 2:
                    # Flush previous section
                    if current_section is not None:
                        sections[current_section] = _finalize_section(current_data)
                    canonical = _normalize_heading(heading_text)
                    if canonical:
                        current_section = canonical
                        current_data = {}
                        current_subsection = None
                    else:
                        current_section = None
                        current_data = {}

                elif level == 3 and current_section is not None:
                    current_subsection = _normalize_key(heading_text)

            i += 3  # skip heading_open, inline, heading_close
            continue

        # --- Bullet list ---
        if token.type == "bullet_list_open" and current_section is not None:
            items = _extract_list_items(tokens, i)
            target_key = current_subsection or "_items"

            if current_section == "meta":
                for item in items:
                    k, v = _parse_kv(item)
                    if k:
                        current_data[k] = v
            elif current_section == "validation_checklist":
                cleaned = [re.sub(r"^\[[ x]\]\s*", "", item) for item in items]
                current_data.setdefault("_items", []).extend(cleaned)
            elif current_subsection:
                current_data[current_subsection] = items
            else:
                parsed_any_kv = False
                for item in items:
                    k, v = _parse_kv(item)
                    if k:
                        current_data[k] = v
                        parsed_any_kv = True
                if not parsed_any_kv:
                    current_data.setdefault("_items", []).extend(items)

            # Skip past the list
            depth = 1
            i += 1
            while i < len(tokens) and depth > 0:
                if tokens[i].type == "bullet_list_open":
                    depth += 1
                elif tokens[i].type == "bullet_list_close":
                    depth -= 1
                i += 1
            continue

        # --- Ordered list ---
        if token.type == "ordered_list_open" and current_section is not None:
            items = _extract_ordered_items(tokens, i)
            target_key = current_subsection or "_items"
            if current_subsection:
                current_data[current_subsection] = items
            else:
                current_data.setdefault("_items", []).extend(items)
            depth = 1
            i += 1
            while i < len(tokens) and depth > 0:
                if tokens[i].type == "ordered_list_open":
                    depth += 1
                elif tokens[i].type == "ordered_list_close":
                    depth -= 1
                i += 1
            continue

        # --- Fenced code block ---
        if token.type == "fence" and current_section is not None:
            lang = (token.info or "").strip()
            current_data.setdefault("_code_blocks", []).append({
                "lang": lang,
                "content": token.content,
            })
            i += 1
            continue

        # --- Paragraph (free text) ---
        if token.type == "paragraph_open" and current_section is not None:
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                text = tokens[i + 1].content
                if current_subsection:
                    existing = current_data.get(current_subsection, "")
                    if isinstance(existing, str) and existing:
                        current_data[current_subsection] = existing + "\n" + text
                    else:
                        current_data[current_subsection] = text
                else:
                    existing = current_data.get("_text", "")
                    if existing:
                        current_data["_text"] = existing + "\n" + text
                    else:
                        current_data["_text"] = text
            i += 3  # paragraph_open, inline, paragraph_close
            continue

        i += 1

    # Flush last section
    if current_section is not None:
        sections[current_section] = _finalize_section(current_data)

    return sections


def _finalize_section(data: dict[str, Any]) -> Any:
    """Convert raw section data to final format."""
    if list(data.keys()) == ["_items"]:
        return data["_items"]
    if list(data.keys()) == ["_text"]:
        return data["_text"]
    return data


def _extract_list_items(tokens: list, start: int) -> list[str]:
    """Extract text content from a bullet_list starting at `start`."""
    items = []
    depth = 0
    i = start
    while i < len(tokens):
        t = tokens[i]
        if t.type == "bullet_list_open":
            depth += 1
        elif t.type == "bullet_list_close":
            depth -= 1
            if depth == 0:
                break
        elif t.type == "inline" and depth == 1:
            items.append(t.content)
        i += 1
    return items


def _extract_ordered_items(tokens: list, start: int) -> list[str]:
    """Extract text content from an ordered_list starting at `start`."""
    items = []
    depth = 0
    i = start
    while i < len(tokens):
        t = tokens[i]
        if t.type == "ordered_list_open":
            depth += 1
        elif t.type == "ordered_list_close":
            depth -= 1
            if depth == 0:
                break
        elif t.type == "inline" and depth == 1:
            text = re.sub(r"^\d+\.\s*", "", t.content)
            items.append(text)
        i += 1
    return items


def _parse_kv(text: str) -> tuple[str | None, str]:
    """Try to parse 'Key: Value' from a bullet item.

    Returns (normalized_key, value) or (None, original_text).
    """
    match = re.match(r"^([^:]+):\s*(.+)$", text, re.DOTALL)
    if match:
        key = _normalize_key(match.group(1))
        value = match.group(2).strip()
        return key, value
    return None, text
