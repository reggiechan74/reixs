"""REIXS enumerations."""

from enum import Enum


class Tier(str, Enum):
    MICRO = "micro"
    STANDARD = "standard"
    COMPLEX = "complex"


class FieldStatus(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    MISSING = "missing"
    CONFLICT = "conflict"
