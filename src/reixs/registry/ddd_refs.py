"""DDD reference format validation and registry."""

import re

DDD_REF_PATTERN = re.compile(r"^re-ddd:[\w_]+@\d+\.\d+\.\d+$")

KNOWN_DDD_REFS = {
    "re-ddd:lease_core_terms_ontario@0.1.0",
}


def is_valid_ddd_format(ref: str) -> bool:
    return bool(DDD_REF_PATTERN.match(ref))


def is_known_ddd_ref(ref: str) -> bool:
    return ref in KNOWN_DDD_REFS
