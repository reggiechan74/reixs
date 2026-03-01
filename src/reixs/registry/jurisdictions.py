"""Known jurisdiction profiles."""

KNOWN_JURISDICTIONS = {
    "ontario, canada": {"currency": "CAD", "area_unit": "sq ft"},
    "ontario": {"currency": "CAD", "area_unit": "sq ft"},
}


def is_known_jurisdiction(jurisdiction: str) -> bool:
    return jurisdiction.lower().strip() in KNOWN_JURISDICTIONS
